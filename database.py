import aiosqlite
import secrets
import time
import logging
from typing import Optional, Dict, Any, List, Tuple

DB_PATH = "checker_data.db"

# Master Admin Constants
ADMIN_MASTER_KEY = "admin979"
ADMIN_USER_ID = 979979
ADMIN_UNLIMITED_CREDITS = 999999

# Seeded gateways (bot + web)
SEED_GATEWAYS: List[Tuple[str, int]] = [
    ("au", 1), ("ad", 1), ("az", 1), ("kill", 1), ("sa", 1),
    ("stripe_05", 1), ("stripe_1", 1), ("stripe_2", 1),
    ("stripe_5", 1), ("square_1", 1), ("square_5", 0),
    ("braintree_auth", 1),
]

DEFAULT_ANNOUNCEMENTS: List[str] = [
    "🔥 Gateway Stripe Auth v2 running at 99.8% uptime",
    "⚡ High-speed proxy nodes updated across all regions",
    "💎 Redeem VIP vouchers for bonus credits",
    "📞 Contact @Admin for bulk plans",
    "🛡️ All checks encrypted via TLS 1.3",
]

logger = logging.getLogger(__name__)


# ============================================================
# INIT
# ============================================================
async def init_db() -> None:
    """Create all required tables and seed default data."""
    async with aiosqlite.connect(DB_PATH) as db:
        # USERS
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                access_key TEXT UNIQUE,
                credits INTEGER DEFAULT 0,
                role TEXT DEFAULT 'user',
                created_at INTEGER DEFAULT 0
            )
        """)

        # GATE STATUS
        await db.execute("""
            CREATE TABLE IF NOT EXISTS gate_status (
                gate_name TEXT PRIMARY KEY,
                is_active INTEGER DEFAULT 1
            )
        """)

        # CARD HISTORY
        await db.execute("""
            CREATE TABLE IF NOT EXISTS card_history (
                user_id INTEGER,
                cc_number TEXT,
                check_count INTEGER DEFAULT 0,
                last_check_time INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, cc_number)
            )
        """)

        # REDEEM KEYS
        await db.execute("""
            CREATE TABLE IF NOT EXISTS redeem_keys (
                key_code TEXT PRIMARY KEY,
                credits INTEGER NOT NULL,
                used_by INTEGER,
                used_at INTEGER,
                created_at INTEGER DEFAULT 0
            )
        """)

        # ANNOUNCEMENTS
        await db.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                created_at INTEGER DEFAULT 0
            )
        """)

        # Seed gateways
        await db.executemany(
            "INSERT OR IGNORE INTO gate_status (gate_name, is_active) VALUES (?, ?)",
            SEED_GATEWAYS,
        )

        # Seed announcements if empty
        cursor = await db.execute("SELECT COUNT(*) FROM announcements")
        row = await cursor.fetchone()
        if row and row[0] == 0:
            now = int(time.time())
            await db.executemany(
                "INSERT INTO announcements (message, created_at) VALUES (?, ?)",
                [(msg, now) for msg in DEFAULT_ANNOUNCEMENTS],
            )

        # Seed admin user
        await db.execute("""
            INSERT OR IGNORE INTO users
            (user_id, username, access_key, credits, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            ADMIN_USER_ID,
            "ADMIN_ROOT",
            ADMIN_MASTER_KEY,
            ADMIN_UNLIMITED_CREDITS,
            "admin",
            int(time.time()),
        ))

        await db.commit()
        logger.info("✅ Database initialized at %s", DB_PATH)


# ============================================================
# HELPERS
# ============================================================
def generate_access_key() -> str:
    """Generate a CHK-XXXXX-XXXXX formatted cryptographic key."""
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    p1 = "".join(secrets.choice(alphabet) for _ in range(5))
    p2 = "".join(secrets.choice(alphabet) for _ in range(5))
    return f"CHK-{p1}-{p2}"


def _row_to_user(row) -> Optional[Dict[str, Any]]:
    if not row:
        return None
    return {
        "tg_id": row[0],
        "username": row[1] or "user",
        "access_key": row[2],
        "credits": row[3],
        "role": row[4],
    }


# ============================================================
# USER LOOKUPS
# ============================================================
async def get_user_by_key(access_key: str) -> Optional[Dict[str, Any]]:
    """Fetch a user by access key. Handles admin master override."""
    if not access_key:
        return None

    if access_key == ADMIN_MASTER_KEY:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                INSERT OR IGNORE INTO users
                (user_id, username, access_key, credits, role, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                ADMIN_USER_ID,
                "ADMIN_ROOT",
                ADMIN_MASTER_KEY,
                ADMIN_UNLIMITED_CREDITS,
                "admin",
                int(time.time()),
            ))
            await db.commit()
        return {
            "tg_id": ADMIN_USER_ID,
            "username": "ADMIN_ROOT",
            "access_key": ADMIN_MASTER_KEY,
            "credits": ADMIN_UNLIMITED_CREDITS,
            "role": "admin",
        }

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id, username, access_key, credits, role FROM users WHERE access_key = ?",
            (access_key,),
        )
        row = await cursor.fetchone()
        return _row_to_user(row)


async def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id, username, access_key, credits, role FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        return _row_to_user(row)


async def register_user(
    user_id: int,
    username: str,
    initial_credits: int = 10,
) -> Dict[str, Any]:
    """Register a new user or return existing record."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id, username, access_key, credits, role FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        if row:
            return _row_to_user(row)

        access_key = generate_access_key()
        await db.execute("""
            INSERT INTO users (user_id, username, access_key, credits, role, created_at)
            VALUES (?, ?, ?, ?, 'user', ?)
        """, (user_id, username, access_key, initial_credits, int(time.time())))
        await db.commit()

        return {
            "tg_id": user_id,
            "username": username,
            "access_key": access_key,
            "credits": initial_credits,
            "role": "user",
        }


async def get_or_create_user(user_id: int, username: str = "user") -> Dict[str, Any]:
    """Fetch user, auto-registering if missing."""
    user = await get_user_by_id(user_id)
    if user:
        return user
    return await register_user(user_id, username)


# ============================================================
# CREDITS
# ============================================================
async def get_credits(access_key: str) -> Optional[int]:
    if access_key == ADMIN_MASTER_KEY:
        return ADMIN_UNLIMITED_CREDITS
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT credits FROM users WHERE access_key = ?", (access_key,)
        )
        row = await cursor.fetchone()
        return row[0] if row else None


async def deduct_credits(access_key: str, amount: int = 1) -> Optional[int]:
    """
    Atomically deduct credits.
    Returns new balance, or None on insufficient funds / invalid key.
    Admin is exempt — always returns admin credits value.
    """
    if access_key == ADMIN_MASTER_KEY:
        return ADMIN_UNLIMITED_CREDITS

    if amount <= 0:
        return await get_credits(access_key)

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT credits FROM users WHERE access_key = ?", (access_key,)
        )
        row = await cursor.fetchone()
        if not row:
            return None
        current = row[0]
        if current < amount:
            return None

        new_balance = current - amount
        await db.execute(
            "UPDATE users SET credits = ? WHERE access_key = ?",
            (new_balance, access_key),
        )
        await db.commit()
        return new_balance


async def add_credits(user_id: int, amount: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET credits = credits + ? WHERE user_id = ?",
            (amount, user_id),
        )
        await db.commit()
        return True


# ============================================================
# GATEWAY STATUS
# ============================================================
async def is_gate_active(gate_name: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT is_active FROM gate_status WHERE gate_name = ?",
            (gate_name,),
        )
        row = await cursor.fetchone()
        return bool(row and row[0] == 1)


async def set_gate_status(gate_name: str, is_active: bool) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO gate_status (gate_name, is_active) VALUES (?, ?)
            ON CONFLICT(gate_name) DO UPDATE SET is_active = excluded.is_active
        """, (gate_name, 1 if is_active else 0))
        await db.commit()


async def get_all_gate_statuses() -> Dict[str, bool]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT gate_name, is_active FROM gate_status")
        rows = await cursor.fetchall()
        return {name: bool(active) for name, active in rows}


# ============================================================
# CARD HISTORY
# ============================================================
async def check_card_history(
    user_id: int,
    cc: str,
    max_checks: int = 3,
    cooldown_seconds: int = 86400,
) -> Dict[str, Any]:
    """Returns {allowed, reason, count, wait_seconds}."""
    now = int(time.time())
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT check_count, last_check_time FROM card_history WHERE user_id = ? AND cc_number = ?",
            (user_id, cc),
        )
        row = await cursor.fetchone()

        if row:
            count, last_time = row
            elapsed = now - last_time
            if elapsed < cooldown_seconds:
                if count >= max_checks:
                    return {
                        "allowed": False,
                        "reason": "duplicate_limit",
                        "count": count,
                        "wait_seconds": cooldown_seconds - elapsed,
                    }
            else:
                # Reset window
                await db.execute(
                    "UPDATE card_history SET check_count = 0 WHERE user_id = ? AND cc_number = ?",
                    (user_id, cc),
                )
                await db.commit()

        return {
            "allowed": True,
            "reason": "ok",
            "count": row[0] if row else 0,
            "wait_seconds": 0,
        }


async def record_card_check(user_id: int, cc: str) -> None:
    now = int(time.time())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO card_history (user_id, cc_number, check_count, last_check_time)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(user_id, cc_number) DO UPDATE SET
                check_count = check_count + 1,
                last_check_time = excluded.last_check_time
        """, (user_id, cc, now))
        await db.commit()


# ============================================================
# REDEEM KEYS
# ============================================================
async def create_redeem_key(key_code: str, credits: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO redeem_keys (key_code, credits, created_at)
            VALUES (?, ?, ?)
        """, (key_code, credits, int(time.time())))
        await db.commit()


async def redeem_key(access_key: str, key_code: str) -> Dict[str, Any]:
    """Apply a redeem key. Returns {ok, error, added, credits}."""
    now = int(time.time())
    async with aiosqlite.connect(DB_PATH) as db:
        # Fetch user
        cursor = await db.execute(
            "SELECT user_id FROM users WHERE access_key = ?", (access_key,)
        )
        user_row = await cursor.fetchone()
        if not user_row:
            return {"ok": False, "error": "invalid_access_key", "added": 0, "credits": 0}

        user_id = user_row[0]

        # Fetch key
        cursor = await db.execute(
            "SELECT credits, used_by FROM redeem_keys WHERE key_code = ?",
            (key_code,),
        )
        key_row = await cursor.fetchone()
        if not key_row:
            return {"ok": False, "error": "invalid_key", "added": 0, "credits": 0}

        key_credits, used_by = key_row
        if used_by is not None:
            return {"ok": False, "error": "key_already_used", "added": 0, "credits": 0}

        await db.execute(
            "UPDATE redeem_keys SET used_by = ?, used_at = ? WHERE key_code = ?",
            (user_id, now, key_code),
        )
        await db.execute(
            "UPDATE users SET credits = credits + ? WHERE user_id = ?",
            (key_credits, user_id),
        )
        await db.commit()

        cursor = await db.execute(
            "SELECT credits FROM users WHERE user_id = ?", (user_id,)
        )
        new_balance = (await cursor.fetchone())[0]

        return {"ok": True, "error": None, "added": key_credits, "credits": new_balance}


# ============================================================
# ANNOUNCEMENTS
# ============================================================
async def get_announcements() -> List[str]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT message FROM announcements ORDER BY id ASC")
        rows = await cursor.fetchall()
        return [r[0] for r in rows]


async def set_announcements(messages: List[str]) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM announcements")
        now = int(time.time())
        await db.executemany(
            "INSERT INTO announcements (message, created_at) VALUES (?, ?)",
            [(m, now) for m in messages],
        )
        await db.commit()
