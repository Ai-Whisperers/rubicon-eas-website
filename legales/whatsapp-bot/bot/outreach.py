"""
Ometz Dental — Outreach Tool
=============================
Send personalized WhatsApp messages to a list of patients.

Usage:
1. Create a CSV file with columns: phone,name,last_visit
2. Run: python3 outreach.py patients.csv

CSV format:
    phone,name,last_visit,notes
    595981324569,Juan Pérez,2025-03-15,Limpieza
    595987123456,María López,2024-11-20,Restauración
"""

import os
import sys
import csv
import json
import time
import logging
import asyncio
import httpx
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("/root/ometsdental-bot/.env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("ometsdental-outreach")

EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "https://evolution.sunstein.cloud")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")
INSTANCE = os.getenv("EVOLUTION_INSTANCE", "ometsdental-business")

DELAY_BETWEEN_MESSAGES = 10  # seconds (anti-ban)


def make_message(name, last_visit, notes):
    """Generate personalized outreach message."""
    first_name = name.split()[0] if name else "Hola"

    if last_visit:
        try:
            dt = datetime.fromisoformat(last_visit)
            last_visit_str = dt.strftime("%B %Y")  # "March 2025"
            time_ago = (datetime.now() - dt).days
            if time_ago < 90:
                time_phrase = "hace poco"
            elif time_ago < 365:
                time_phrase = f"hace {time_ago // 30} meses"
            else:
                time_phrase = f"hace {time_ago // 365} año(s)"
        except Exception:
            time_phrase = "hace tiempo"
            last_visit_str = last_visit
    else:
        time_phrase = "hace tiempo"
        last_visit_str = "tu última visita"

    if notes:
        context = f" por {notes.lower()}"
    else:
        context = ""

    return f"""Hola {first_name} 👋

Soy la Dra. Gaby González. {time_phrase.capitalize()} te atendí{context} en mi consultorio.

Te cuento que **abrí mi propio consultorio en Mburucuyá** (Auditores de la Guerra del Chaco 617, Asunción). Estoy atendiendo con la misma dedicación pero con más tiempo para cada paciente.

Si necesitás algo, escribime por acá. También acepto segunda opinión sin compromiso.

Si tu experiencia fue buena, me ayudaría mucho una reseña en Google 🙏:
👉 https://g.page/r/ometz-dental/review

— Dra. Gaby
Ometz Dental · אומץ"""


async def send_one(phone, message, dry_run=False):
    if dry_run:
        logger.info(f"[DRY-RUN] Would send to {phone}:")
        logger.info(f"   {message[:200]}...")
        return True

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            result = await client.post(
                f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE}",
                headers={"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"},
                json={"number": phone, "text": message},
            )
            if result.status_code in (200, 201):
                logger.info(f"✅ Sent to {phone}")
                return True
            logger.error(f"❌ Failed {phone}: {result.status_code} {result.text[:200]}")
            return False
        except Exception as e:
            logger.error(f"❌ Error {phone}: {e}")
            return False


async def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        sys.exit(1)

    dry_run = "--dry-run" in sys.argv
    if dry_run:
        logger.info("🧪 DRY RUN MODE — no messages will be sent")

    # Read CSV
    sent = 0
    failed = 0
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    logger.info(f"Found {len(rows)} patients in CSV")

    for i, row in enumerate(rows):
        phone = row.get("phone", "").strip()
        name = row.get("name", "").strip()
        last_visit = row.get("last_visit", "").strip()
        notes = row.get("notes", "").strip()

        if not phone:
            logger.warning(f"Row {i+1}: missing phone, skipping")
            continue

        # Clean phone
        phone_clean = phone.replace("+", "").replace(" ", "").replace("-", "")
        if not phone_clean.isdigit():
            logger.warning(f"Row {i+1}: invalid phone '{phone}', skipping")
            continue

        message = make_message(name, last_visit, notes)
        ok = await send_one(phone_clean, message, dry_run=dry_run)

        if ok:
            sent += 1
        else:
            failed += 1

        # Anti-ban delay
        if not dry_run and i < len(rows) - 1:
            logger.info(f"⏸️ Waiting {DELAY_BETWEEN_MESSAGES}s...")
            await asyncio.sleep(DELAY_BETWEEN_MESSAGES)

    logger.info(f"📊 Done: {sent} sent, {failed} failed out of {len(rows)}")


if __name__ == "__main__":
    asyncio.run(main())
