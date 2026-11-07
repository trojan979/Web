import asyncio
import logging
import os
import time
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

import database as db

# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("nexus.main")


# ============================================================
# OPTIONAL GATEWAY MODULES
# ============================================================
GATEWAY_FUNCS: Dict[str, Any] = {}
GATEWAYS_AVAILABLE = False

try:
    from gatet import Tele as TeleAU
    from gatet1 import Tele as TeleAD
    from gatet2 import Tele as TeleAZ
    from gatet3 import Tele as TeleSA
    from gatet4 import Tele as TeleKILL

    GATEWAY_FUNCS = {
        "au": TeleAU,
        "ad": TeleAD,
        "az": TeleAZ,
        "sa": TeleSA,
        "kill": TeleKILL,
    }
    GATEWAYS_AVAILABLE = True
    logger.info("✅ Gateway modules loaded successfully.")
except Exception as e:
    logger.warning("⚠️ Gateway modules not available: %s", e)


# ============================================================
# OPTIONAL TELEGRAM BOT
# ============================================================
TELEGRAM_APP = None
TELEGRAM_TASK: Optional[asyncio.Task] = None

try:
    from telegram.ext import ApplicationBuilder
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    logger.warning("⚠️ python-telegram-bot not installed — bot disabled.")


# ============================================================
# WEB <-> BOT GATEWAY MAPPING
# ============================================================
WEB_TO_BOT_GATEWAY: Dict[str, str] = {
    "stripe_05": "au",
    "stripe_1": "au",
    "stripe_2": "ad",
    "stripe_5": "ad",
    "square_1": "az",
    "square_5": "az",
    "braintree_auth": "sa",
    # Direct bot ids
    "au": "au",
    "ad": "ad",
    "az": "az",
    "sa": "sa",
    "kill": "kill",
}


# ============================================================
# PYDANTIC MODELS
# ============================================================
class AuthRequest(BaseModel):
    access_key: str = Field(..., min_length=1)


class CheckRequest(BaseModel):
    access_key: str
    data: str
    gateway: str = "stripe_1"


class RedeemRequest(BaseModel):
    access_key: str
    key_code: str


# ============================================================
# STATUS NORMALIZATION
# ============================================================
def parse_status(raw: str) -> str:
    """Map raw gateway response text to APPROVED | INSU | 3DS | DECLINED."""
    if not raw:
        return "DECLINED"
    text = str(raw).lower()

    if any(k in text for k in ["insufficient", "not enough", "nsf", "no funds"]):
        return "INSU"

    if any(k in text for k in ["3ds", "otp", "verification required", "challenge"]):
        return "3DS"

    if any(k in text for k in [
        "success", "thank", "approved", "charged", "succeeded",
    ]):
        return "APPROVED"

    return "DECLINED"


# ============================================================
# GATEWAY EXECUTOR (with retry)
# ============================================================
def run_gateway_check(cc: str, web_gateway: str) -> str:
    """Run underlying bot checker with retry logic for proxy timeouts."""
    bot_gateway = WEB_TO_BOT_GATEWAY.get(web_gateway, "au")
    func = GATEWAY_FUNCS.get(bot_gateway)

    if func is None:
        # Fallback stub — makes frontend testable without external modules
        return f"[SIMULATED] Checked {cc} via {bot_gateway}"

    last = None
    for attempt in range(3):
        try:
            last = str(func(cc))
            err = last.lower()
            if any(x in err for x in ["timeout", "proxy", "connection", "502", "503", "504"]):
                time.sleep(1.5)
                continue
            return last
        except Exception as e:
            last = f"Error: {e}"
            time.sleep(1.2)

    return last or "Timeout"


# ============================================================
# LIFESPAN — DB INIT + BOT START
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Init DB
    await db.init_db()

    # 2. Start Telegram bot in background
    global TELEGRAM_APP, TELEGRAM_TASK
    if TELEGRAM_AVAILABLE:
        try:
            from bot import (
                start as bot_start,
                register as bot_register,
                balance as bot_balance,
                au_check, ad_check, az_check, kill_check, sa_check,
                add_credit, control_gate, get_id, remove_file,
                start_addtxt, handle_document, cancel,
                UPLOAD_FILE, BOT_TOKEN,
            )
            from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler

            TELEGRAM_APP = ApplicationBuilder().token(BOT_TOKEN).build()
            TELEGRAM_APP.add_handler(CommandHandler("start", bot_start))
            TELEGRAM_APP.add_handler(CommandHandler("register", bot_register))
            TELEGRAM_APP.add_handler(CommandHandler("balance", bot_balance))
            TELEGRAM_APP.add_handler(CommandHandler("au", au_check))
            TELEGRAM_APP.add_handler(CommandHandler("ad", ad_check))
            TELEGRAM_APP.add_handler(CommandHandler("az", az_check))
            TELEGRAM_APP.add_handler(CommandHandler("kill", kill_check))
            TELEGRAM_APP.add_handler(CommandHandler("sa", sa_check))
            TELEGRAM_APP.add_handler(CommandHandler("add", add_credit))
            TELEGRAM_APP.add_handler(CommandHandler("gate", control_gate))
            TELEGRAM_APP.add_handler(CommandHandler("id", get_id))
            TELEGRAM_APP.add_handler(CommandHandler("rmtxt", remove_file))

            conv = ConversationHandler(
                entry_points=[CommandHandler("addtxt", start_addtxt)],
                states={UPLOAD_FILE: [MessageHandler(filters.Document.ALL, handle_document)]},
                fallbacks=[CommandHandler("cancel", cancel)],
            )
            TELEGRAM_APP.add_handler(conv)

            await TELEGRAM_APP.initialize()
            await TELEGRAM_APP.start()
            TELEGRAM_TASK = asyncio.create_task(TELEGRAM_APP.updater.start_polling())
            logger.info("✅ Telegram bot started in background.")
        except Exception as e:
            logger.error("❌ Failed to start Telegram bot: %s", e)

    yield

    # Shutdown
    if TELEGRAM_APP:
        try:
            await TELEGRAM_APP.updater.stop()
            await TELEGRAM_APP.stop()
            await TELEGRAM_APP.shutdown()
        except Exception:
            pass
    if TELEGRAM_TASK:
        TELEGRAM_TASK.cancel()


# ============================================================
# FASTAPI APP
# ============================================================
app = FastAPI(title="NEXUS OS v7.0 — CYBERPUNK ELITE", lifespan=lifespan)


# ============================================================
# ROOT — SERVE FRONTEND
# ============================================================
@app.get("/")
async def serve_index():
    path = os.path.join(os.path.dirname(__file__), "index.html")
    if not os.path.exists(path):
        return JSONResponse(
            {"detail": "index.html not found in server directory."},
            status_code=404,
        )
    return FileResponse(path, media_type="text/html")


# ============================================================
# AUTH
# ============================================================
@app.post("/api/auth")
async def api_auth(payload: AuthRequest):
    key = payload.access_key.strip()
    if not key:
        raise HTTPException(status_code=400, detail="Missing access_key")

    user = await db.get_user_by_key(key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Access Key")

    return {
        "tg_id": user["tg_id"],
        "username": user["username"],
        "access_key": user["access_key"],
        "credits": user["credits"],
        "role": user["role"],
    }


# ============================================================
# CHECK
# ============================================================
@app.post("/api/check")
async def api_check(payload: CheckRequest):
    key = payload.access_key.strip()
    data = payload.data.strip()
    gateway = (payload.gateway or "stripe_1").strip()

    if not key or not data:
        raise HTTPException(status_code=400, detail="Missing access_key or data")

    user = await db.get_user_by_key(key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Access Key")

    is_admin = user["role"] == "admin"

    # Cost — premium gateways cost 2
    cost = 2 if gateway in ("shopify_1", "square_5") else 1

    # Gate active check
    if not is_admin:
        active = await db.is_gate_active(gateway)
        if not active:
            return JSONResponse(
                {
                    "result": {
                        "status": "ERROR",
                        "data": data,
                        "response": f"Gateway '{gateway}' is offline / under maintenance.",
                    },
                    "credits": user["credits"],
                },
                status_code=200,
            )

    # Credit deduction (admin bypass)
    remaining = user["credits"]
    if not is_admin:
        remaining = await db.deduct_credits(key, cost)
        if remaining is None:
            raise HTTPException(status_code=402, detail="Out of credits")

    # Run check
    try:
        raw_response = run_gateway_check(data, gateway)
    except Exception as e:
        logger.exception("Gateway check failed")
        raw_response = f"Error: {e}"

    status = parse_status(raw_response)

    # Record history
    try:
        await db.record_card_check(user["tg_id"], data)
    except Exception:
        pass

    return {
        "result": {
            "status": status,
            "data": data,
            "response": raw_response,
        },
        "credits": remaining if not is_admin else user["credits"],
    }


# ============================================================
# REDEEM
# ============================================================
@app.post("/api/redeem")
async def api_redeem(payload: RedeemRequest):
    key = payload.access_key.strip()
    code = payload.key_code.strip()

    if not key or not code:
        raise HTTPException(status_code=400, detail="Missing access_key or key_code")

    result = await db.redeem_key(key, code)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Redeem failed"))

    return {
        "added": result["added"],
        "credits": result["credits"],
    }


# ============================================================
# ANNOUNCEMENTS
# ============================================================
@app.get("/api/announcement")
async def api_announcement():
    try:
        messages = await db.get_announcements()
        if not messages:
            messages = list(db.DEFAULT_ANNOUNCEMENTS)
        return {"messages": messages}
    except Exception:
        return {"messages": []}


# ============================================================
# GATEWAY STATUS
# ============================================================
@app.get("/api/gateways")
async def api_gateways():
    statuses = await db.get_all_gate_statuses()
    return {"gateways": statuses}


# ============================================================
# ADMIN — ANNOUNCEMENTS
# ============================================================
@app.post("/api/admin/announcement")
async def api_admin_announcement(payload: Dict[str, Any]):
    key = str(payload.get("access_key", "")).strip()
    user = await db.get_user_by_key(key)
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    messages = payload.get("messages")
    if not isinstance(messages, list) or not messages:
        raise HTTPException(status_code=400, detail="messages must be a non-empty list")

    await db.set_announcements([str(m) for m in messages])
    return {"ok": True, "count": len(messages)}


# ============================================================
# ADMIN — REDEEM KEY
# ============================================================
@app.post("/api/admin/redeem-key")
async def api_admin_redeem_key(payload: Dict[str, Any]):
    key = str(payload.get("access_key", "")).strip()
    user = await db.get_user_by_key(key)
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    code = str(payload.get("key_code", "")).strip()
    credits = int(payload.get("credits", 10))

    if not code:
        raise HTTPException(status_code=400, detail="key_code required")

    await db.create_redeem_key(code, credits)
    return {"ok": True, "key_code": code, "credits": credits}


# ============================================================
# ADMIN — GATEWAY TOGGLE
# ============================================================
@app.post("/api/admin/gateway")
async def api_admin_gateway(payload: Dict[str, Any]):
    key = str(payload.get("access_key", "")).strip()
    user = await db.get_user_by_key(key)
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    gate = str(payload.get("gateway", "")).strip()
    is_active = bool(payload.get("active", True))
    if not gate:
        raise HTTPException(status_code=400, detail="gateway required")

    await db.set_gate_status(gate, is_active)
    return {"ok": True, "gateway": gate, "active": is_active}


# ============================================================
# HEALTH
# ============================================================
@app.get("/api/health")
async def api_health():
    return {
        "status": "online",
        "bot_running": TELEGRAM_APP is not None,
        "gateways_available": GATEWAYS_AVAILABLE,
        "time": int(time.time()),
    }


# ============================================================
# ENTRYPOINT
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
