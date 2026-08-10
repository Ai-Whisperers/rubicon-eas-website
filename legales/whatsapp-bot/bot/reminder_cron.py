"""
Ometz Dental — Reminder Cron
=============================
Runs every hour. Checks for appointments 24h from now and sends
a WhatsApp reminder to the patient.

Also sends review request 24h AFTER attended appointment.

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

# === CONFIG ===
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "https://evolution.sunstein.cloud")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")
INSTANCE = os.getenv("EVOLUTION_INSTANCE", "ometsdental-business")

# Postgres
PG_CONTAINER = "postgres_postgres.1.kpmo0dfqbz28pltocxlmtj8lu"
PG_USER = "postgres"
PG_DB = "ometsdental"

TIMEZONE_OFFSET = -4

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("ometsdental-reminders")


def now_asuncion():
    return datetime.now(timezone(timedelta(hours=TIMEZONE_OFFSET)))


def pg_query(sql):
    cmd = ["docker", "exec", PG_CONTAINER, "psql", "-U", PG_USER, "-d", PG_DB, "-At", "-F", "|", "-c", sql]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if result.returncode != 0:
        logger.error(f"PG query failed: {result.stderr}")
        return []
    rows = []
    for line in result.stdout.strip().split("\n"):
        if line:
            rows.append(line.split("|"))
    return rows


def pg_exec(sql):
    cmd = ["docker", "exec", PG_CONTAINER, "psql", "-U", PG_USER, "-d", PG_DB, "-c", sql]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    return result.returncode == 0


async def send_message(phone, text):
    async with httpx.AsyncClient(timeout=30) as client:
        result = await client.post(
            f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE}",
            headers={"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"},
            json={"number": phone, "text": text},
        )
        return result.status_code == 201 or result.status_code == 200


async def send_24h_reminders():
    """Find appointments 24h from now, send reminder."""
    now = now_asuncion()
    # Window: 23-25h from now
    start = now + timedelta(hours=23)
    end = now + timedelta(hours=25)

    rows = pg_query(f"""
        SELECT id, phone, patient_name, scheduled_at, reminder_sent_24h
        FROM wa_appointments
        WHERE status = 'scheduled'
          AND scheduled_at BETWEEN '{start.isoformat()}' AND '{end.isoformat()}'
          AND reminder_sent_24h = FALSE
    """)

    logger.info(f"Found {len(rows)} appointments needing 24h reminder")

    weekday_names = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    for row in rows:
        appt_id, phone, name, scheduled_at, _ = row

        try:
            dt = datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
            day_name = weekday_names[dt.weekday()]
            time_str = dt.strftime("%H:%M")
        except Exception as e:
            logger.error(f"Date parse error for appt {appt_id}: {e}")
            continue

        msg = f"""⏰ Recordatorio de tu cita

📅 {day_name.title()} {dt.strftime('%d/%m')} a las {time_str}
📍 Auditores de la Guerra del Chaco 617, Mburucuyá
⏱️ 60 minutos

ID: #{appt_id}

¿Necesitás cancelar o cambiar? /cancelar
¿Querés confirmar? Respondé "confirmo"

— Equipo Ometz Dental"""

        if await send_message(phone, msg):
            pg_exec(f"UPDATE wa_appointments SET reminder_sent_24h = TRUE, updated_at = NOW() WHERE id = {appt_id}")
            logger.info(f"✅ 24h reminder sent for appt {appt_id} to {phone}")
        else:
            logger.error(f"❌ Failed to send reminder for appt {appt_id}")


async def send_post_attended_reviews():
    """Find appointments attended 24h ago, send Google review request."""
    now = now_asuncion()
    # Window: 20-28h ago (attended)
    start = now - timedelta(hours=28)
    end = now - timedelta(hours=20)

    rows = pg_query(f"""
        SELECT id, phone, patient_name, attended_at
        FROM wa_appointments
        WHERE status = 'attended'
          AND attended_at BETWEEN '{start.isoformat()}' AND '{end.isoformat()}'
          AND review_requested = FALSE
    """)

    logger.info(f"Found {len(rows)} attended appointments needing review request")

    for row in rows:
        appt_id, phone, name, attended_at = row

        msg = f"""¡Hola {name}! 👋

Gracias por tu visita a Ometz Dental. 🙏

Si tu experiencia fue buena, me ayudaría mucho si pudieras dejarme una breve reseña en Google. Solo te toma 1 minuto:

👉 https://g.page/r/ometz-dental/review

Tu opinión ayuda a que más personas encuentren atención dental honesta en Asunción.

¡Gracias! 💚
— Dra. Gaby"""

        if await send_message(phone, msg):
            pg_exec(f"UPDATE wa_appointments SET review_requested = TRUE, updated_at = NOW() WHERE id = {appt_id}")
            logger.info(f"✅ Review request sent for appt {appt_id} to {phone}")


async def main():
    logger.info("🕐 Reminder cron starting")
    await send_24h_reminders()
    await send_post_attended_reviews()
    logger.info("✅ Reminder cron finished")


if __name__ == "__main__":
    asyncio.run(main())
