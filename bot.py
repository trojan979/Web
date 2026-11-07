import sqlite3
import logging
import time
import os
import random
import re
from typing import Optional, Tuple

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

# ============================================================
# CONFIG
# ============================================================
BOT_TOKEN = "8682439584:AAEZNqlGag6WzOsvB4odTkjc3TjNHqAgWN4"
ADMIN_ID = 7954343626  # Your Telegram admin user id

DB_PATH = "checker_data.db"

UPLOAD_FILE = 1

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("nexus.bot")


# ============================================================
# SAFE IMPORTS — GATEWAY MODULES
# ============================================================
GATEWAYS_AVAILABLE = False
GATEWAY_FUNCS = {}

try:
    from gatet import Tele as TeleAU
    from gatet1 import Tele as TeleAD
    from gatet2 import Tele as TeleAZ
    from gatet3 import Tele as TeleSA
    from gatet4 import Tele as TeleKILL
    from hit_sender import send as send_hit

    GATEWAY_FUNCS = {
        "au": TeleAU,
        "ad": TeleAD,
        "az": TeleAZ,
        "sa": TeleSA,
        "kill": TeleKILL,
    }
    GATEWAYS_AVAILABLE = True
    logger.info("✅ Gateway modules loaded in bot.")
except Exception as e:
    logger.warning("⚠️ Gateway modules not available in bot: %s", e)

    # Fallback stubs so the bot still runs
    def _stub(cc): return f"[SIMULATED] checked {cc}"
    GATEWAY_FUNCS = {
        "au": _stub, "ad": _stub, "az": _stub, "sa": _stub, "kill": _stub,
    }

    def send_hit(cc, status, username, elapsed):
        return f"<b>{cc}</b>\nStatus: {status}\nBy @{username} • {elapsed}s"


# ============================================================
# DATABASE HELPERS (sync)
# ============================================================
def _get_db() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def _generate_access_key() -> str:
    import secrets
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    p1 = "".join(secrets.choice(alphabet) for _ in range(5))
    p2 = "".join(secrets.choice(alphabet) for _ in range(5))
    return f"CHK-{p1}-{p2}"


def _get_or_create_user(user_id: int, username: str = "user") -> dict:
    """Fetch or create a user (auto-generates access key)."""
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, username, access_key, credits, role FROM users WHERE user_id = ?",
        (user_id,),
    )
    row = cursor.fetchone()
    if row:
        conn.close()
        return {
            "tg_id": row[0], "username": row[1] or "user",
            "access_key": row[2], "credits": row[3], "role": row[4],
        }

    access_key = _generate_access_key()
    cursor.execute("""
        INSERT INTO users (user_id, username, access_key, credits, role, created_at)
        VALUES (?, ?, ?, 10, 'user', ?)
    """, (user_id, username, access_key, int(time.time())))
    conn.commit()
    conn.close()

    return {
        "tg_id": user_id, "username": username,
        "access_key": access_key, "credits": 10, "role": "user",
    }


def _get_credits(user_id: int) -> Optional[int]:
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def _deduct_credits(user_id: int, amount: int = 1) -> Optional[int]:
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if not row or row[0] < amount:
        conn.close()
        return None

    new_balance = row[0] - amount
    cursor.execute(
        "UPDATE users SET credits = ? WHERE user_id = ?", (new_balance, user_id)
    )
    conn.commit()
    conn.close()
    return new_balance


def _is_gate_on(gate_name: str) -> bool:
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT is_active FROM gate_status WHERE gate_name = ?", (gate_name,)
    )
    row = cursor.fetchone()
    conn.close()
    return bool(row and row[0] == 1)


def _check_history(user_id: int, cc: str, max_checks: int = 3, cooldown: int = 86400) -> dict:
    now = int(time.time())
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT check_count, last_check_time FROM card_history WHERE user_id = ? AND cc_number = ?",
        (user_id, cc),
    )
    row = cursor.fetchone()

    if row:
        count, last_time = row
        elapsed = now - last_time
        if elapsed < cooldown:
            if count >= max_checks:
                conn.close()
                return {"allowed": False, "wait": cooldown - elapsed, "count": count}
        else:
            cursor.execute(
                "UPDATE card_history SET check_count = 0 WHERE user_id = ? AND cc_number = ?",
                (user_id, cc),
            )
            conn.commit()

    conn.close()
    return {"allowed": True, "wait": 0, "count": row[0] if row else 0}


def _record_check(user_id: int, cc: str) -> None:
    now = int(time.time())
    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO card_history (user_id, cc_number, check_count, last_check_time)
        VALUES (?, ?, 1, ?)
        ON CONFLICT(user_id, cc_number) DO UPDATE SET
            check_count = check_count + 1,
            last_check_time = excluded.last_check_time
    """, (user_id, cc, now))
    conn.commit()
    conn.close()


# ============================================================
# CARD PARSER
# ============================================================
def parse_card(cc: str) -> Tuple[str, str, str, str]:
    """Robust card parser — handles multiple formats."""
    cc = cc.strip()
    n = mm = yy = cvc = ""

    card_match = re.search(r'\b\d{15,16}\b', cc)
    expiry_match = re.search(r'\b(\d{1,2})[\\/\-](\d{2,4})\b', cc)

    if card_match and expiry_match:
        n = card_match.group(0)
        mm = expiry_match.group(1)
        yy = expiry_match.group(2)
        remaining = cc.replace(n, "").replace(expiry_match.group(0), "")
        cvv_match = re.search(r'\b\d{3,4}\b', remaining)
        if cvv_match:
            cvc = cvv_match.group(0)
    else:
        numbers = re.findall(r'\d+', cc)
        if len(numbers) >= 4:
            n, mm, yy, cvc = numbers[0], numbers[1], numbers[2], numbers[3]

    if n and mm and yy:
        mm = str(int(mm))
        if len(yy) == 4:
            yy = yy[-2:]

    return n, mm, yy, cvc


# ============================================================
# ADMIN-ONLY FILE COMMANDS
# ============================================================
async def remove_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("⚠️ Usage: `/rmtxt proxy.txt`", parse_mode="Markdown")
        return
    filename = context.args[0]
    try:
        if os.path.exists(filename):
            os.remove(filename)
            await update.message.reply_text(f"✅ Deleted **{filename}**", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"❌ File **{filename}** not found.", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def start_addtxt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return ConversationHandler.END
    await update.message.reply_text(
        "📁 Please upload the **.txt** file you want to save.\n\nCancel with /cancel",
        parse_mode="Markdown",
    )
    return UPLOAD_FILE


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_name = update.message.document.file_name
    if not file_name.endswith(('.txt', '.py')):
        await update.message.reply_text("❌ Only .txt or .py files are accepted.")
        return UPLOAD_FILE
    try:
        await file.download_to_drive(file_name)
        await update.message.reply_text(
            f"✅ File **{file_name}** saved successfully.", parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Save failed: {e}")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operation cancelled.")
    return ConversationHandler.END


# ============================================================
# CORE COMMANDS
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Auto-register user + display access key, credits, and commands."""
    user_id = update.effective_user.id
    username = update.effective_user.username or f"user_{user_id}"

    user = _get_or_create_user(user_id, username)
    access_key = user["access_key"]
    credits = user["credits"]

    await update.message.reply_text(
        "👋 Welcome to **NEXUS OS v7.0 — CYBERPUNK ELITE**!\n\n"
        f"🔑 **Your Web Access Key:**\n`{access_key}`\n\n"
        f"💳 **Credits:** {credits}\n\n"
        "**Available Commands:**\n"
        "/register - Register account (10 free credits)\n"
        "/balance - Check credit balance\n"
        "/au - Authorize 1 (1 Credit)\n"
        "/ad - Authorize 2 (1 Credit)\n"
        "/az - Authorize 3 (1 Credit)\n"
        "/kill - CC Kill USA Visa Only (1 Credit)\n"
        "/sa - Stripe Auth (Free)\n\n"
        "🌐 **Web Dashboard:** Use your access key above to log in.\n"
        "📞 **Contact:** @strawhatchannel69",
        parse_mode="Markdown",
    )


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or f"user_{user_id}"

    conn = _get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        conn.close()
        await update.message.reply_text("❌ You are already registered. Use /balance to check credits.")
        return

    access_key = _generate_access_key()
    cursor.execute("""
        INSERT INTO users (user_id, username, access_key, credits, role, created_at)
        VALUES (?, ?, ?, 10, 'user', ?)
    """, (user_id, username, access_key, int(time.time())))
    conn.commit()
    conn.close()

    await update.message.reply_text(
        "✅ Registration successful!\n\n"
        f"🔑 **Access Key:** `{access_key}`\n"
        "💳 **Credits:** 10\n\n"
        "Use this key to log in to the web dashboard.",
        parse_mode="Markdown",
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    credits = _get_credits(user_id)
    if credits is None:
        await update.message.reply_text("⚠️ Please /register first.")
        return
    await update.message.reply_text(f"💰 Balance: **{credits}** credits", parse_mode="Markdown")


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🆔 Chat ID: `{update.effective_chat.id}`\n"
        f"👤 User ID: `{update.effective_user.id}`",
        parse_mode="Markdown",
    )


# ============================================================
# GATEWAY CHECK FLOW
# ============================================================
def _is_chat_allowed(chat_id: int) -> bool:
    """Optional whitelist via group.txt — free checks for allowed chats."""
    filename = "group.txt"
    if not os.path.exists(filename):
        return False
    try:
        with open(filename, "r") as f:
            ids = [line.strip() for line in f.readlines() if line.strip()]
        return str(chat_id) in ids
    except Exception:
        return False


async def process_card_check(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    gate_func,
    gate_name: str,
):
    if not _is_gate_on(gate_name):
        await update.message.reply_text(
            f"❌ Gateway **{gate_name}** is currently offline for maintenance.",
            parse_mode="Markdown",
        )
        return

    user_id = update.effective_user.id
    username = update.effective_user.username or "NoUsername"
    current_chat_id = update.effective_chat.id
    is_free_group = _is_chat_allowed(current_chat_id)

    if not context.args:
        await update.message.reply_text(
            f"⚠️ Card format invalid. Example: `/{gate_name} cc|mm|yy|cvc`",
            parse_mode="Markdown",
        )
        return

    cc = " ".join(context.args).strip()

    # Ensure user exists
    user = _get_or_create_user(user_id, username)

    # Credit check (skip for free groups and /sa)
    if not is_free_group and gate_name != "sa":
        if user["role"] != "admin" and user["credits"] <= 0:
            await update.message.reply_text(
                "❌ Insufficient credits. Please redeem a voucher."
            )
            return

    # Duplicate check
    hist = _check_history(user_id, cc)
    if not hist["allowed"]:
        wait = hist["wait"]
        hours = wait // 3600
        minutes = (wait % 3600) // 60
        await update.message.reply_text(
            f"❌ **Duplicate check detected!**\n\n"
            f"This card has been checked 3 times in 24 hours. "
            f"Please wait **{hours}h {minutes}m** before retrying.",
            parse_mode="Markdown",
        )
        return

    msg = await update.message.reply_text("🔍 Processing your card...")
    start_time = time.time()

    try:
        # ==== /kill — auto 10 randomized CVV attempts ====
        if gate_name == "kill":
            n, mm, yy, _ = parse_card(cc)
            if not n or not mm or not yy:
                await msg.edit_text("❌ Card data incomplete or invalid format.")
                return

            results_list = []
            total_checks = 10

            for i in range(1, total_checks + 1):
                await msg.edit_text(
                    f"🔍 **Visa Killing... ({i}/{total_checks})** ⏳\n"
                    f"Card: <code>{n}|{mm}|{yy}</code>",
                    parse_mode="HTML",
                )

                rand_cvc = str(random.randint(100, 999))
                loop_cc = f"{n}|{mm}|{yy}|{rand_cvc}"

                last = None
                for retry in range(5):
                    try:
                        last = str(gate_func(loop_cc))
                        err = last.lower()
                        if any(x in err for x in [
                            "timeout", "proxy", "connection aborted",
                            "connection error", "read timed out",
                            "ssl", "502", "503", "504",
                        ]):
                            if retry < 4:
                                await msg.edit_text(
                                    f"🔄 Retry ({i}/{total_checks}) — proxy retry {retry+1}/5"
                                )
                                time.sleep(2)
                                continue
                        break
                    except Exception as e:
                        err = str(e).lower()
                        if any(x in err for x in [
                            "timeout", "proxy", "connection", "ssl", "502", "503", "504",
                        ]):
                            if retry < 4:
                                await msg.edit_text(
                                    f"🔄 Retry ({i}/{total_checks}) — conn retry {retry+1}/5"
                                )
                                time.sleep(2)
                                continue
                        last = "Proxy Error"
                        break

                if last is None:
                    last = "Proxy Timeout"

                ll = last.lower()
                if any(x in ll for x in ["success", "thank"]):
                    status = "Charged 💥"
                elif "succeeded" in ll:
                    status = "Approved 💥"
                else:
                    status = "Declined ❌"

                results_list.append(f"<code>{loop_cc}</code> ➜ <b>{status}</b>")

                if not is_free_group and user["role"] != "admin":
                    _deduct_credits(user_id, 1)

            _record_check(user_id, cc)
            elapsed = round(time.time() - start_time, 2)
            combined = "\n".join(results_list)
            resp = send_hit(combined, "Visa Killed ✅", username, elapsed)
            await msg.edit_text(resp, parse_mode="HTML")

        # ==== Standard gateways (au / ad / az / sa) ====
        else:
            last = None
            for attempt in range(5):
                try:
                    last = str(gate_func(cc))
                    err = last.lower()
                    if any(x in err for x in [
                        "timeout", "proxy", "connection aborted",
                        "connection error", "remote disconnected",
                        "read timed out", "ssl", "502", "503", "504",
                    ]):
                        if attempt < 4:
                            await msg.edit_text(
                                f"⚠️ Proxy timeout...\n🔄 Retrying ({attempt+1}/5)"
                            )
                            time.sleep(2)
                            continue
                    break
                except Exception as e:
                    err = str(e).lower()
                    if any(x in err for x in [
                        "timeout", "proxy", "connection", "ssl", "502", "503", "504",
                    ]):
                        if attempt < 4:
                            await msg.edit_text(
                                f"⚠️ Connection error...\n🔄 Retrying ({attempt+1}/5)"
                            )
                            time.sleep(2)
                            continue
                    raise e

            if last is None:
                await msg.edit_text("❌ Proxy timeout after 5 retries.")
                return

            _record_check(user_id, cc)

            if not is_free_group and user["role"] != "admin" and gate_name != "sa":
                _deduct_credits(user_id, 1)

            ll = last.lower()
            if any(x in ll for x in ["success", "thank"]):
                last = "Charged 💥"
            elif "succeeded" in ll:
                last = "Approved 💥"

            elapsed = round(time.time() - start_time, 2)
            resp = send_hit(cc, last, username, elapsed)
            await msg.edit_text(resp, parse_mode="HTML")

    except Exception as e:
        logger.error(f"Check error: {e}")
        await msg.edit_text(f"❌ An error occurred: try again.")


# ============================================================
# GATEWAY COMMAND HANDLERS
# ============================================================
async def au_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_card_check(update, context, GATEWAY_FUNCS["au"], "au")


async def ad_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_card_check(update, context, GATEWAY_FUNCS["ad"], "ad")


async def az_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_card_check(update, context, GATEWAY_FUNCS["az"], "az")


async def kill_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_card_check(update, context, GATEWAY_FUNCS["kill"], "kill")


async def sa_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_card_check(update, context, GATEWAY_FUNCS["sa"], "sa")


# ============================================================
# ADMIN COMMANDS
# ============================================================
async def add_credit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        target_id = int(context.args[0])
        amount = int(context.args[1])
        conn = _get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET credits = credits + ? WHERE user_id = ?",
            (amount, target_id),
        )
        conn.commit()
        conn.close()
        await update.message.reply_text(f"✅ User {target_id} +{amount} credits.")
    except Exception:
        await update.message.reply_text("Usage: `/add [USER_ID] [AMOUNT]`", parse_mode="Markdown")


async def control_gate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        gate_name = context.args[0].lower()
        action = context.args[1].lower()
        status = 1 if action == "on" else 0
        conn = _get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE gate_status SET is_active = ? WHERE gate_name = ?",
            (status, gate_name),
        )
        conn.commit()
        conn.close()
        await update.message.reply_text(f"✅ Gateway **{gate_name}** → {action}", parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(
            "Usage: `/gate [au|ad|az|kill|sa|stripe_1|...] [on|off]`",
            parse_mode="Markdown",
        )


# ============================================================
# STANDALONE ENTRYPOINT (for direct bot execution)
# ============================================================
def build_application():
    """Build and return the Telegram Application object (used by main.py too)."""
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("au", au_check))
    app.add_handler(CommandHandler("ad", ad_check))
    app.add_handler(CommandHandler("az", az_check))
    app.add_handler(CommandHandler("kill", kill_check))
    app.add_handler(CommandHandler("sa", sa_check))
    app.add_handler(CommandHandler("add", add_credit))
    app.add_handler(CommandHandler("gate", control_gate))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("rmtxt", remove_file))

    conv = ConversationHandler(
        entry_points=[CommandHandler("addtxt", start_addtxt)],
        states={UPLOAD_FILE: [MessageHandler(filters.Document.ALL, handle_document)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)

    return app


if __name__ == "__main__":
    logger.info("Starting bot in standalone mode...")
    build_application().run_polling()
