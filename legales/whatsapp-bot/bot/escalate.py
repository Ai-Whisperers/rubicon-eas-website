"""
Ometz Dental — Escalation Notifier
===================================
Sends notifications to Gaby/Kiki when escalations happen.
Uses Telegram bot (free, no SMTP needed) or SendGrid email.

Owner: Erebus (Hermes-AI)
"""

import os
import sys
import json
import logging
import subprocess
import httpx
import asyncio
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv("/root/ometsdental-bot/.env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("ometsdental-escalate")

# === CONFIG ===
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "https://evolution.sunstein.cloud")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")
INSTANCE = os.getenv("EVOLUTION_INSTANCE", "ometsdental-business")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")  # Gaby or Kiki

# Email (SendGrid)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
GABY_EMAIL = os.getenv("GABY_EMAIL", "doctora.gabi@ometsdental.com")
KIKI_EMAIL = os.getenv("KIKI_EMAIL", "")

# Postgres
PG_CONTAINER = "postgres_postgres.1.kpmo0dfqbz28pltocxlmtj8lu"
PG_USER = "postgres"
PG_DB = "ometsdental"

TIMEZONE_OFFSET = -4


def now_asuncion():
    return datetime.now(timezone(timedelta(hours=TIMEZONE_OFFSET)))


def pg_query(sql):
    cmd = ["docker", "exec", PG_CONTAINER, "psql", "-U", PG_USER, "-d", PG_DB, "-At", "-F", "|", "-c", sql]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if result.returncode != 0:
        logger.error(f"PG query failed: {result.stderr}")
        return []
    return [line.split("|") for line in result.stdout.strip().split("\n") if line]


def pg_exec(sql):
    cmd = ["docker", "exec", PG_CONTAINER, "psql", "-U", PG_USER, "-d", PG_DB, "-c", sql]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    return result.returncode == 0


async def send_telegram_notification(phone, message_text, category, priority):
    """Send Telegram notification to Gaby."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.debug("Telegram not configured, skipping")
        return False

    urgency_emoji = "🚨" if priority == "URGENT" else "⚠️"
    text = f"""{urgency_emoji} Ometz Dental — Escalación

📱 De: {phone}
🏷️ Categoría: {category}
📊 Prioridad: {priority}

💬 Mensaje:
{message_text[:500]}

⏰ {now_asuncion().strftime('%Y-%m-%d %H:%M:%S')}

Para responder, abrí WA Business:
https://evolution.sunstein.cloud/manager
"""

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            result = await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": text,
                    "parse_mode": "HTML",
                },
            )
            if result.status_code == 200:
                logger.info(f"✅ Telegram notification sent for {phone}")
                return True
            logger.error(f"Telegram error: {result.status_code} {result.text[:200]}")
    except Exception as e:
        logger.error(f"Telegram error: {e}")
    return False


async def send_email_notification(phone, message_text, category, priority):
    """Send email via SendGrid."""
    if not SENDGRID_API_KEY:
        logger.debug("SendGrid not configured, skipping")
        return False

    urgency = "URGENTE" if priority == "URGENT" else "Normal"
    subject = f"[{urgency}] Ometz Dental — Nuevo mensaje de {phone}"
    html = f"""<h2>{urgency}: Nuevo mensaje en Ometz Dental</h2>
<p><strong>De:</strong> {phone}</p>
<p><strong>Categoría:</strong> {category}</p>
<p><strong>Prioridad:</strong> {priority}</p>
<p><strong>Fecha:</strong> {now_asuncion().strftime('%Y-%m-%d %H:%M:%S')}</p>
<h3>Mensaje:</h3>
<blockquote>{message_text[:1000]}</blockquote>
<p><a href="https://admin.sunstein.cloud/">Abrir Dashboard</a></p>
<p><a href="https://evolution.sunstein.cloud/manager">Abrir WA Manager</a></p>
"""

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            result = await client.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={
                    "Authorization": f"Bearer {SENDGRID_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "personalizations": [{"to": [{"email": GABY_EMAIL}] + ([{"email": KIKI_EMAIL}] if KIKI_EMAIL else [])}],
                    "from": {"email": "bot@ometsdental.com", "name": "Ometz Dental Bot"},
                    "subject": subject,
                    "content": [{"type": "text/html", "value": html}],
                },
            )
            if result.status_code == 202:
                logger.info(f"✅ Email sent for {phone}")
                return True
            logger.error(f"SendGrid error: {result.status_code} {result.text[:200]}")
    except Exception as e:
        logger.error(f"SendGrid error: {e}")
    return False


async def send_wa_internal_notification(phone, message_text, category, priority):
    """Send WhatsApp notification to Gaby's personal number."""
    gaby_personal = os.getenv("GABY_PERSONAL_WA", "")
    if not gaby_personal:
        return False

    urgency_emoji = "🚨" if priority == "URGENT" else "⚠️"
    text = f"""{urgency_emoji} Bot Ometz — Escalación

📱 {phone}
🏷️ {category}

{message_text[:300]}

Responde desde WA Business:
https://evolution.sunstein.cloud/manager"""

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            result = await client.post(
                f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE}",
                headers={"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"},
                json={"number": gaby_personal, "text": text},
            )
            if result.status_code in (200, 201):
                logger.info(f"✅ WA internal notification sent")
                return True
    except Exception as e:
        logger.error(f"WA internal error: {e}")
    return False


async def process_escalations():
    """Find pending escalations and notify."""
    rows = pg_query("""
        SELECT id, phone, category, priority, original_message
        FROM wa_escalations
        WHERE status = 'pending'
        ORDER BY
            CASE priority
                WHEN 'URGENT' THEN 1
                WHEN 'HOT_LEAD' THEN 2
                WHEN 'APPOINTMENT' THEN 3
                WHEN 'PRICING' THEN 4
                ELSE 5
            END,
            created_at
        LIMIT 10
    """)

    if not rows:
        logger.info("No pending escalations")
        return

    logger.info(f"Found {len(rows)} pending escalations")

    for row in rows:
        if len(row) < 5:
            continue
        esc_id, phone, category, priority, message = row

        # Send via all configured channels
        sent = False
        sent = await send_telegram_notification(phone, message, category, priority) or sent
        sent = await send_email_notification(phone, message, category, priority) or sent
        sent = await send_wa_internal_notification(phone, message, category, priority) or sent

        if sent:
            # Mark as notified (but still pending for human response)
            pg_exec(f"UPDATE wa_escalations SET status = 'notified', updated_at = NOW() WHERE id = {esc_id}")
            logger.info(f"✅ Escalation {esc_id} notified via channel")
        else:
            logger.warning(f"⚠️ No channel configured for escalation {esc_id}")


async def main():
    logger.info("🚨 Escalation notifier starting")
    await process_escalations()
    logger.info("✅ Done")


if __name__ == "__main__":
    asyncio.run(main())
