"""
Ometz Dental — Admin Dashboard Backend
========================================
FastAPI backend for the admin dashboard.

Endpoints:
- GET  /api/appointments?date=YYYY-MM-DD — list appointments
- GET  /api/appointments/week?start=YYYY-MM-DD — weekly view
- POST /api/appointments — create appointment
- PATCH /api/appointments/{id} — update status
- DELETE /api/appointments/{id} — cancel
- GET  /api/contacts — list contacts
- GET  /api/messages?phone=X — get conversation history
- GET  /api/metrics — dashboard metrics
- GET  /api/calendar/today — calendar info for today
- GET  /api/calendar/upcoming — upcoming appointments
- GET  / — static dashboard HTML
"""

import os
import subprocess
import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import httpx

# === CONFIG ===
PG_CONTAINER = "postgres_postgres.1.kpmo0dfqbz28pltocxlmtj8lu"
PG_USER = "postgres"
PG_DB = "ometsdental"
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "https://evolution.sunstein.cloud")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")
INSTANCE = os.getenv("EVOLUTION_INSTANCE", "ometsdental-business")

# Scheduler
SCHEDULE = {
    0: (14, 30, 19, 0), 1: (14, 30, 19, 0), 2: (14, 30, 19, 0),
    3: (14, 30, 19, 0), 4: (14, 30, 19, 0), 5: None, 6: None,
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ometsdental-backend")


# === TIME UTILS ===
def now_asuncion():
    return datetime.now(timezone(timedelta(hours=-4)))


# === DB ===
import psycopg2
from psycopg2.extras import RealDictCursor

# Connection pool
PG_POOL = None

def _get_connection():
    global PG_POOL
    if PG_POOL is None or PG_POOL.closed:
        PG_POOL = psycopg2.connect(
            host=os.getenv("PG_HOST", "postgres"),
            port=int(os.getenv("PG_PORT", "5432")),
            user=os.getenv("PG_USER", "postgres"),
            password=os.getenv("PG_PASSWORD", "2c9a91153a5312dbe0ad9398cceccb4c"),
            database=os.getenv("PG_DB", "ometsdental"),
            cursor_factory=RealDictCursor,
        )
    return PG_POOL


def pg_query(sql, params=None):
    try:
        conn = _get_connection()
        cur = conn.cursor()
        cur.execute(sql, params or [])
        if cur.description:
            columns = [d[0] for d in cur.description]
            rows = cur.fetchall()
            return [list(row.values()) for row in rows]
        return []
    except Exception as e:
        logger.error(f"PG query failed: {e}")
        return []


def pg_exec(sql, params=None):
    try:
        conn = _get_connection()
        cur = conn.cursor()
        cur.execute(sql, params or [])
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"PG exec failed: {e}")
        return False


# === MODELS ===
class AppointmentCreate(BaseModel):
    phone: str
    patient_name: str
    scheduled_at: str  # ISO format
    duration_minutes: int = 60
    service: Optional[str] = None
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    scheduled_at: Optional[str] = None
    service: Optional[str] = None


# === APP ===
app = FastAPI(title="Ometz Dental Admin", version="1.0.0")

# Static files (images, CSS, etc.)
STATIC_DIR = os.getenv("STATIC_DIR", "/app/static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# === ROUTES ===
@app.get("/api/appointments")
async def list_appointments(
    date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """List appointments. Filter by date or range."""
    if date:
        rows = pg_query("""
            SELECT id, phone, patient_name, scheduled_at, duration_minutes, status, notes, service, created_at
            FROM wa_appointments
            WHERE DATE(scheduled_at AT TIME ZONE 'America/Asuncion') = %s
            ORDER BY scheduled_at
        """, [date])
    elif start and end:
        rows = pg_query("""
            SELECT id, phone, patient_name, scheduled_at, duration_minutes, status, notes, service, created_at
            FROM wa_appointments
            WHERE DATE(scheduled_at AT TIME ZONE 'America/Asuncion') BETWEEN %s AND %s
            ORDER BY scheduled_at
        """, [start, end])
    else:
        rows = pg_query("""
            SELECT id, phone, patient_name, scheduled_at, duration_minutes, status, notes, service, created_at
            FROM wa_appointments
            WHERE scheduled_at > NOW() - INTERVAL '7 days'
            ORDER BY scheduled_at
        """)

    if status:
        rows = [r for r in rows if len(r) > 5 and r[5] == status]

    appointments = []
    for row in rows:
        if len(row) < 9:
            continue
        appointments.append({
            "id": int(row[0]),
            "phone": row[1],
            "patient_name": row[2],
            "scheduled_at": row[3],
            "duration_minutes": int(row[4]) if row[4] else 60,
            "status": row[5],
            "notes": row[6],
            "service": row[7],
            "created_at": row[8],
        })
    return appointments


@app.post("/api/appointments")
async def create_appointment(appt: AppointmentCreate):
    """Create a new appointment."""
    ok = pg_exec("""
        INSERT INTO wa_appointments (phone, patient_name, scheduled_at, duration_minutes, service, notes, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, 'scheduled', NOW(), NOW())
    """, [appt.phone, appt.patient_name, appt.scheduled_at, appt.duration_minutes, appt.service, appt.notes])
    if not ok:
        raise HTTPException(status_code=500, detail="Failed to create appointment")
    return {"status": "ok", "message": "Appointment created"}


@app.patch("/api/appointments/{appt_id}")
async def update_appointment(appt_id: int, update: AppointmentUpdate):
    """Update appointment."""
    sets = []
    params = []
    if update.status:
        sets.append("status = %s")
        params.append(update.status)
        if update.status == "attended":
            sets.append("attended_at = NOW()")
    if update.notes is not None:
        sets.append("notes = %s")
        params.append(update.notes)
    if update.scheduled_at:
        sets.append("scheduled_at = %s")
        params.append(update.scheduled_at)
    if update.service:
        sets.append("service = %s")
        params.append(update.service)
    sets.append("updated_at = NOW()")

    if not sets:
        raise HTTPException(status_code=400, detail="No fields to update")

    params.append(appt_id)
    sql = f"UPDATE wa_appointments SET {', '.join(sets)} WHERE id = %s"
    ok = pg_exec(sql, params)
    if not ok:
        raise HTTPException(status_code=500, detail="Failed to update")
    return {"status": "ok"}


@app.delete("/api/appointments/{appt_id}")
async def delete_appointment(appt_id: int):
    """Cancel appointment."""
    ok = pg_exec("""
        UPDATE wa_appointments SET status = 'cancelled', updated_at = NOW() WHERE id = %s
    """, [appt_id])
    if not ok:
        raise HTTPException(status_code=500, detail="Failed")
    return {"status": "ok"}


@app.get("/api/contacts")
async def list_contacts(limit: int = 50):
    """List contacts."""
    rows = pg_query("""
        SELECT phone, name, total_messages, last_message_at, is_existing_patient, last_classification
        FROM wa_contacts
        ORDER BY last_message_at DESC NULLS LAST
        LIMIT %s
    """, [limit])
    contacts = []
    for row in rows:
        if len(row) < 6:
            continue
        contacts.append({
            "phone": row[0],
            "name": row[1],
            "total_messages": int(row[2]) if row[2] else 0,
            "last_message_at": row[3],
            "is_existing_patient": row[4] == "t",
            "last_classification": row[5],
        })
    return contacts


@app.get("/api/messages")
async def get_messages(phone: str = Query(...), limit: int = 50):
    """Get conversation history with a phone."""
    rows = pg_query("""
        SELECT direction, text, category, priority, created_at
        FROM wa_messages
        WHERE phone = %s
        ORDER BY created_at DESC
        LIMIT %s
    """, [phone, limit])
    messages = []
    for row in rows:
        if len(row) < 5:
            continue
        messages.append({
            "direction": row[0],
            "text": row[1],
            "category": row[2],
            "priority": row[3],
            "created_at": row[4],
        })
    return list(reversed(messages))


@app.get("/api/metrics")
async def get_metrics():
    """Dashboard metrics."""
    # Total messages today
    rows = pg_query("""
        SELECT COUNT(*) FROM wa_messages
        WHERE created_at > NOW() - INTERVAL '24 hours'
    """)
    total_messages_24h = int(rows[0][0]) if rows else 0

    # Inbound today
    rows = pg_query("""
        SELECT COUNT(*) FROM wa_messages
        WHERE direction = 'inbound' AND created_at > NOW() - INTERVAL '24 hours'
    """)
    inbound_24h = int(rows[0][0]) if rows else 0

    # Outbound today
    rows = pg_query("""
        SELECT COUNT(*) FROM wa_messages
        WHERE direction = 'outbound' AND created_at > NOW() - INTERVAL '24 hours'
    """)
    outbound_24h = int(rows[0][0]) if rows else 0

    # Unique contacts
    rows = pg_query("""
        SELECT COUNT(DISTINCT phone) FROM wa_messages
        WHERE created_at > NOW() - INTERVAL '24 hours'
    """)
    unique_contacts_24h = int(rows[0][0]) if rows else 0

    # Today's appointments
    today = now_asuncion().strftime("%Y-%m-%d")
    rows = pg_query("""
        SELECT COUNT(*) FROM wa_appointments
        WHERE DATE(scheduled_at AT TIME ZONE 'America/Asuncion') = %s
    """, [today])
    appointments_today = int(rows[0][0]) if rows else 0

    # Pending escalations
    rows = pg_query("""
        SELECT COUNT(*) FROM wa_escalations
        WHERE status = 'pending'
    """)
    pending_escalations = int(rows[0][0]) if rows else 0

    return {
        "messages_24h": total_messages_24h,
        "inbound_24h": inbound_24h,
        "outbound_24h": outbound_24h,
        "unique_contacts_24h": unique_contacts_24h,
        "appointments_today": appointments_today,
        "pending_escalations": pending_escalations,
    }


@app.get("/api/calendar/today")
async def calendar_today():
    """Today's schedule and appointments."""
    today = now_asuncion().strftime("%Y-%m-%d")
    weekday = now_asuncion().weekday()
    weekday_names = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

    is_business = weekday < 5
    schedule = SCHEDULE.get(weekday) if is_business else None

    appointments = await list_appointments(date=today)

    return {
        "date": today,
        "weekday": weekday_names[weekday],
        "is_business_day": is_business,
        "schedule": f"{schedule[0]:02d}:{schedule[1]:02d}-{schedule[2]:02d}:{schedule[3]:02d}" if schedule else None,
        "appointments_count": len(appointments),
        "appointments": appointments,
    }


@app.get("/api/calendar/upcoming")
async def calendar_upcoming(limit: int = 10):
    """Upcoming appointments."""
    rows = pg_query("""
        SELECT id, phone, patient_name, scheduled_at, status, service, notes
        FROM wa_appointments
        WHERE scheduled_at > NOW() AND status IN ('scheduled', 'confirmed')
        ORDER BY scheduled_at
        LIMIT %s
    """, [limit])
    appointments = []
    for row in rows:
        if len(row) < 7:
            continue
        appointments.append({
            "id": int(row[0]),
            "phone": row[1],
            "patient_name": row[2],
            "scheduled_at": row[3],
            "status": row[4],
            "service": row[5],
            "notes": row[6],
        })
    return appointments


@app.get("/api/slots")
async def get_slots(date: str = Query(...)):
    """Get available slots for a date."""
    target = datetime.fromisoformat(date)
    if target.tzinfo is None:
        target = target.replace(tzinfo=timezone(timedelta(hours=-4)))

    weekday = target.weekday()
    schedule = SCHEDULE.get(weekday)
    if not schedule:
        return []

    open_dt = target.replace(hour=schedule[0], minute=schedule[1], second=0, microsecond=0)
    close_dt = target.replace(hour=schedule[2], minute=schedule[3], second=0, microsecond=0)

    # Get booked
    rows = pg_query("""
        SELECT scheduled_at FROM wa_appointments
        WHERE DATE(scheduled_at AT TIME ZONE 'America/Asuncion') = %s
          AND status NOT IN ('cancelled', 'no_show')
    """, [date])

    booked = set()
    for row in rows:
        if row[0]:
            try:
                dt = datetime.fromisoformat(row[0].replace("Z", "+00:00"))
                booked.add(dt.strftime("%H:%M"))
            except Exception:
                pass

    slots = []
    current = open_dt
    while current < close_dt:
        time_str = current.strftime("%H:%M")
        slots.append({
            "time": time_str,
            "datetime": current.isoformat(),
            "available": time_str not in booked,
        })
        current += timedelta(hours=1)

    return slots


# === STATIC DASHBOARD ===
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard HTML."""
    # Use env var for static dir to work both locally and in container
    static_dir = Path(os.getenv("STATIC_DIR", "/app/static"))
    html_file = static_dir / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    return HTMLResponse("<h1>Dashboard not yet built</h1>")


# === HOOK TO BOT ===
@app.post("/api/notify/new-appointment")
async def notify_new_appointment(appt_id: int):
    """Send WhatsApp confirmation to patient."""
    rows = pg_query("SELECT phone, patient_name, scheduled_at FROM wa_appointments WHERE id = %s", [appt_id])
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    phone, name, scheduled_at = rows[0]

    weekday_names = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    dt = datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
    day_name = weekday_names[dt.weekday()]

    msg = f"""✅ ¡Cita agendada!

📅 {day_name.title()} {dt.strftime('%d/%m')}
🕐 {dt.strftime('%H:%M')} (60 minutos)
📍 Auditores de la Guerra del Chaco 617, Mburucuyá

ID: #{appt_id}

Te confirmamos el día anterior por WhatsApp.

— Equipo Ometz Dental"""

    async with httpx.AsyncClient() as client:
        result = await client.post(
            f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE}",
            headers={"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"},
            json={"number": phone, "text": msg},
            timeout=30,
        )
    return {"status": "sent", "response": result.json()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
