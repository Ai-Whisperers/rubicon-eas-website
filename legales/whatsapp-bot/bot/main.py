"""
Ometz Dental — Bot v4 with appointment booking
================================================
Adds:
- /cita shows available slots for today
- /manana shows slots for tomorrow
- /lunes-5 shows slots for specific weekday
- Patient picks by number → creates appointment
- Confirmation message with details
- Update wa_appointments table
- Sync to Supabase
"""

import os
import json
import time
import asyncio
import logging
import subprocess
import httpx
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv("/root/ometsdental-bot/.env")

# === CONFIG ===
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "https://evolution.sunstein.cloud")
LOCATION_IMAGE_URL = os.getenv("LOCATION_IMAGE_URL", "https://admin.sunstein.cloud/static/img/placard.png")
LOCATION_TEXT = """📍 Ometz Dental
Auditores de la Guerra del Chaco 617
Barrio Mburucuyá, Asunción

Es una casa con rejas verdes. Toca timbre "Ometz Dental".

🕐 Lun-Vie 14:30-19:00

— Equipo Ometz Dental"""
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")
INSTANCE = os.getenv("EVOLUTION_INSTANCE", "ometsdental-business")
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "5"))

# Schedule
TIMEZONE_OFFSET = -4
SCHEDULE = {
    0: (14, 30, 19, 0), 1: (14, 30, 19, 0), 2: (14, 30, 19, 0),
    3: (14, 30, 19, 0), 4: (14, 30, 19, 0), 5: None, 6: None,
}
SLOT_DURATION_MINUTES = 60

# Postgres
PG_CONTAINER = "postgres_postgres.1.kpmo0dfqbz28pltocxlmtj8lu"
PG_USER = "postgres"
PG_DB = "ometsdental"

# Rate limiting
MAX_MESSAGES_PER_HOUR = 10

# Supabase mirror
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
SUPABASE_HEADERS = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
}

# === LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("ometsdental-bot-v4")


# === TIME UTILS ===
def now_asuncion():
    return datetime.now(timezone(timedelta(hours=TIMEZONE_OFFSET)))


def is_business_day(target_date):
    """Check if a date is a business day."""
    return target_date.weekday() < 5


def get_business_hours(target_date):
    """Return (open_dt, close_dt) for a given date."""
    weekday = target_date.weekday()
    schedule = SCHEDULE.get(weekday)
    if not schedule:
        return None
    open_h, open_m, close_h, close_m = schedule
    open_dt = target_date.replace(hour=open_h, minute=open_m, second=0, microsecond=0)
    close_dt = target_date.replace(hour=close_h, minute=close_m, second=0, microsecond=0)
    return open_dt, close_dt


def is_business_hours():
    now = now_asuncion()
    weekday = now.weekday()
    schedule = SCHEDULE.get(weekday)
    if not schedule:
        return False
    open_h, open_m, close_h, close_m = schedule
    open_time = now.replace(hour=open_h, minute=open_m, second=0, microsecond=0)
    close_time = now.replace(hour=close_h, minute=close_m, second=0, microsecond=0)
    return open_time <= now <= close_time


def hours_until_open():
    """Return human-readable time until next opening."""
    now = now_asuncion()
    weekday = now.weekday()
    weekday_names = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

    # If today is a business day and we're before opening
    if weekday < 5 and SCHEDULE.get(weekday):
        open_h, open_m, _, _ = SCHEDULE[weekday]
        open_today = now.replace(hour=open_h, minute=open_m, second=0, microsecond=0)
        if now < open_today:
            return f"hoy a las {open_h:02d}:{open_m:02d}"
    weekday_names = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    for i in range(1, 8):
        next_day = (weekday + i) % 7
        if next_day < 5 and SCHEDULE.get(next_day):
            return f"el {weekday_names[next_day]} a las 14:30"
    return "el lunes a las 14:30"


# === POSTGRES ===
def pg_query(sql: str, params: list = None) -> list:
    if params:
        args_str = []
        for p in params:
            if p is None:
                args_str.append("NULL")
            elif isinstance(p, (int, float)):
                args_str.append(str(p))
            elif isinstance(p, bool):
                args_str.append("TRUE" if p else "FALSE")
            else:
                escaped = str(p).replace("'", "''")
                args_str.append(f"'{escaped}'")
        sql = sql.replace("%s", "{}").format(*args_str)
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


def pg_exec(sql: str, params: list = None) -> bool:
    if params:
        args_str = []
        for p in params:
            if p is None:
                args_str.append("NULL")
            elif isinstance(p, (int, float)):
                args_str.append(str(p))
            elif isinstance(p, bool):
                args_str.append("TRUE" if p else "FALSE")
            else:
                escaped = str(p).replace("'", "''")
                args_str.append(f"'{escaped}'")
        sql = sql.replace("%s", "{}").format(*args_str)
    cmd = ["docker", "exec", PG_CONTAINER, "psql", "-U", PG_USER, "-d", PG_DB, "-c", sql]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if result.returncode != 0:
        logger.error(f"PG exec failed: {result.stderr}")
        return False
    return True


# === APPOINTMENT HELPERS ===
def get_slots_for_date(target_date) -> list:
    """Get available slots for a given date."""
    open_close = get_business_hours(target_date)
    if not open_close:
        return []
    open_dt, close_dt = open_close

    # Get existing appointments
    rows = pg_query("""
        SELECT scheduled_at FROM wa_appointments
        WHERE DATE(scheduled_at) = %s
          AND status NOT IN ('cancelled', 'no_show')
    """, [target_date.strftime("%Y-%m-%d")])

    booked = set()
    for row in rows:
        try:
            booked.add(row[0])
        except IndexError:
            pass

    # Generate slots
    slots = []
    current = open_dt
    while current < close_dt:
        slot_str = current.strftime("%H:%M")
        if slot_str not in booked:
            slots.append({
                "datetime": current,
                "time_str": slot_str,
                "available": True,
            })
        current += timedelta(minutes=SLOT_DURATION_MINUTES)

    # If target_date is today, mark past slots as unavailable
    if target_date.date() == now_asuncion().date():
        now = now_asuncion()
        for slot in slots:
            # Ensure slot datetime is timezone-aware
            if slot["datetime"].tzinfo is None:
                slot["datetime"] = slot["datetime"].replace(tzinfo=now.tzinfo)
            if slot["datetime"] <= now:
                slot["available"] = False

    return slots


def has_pending_appointment(phone: str) -> bool:
    """Check if patient has a pending appointment."""
    rows = pg_query("""
        SELECT id FROM wa_appointments
        WHERE phone = %s AND status IN ('scheduled', 'confirmed')
        LIMIT 1
    """, [phone])
    return len(rows) > 0


def create_appointment(phone: str, patient_name: str, scheduled_at: str, notes: str = "") -> int:
    """Create appointment. Returns appointment ID."""
    pg_exec("""
        INSERT INTO wa_appointments (phone, patient_name, scheduled_at, duration_minutes, status, notes, created_at, updated_at)
        VALUES (%s, %s, %s, 60, 'scheduled', %s, NOW(), NOW())
    """, [phone, patient_name, scheduled_at, notes])
    rows = pg_query("SELECT id FROM wa_appointments WHERE phone = %s ORDER BY id DESC LIMIT 1", [phone])
    if rows:
        return int(rows[0][0])
    return 0


# === QUICK REPLIES ===
QUICK_REPLIES = {
    "/hola": """¡Hola! 👋 Soy el asistente de Ometz Dental.

Gracias por escribir. Te respondo en breve.

¿Qué te gustaría hacer?
1 — Quiero planificar mi caso / rehabilitación oral
2 — Pedir una segunda opinión
3 — Consulta general / profilaxis
4 — Blanqueamiento / estética
5 — Hablar con la doctora directo
6 — Precios / planes de pago

— Equipo Ometz Dental""",

    "/precio": """Precios de referencia Ometz Dental:

CONSULTAS
- Consulta general: Gs 300.000-400.000
- Segunda opinión: Gs 450.000-600.000
- Plan de tratamiento: Gs 500.000-800.000

RESTAURACIONES
- Simple (1 superficie): Gs 350.000-450.000
- Compleja (2-3+ superficies): Gs 450.000-550.000

ESTÉTICA
- Blanqueamiento consultorio: consultar
- Carillas composite: consultar

Todos los precios se confirman después de la evaluación clínica.

Ubicación: Auditores de la Guerra del Chaco 617, Mburucuyá, Asunción
Horarios: Lun-Vie 14:30-19:00

— Equipo Ometz Dental""",

    "/direccion": "__IMAGE__",

    "/cita": """🎯 Agendar cita

Te paso los horarios disponibles. Escribí /cita o decime 'agendar' o 'turno' para ver.

— Equipo Ometz Dental""",

    "/horario": """🕐 Horario de atención:

Lunes a viernes: 14:30 a 19:00
Sábado y domingo: cerrado

Atención con cita previa. Respondo mensajes en horario de
consultorio y contesto lo antes posible.

— Equipo Ometz Dental""",

    "/segundaop": """Buena decisión. La segunda opinión en Ometz incluye:

✓ Consulta 45-60 minutos
✓ Examen clínico completo
✓ Revisión de tus radiografías previas
✓ Plan alternativo por escrito (entrega 2-3 días)

Costo: Gs 450.000 a 600.000.

¿Tenés un plan o presupuesto previo? Mandame foto o PDF.

— Equipo Ometz Dental""",

    "/pago": """Métodos de pago aceptados en Ometz Dental:

✓ Efectivo (Gs)
✓ Transferencia bancaria
✓ Bancard (POS)
✓ Pagopar (cuotas con tarjeta)

Para tratamientos mayores, planes de pago en 2-3 cuotas.

— Equipo Ometz Dental""",

    "/deriv": """Para ese tipo de tratamiento derivamos a un especialista de confianza de nuestra red.

Cuando coordines la cita, te paso el nombre y teléfono del especialista.

— Equipo Ometz Dental""",

    "/garantia": """Sobre garantía de tratamientos:

En Ometz Dental usamos materiales certificados de primera línea (3M, Ivoclar, GC).

Las restauraciones en resina tienen durabilidad esperada de 5-10 años. Si se fracturan dentro de los primeros 6 meses por defecto del material, la reparación es sin cargo.

Para coronas y PSI: garantía de 1 año por defecto de fabricación.

— Equipo Ometz Dental""",

    "/gracias": """Gracias por escribir a Ometz Dental. 🙏

Si te quedó alguna duda, escribime cuando quieras.

— Dra. Gaby""",

    "/urgencia": """🚨 URGENCIA DENTAL

Si tenés dolor fuerte, fractura, sangrado o hinchazón:

1. Llamame al +595 987 126 790 (Gaby directo)
2. O escribime "URGENCIA" acá y te respondo inmediatamente

— Dra. Gaby""",
}

# === SLOT FORMATTING ===
def format_slots_message(target_date, slots, max_show=6) -> str:
    """Generate available slots message."""
    now = now_asuncion()
    weekday_names = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    day_name = weekday_names[target_date.weekday()]
    date_str = target_date.strftime("%d/%m")
    available = [s for s in slots if s["available"]]

    if not available:
        return f"""📅 {day_name.title()} {date_str} — no quedan horarios disponibles ese día.

¿Querés que te muestre horarios de otro día? Decime:
- /manana — mañana
- /pasado — pasado mañana
- /lunes /martes etc.""".strip()

    lines = [f"📅 {day_name.title()} {date_str} — horarios disponibles:"]
    for i, slot in enumerate(available[:max_show], 1):
        lines.append(f"  {i} — {slot['time_str']}")

    if len(available) > max_show:
        lines.append(f"  ... y {len(available) - max_show} más")

    lines.append("")
    lines.append("Respondé con el NÚMERO del horario que querés.")
    lines.append("O decime /otro para ver otro día.")
    lines.append("")
    lines.append("— Equipo Ometz Dental")

    return "\n".join(lines)


def format_confirmation_message(appointment_id: int, day_name: str, day_num: str, time_str: str) -> str:
    """Send confirmation after patient picks a slot."""
    parts = [
        "✅ ¡Cita agendada!",
        "",
        f"📅 {day_name.title()} {day_num} a las {time_str} (60 min)",
        "📍 Auditores de la Guerra del Chaco 617, Mburucuyá",
        "",
        f"ID de tu cita: #{appointment_id}",
        "",
        "Te confirmamos el día anterior por WhatsApp.",
        "",
        "¿Tenés radiografías previas? Si sí, mandame foto o PDF.",
        "",
        "— Equipo Ometz Dental",
    ]
    return "\n".join(parts)


# === STATE MANAGEMENT ===
pending_slots = {}  # phone -> {date, datetime_formats, last_msg_id}


def get_user_pending(phone: str):
    return pending_slots.get(phone)


def set_user_pending(phone: str, target_date, slots):
    pending_slots[phone] = {
        "date": target_date.strftime("%Y-%m-%d"),
        "slots": [s["time_str"] for s in slots if s["available"]],
        "expires": (now_asuncion() + timedelta(minutes=10)).isoformat(),
    }


def clear_user_pending(phone: str):
    pending_slots.pop(phone, None)


# === COMMAND HANDLERS ===
def handle_cita(phone: str) -> str:
    """Show available slots for today."""
    # Check if patient already has an upcoming appointment
    existing = pg_query("""
        SELECT id, scheduled_at, status FROM wa_appointments
        WHERE phone = %s AND status IN ('scheduled', 'confirmed')
          AND scheduled_at > NOW()
        ORDER BY scheduled_at
        LIMIT 1
    """, [phone])

    if existing and len(existing[0]) >= 3:
        existing_id = existing[0][0]
        existing_time = existing[0][1]
        existing_status = existing[0][2]
        weekday_names = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        from datetime import datetime as _dt
        try:
            dt = _dt.fromisoformat(existing_time.replace("Z", "+00:00"))
            when = f"{weekday_names[dt.weekday()].title()} {dt.strftime('%d/%m')} a las {dt.strftime('%H:%M')}"
        except Exception:
            when = existing_time

        return f"""📋 Ya tenés una cita agendada:

🗓️ {when}
📊 Estado: {existing_status}
🆔 ID: #{existing_id}

¿Querés:
1 — Mantener esta cita
2 — Cancelar y agendar otra (decime /cancelar)
3 — Ver más detalles (/cita-info {existing_id})

— Equipo Ometz Dental"""

    today = now_asuncion()

    if not is_business_day(today):
        # Find next business day
        for i in range(1, 8):
            next_day = today + timedelta(days=i)
            if is_business_day(next_day):
                weekday_names = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
                return f"""📅 Hoy no atendemos (es fin de semana).

El próximo día disponible es {weekday_names[next_day.weekday()]} {next_day.strftime('%d/%m')}.

Respondé /cita pronto para ver los horarios de ese día."""

    slots = get_slots_for_date(today)
    set_user_pending(phone, today, slots)
    return format_slots_message(today, slots)


def handle_day_command(phone: str, day_offset: int) -> str:
    """Show slots for a day offset from today (1=tomorrow, 2=day after)."""
    target = now_asuncion() + timedelta(days=day_offset)
    if not is_business_day(target):
        # Find next business day after that
        for i in range(1, 8):
            candidate = target + timedelta(days=i)
            if is_business_day(candidate):
                target = candidate
                break
    slots = get_slots_for_date(target)
    set_user_pending(phone, target, slots)
    return format_slots_message(target, slots)


def handle_slot_pick(phone: str, user_response: str) -> str:
    """Handle patient picking a slot number or other commands during slot selection."""
    pending = get_user_pending(phone)
    if not pending:
        return "Escribí /cita para empezar."

    # Check if expired
    expires = datetime.fromisoformat(pending["expires"])
    if now_asuncion() > expires:
        clear_user_pending(phone)
        return "Tu selección expiró. Escribí /cita de nuevo."

    text = user_response.strip().lower()

    # Handle "otro" — show next day
    if text in ("/otro", "otro", "otro día", "otro dia", "siguiente", "next", "1 más", "mas"):
        target_date = datetime.fromisoformat(pending["date"])
        next_date = target_date + timedelta(days=1)
        # Skip weekends
        if not is_business_day(next_date):
            for i in range(1, 8):
                candidate = next_date + timedelta(days=i)
                if is_business_day(candidate):
                    next_date = candidate
                    break
        slots = get_slots_for_date(next_date)
        set_user_pending(phone, next_date, slots)
        return format_slots_message(next_date, slots)

    # Handle "atras" — show previous day
    if text in ("/atras", "atras", "anterior", "prev", "volver"):
        target_date = datetime.fromisoformat(pending["date"])
        prev_date = target_date - timedelta(days=1)
        if not is_business_day(prev_date):
            for i in range(1, 8):
                candidate = prev_date - timedelta(days=i)
                if is_business_day(candidate):
                    prev_date = candidate
                    break
        slots = get_slots_for_date(prev_date)
        set_user_pending(phone, prev_date, slots)
        return format_slots_message(prev_date, slots)

    # Handle cancel
    if text in ("/cancelar", "cancelar", "no", "salir", "exit"):
        clear_user_pending(phone)
        return "❌ Cancelado. Si querés empezar de nuevo, escribí /cita.\n\n— Equipo Ometz Dental"

    # Handle "hola" or "menu" — restart the slot picking
    if text in ("hola", "menu", "menú", "ayuda", "help", "/start"):
        target_date = datetime.fromisoformat(pending["date"])
        slots = get_slots_for_date(target_date)
        set_user_pending(phone, target_date, slots)
        return format_slots_message(target_date, slots)

    # Try to parse as number
    try:
        num = int(text)
    except ValueError:
        return "✋ Elegí un NÚMERO (1, 2, 3...) del 1 al 5.\n\n💡 Tip: /otro para ver mañana, /cancelar para salir."

    slots = pending["slots"]
    if num < 1 or num > len(slots):
        return f"Número inválido. Elegí entre 1 y {len(slots)}."

    chosen_time = slots[num - 1]
    target_date = datetime.fromisoformat(pending["date"])
    scheduled_at_db = f"{pending['date']} {chosen_time}:00"

    # Get name from contact
    name = "Paciente"
    rows = pg_query("SELECT name FROM wa_contacts WHERE phone = %s", [phone])
    if rows and rows[0][0]:
        name = rows[0][0]

    # Create appointment
    appt_id = create_appointment(phone, name, scheduled_at_db)

    # Clear pending
    clear_user_pending(phone)

    weekday_names = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    day_name = weekday_names[target_date.weekday()]
    day_num = target_date.strftime("%d/%m")

    return format_confirmation_message(appt_id, day_name, day_num, chosen_time)


# === KEYWORDS ===
KEYWORDS = {
    "hola": ["hola", "buenas", "buenos dias", "buenas tardes", "buenos días", "buenas tardes", "hi", "hello"],
    "precio": ["cuánto", "precio", "cuesta", "costo", "tarifa", "honorario", "vale"],
    "direccion": ["dirección", "direccion", "donde", "dónde", "cómo llegar", "como llegar", "ubicación", "ubicacion", "mapa"],
    "horario": ["horario", "hora", "abren", "abierto", "atenden", "cuándo"],
    "cita": ["agendar", "turno", "cita", "reservar", "coordinar"],
    "segundaop": ["segunda opinión", "segunda opinion", "no estoy seguro", "duda", "otra opinion"],
    "pago": ["pago", "transferencia", "efectivo", "tarjeta", "bancard", "pagopar", "cuotas"],
    "urgencia": ["dolor fuerte", "urgencia", "fractura", "hinchazón", "hinchazon", "sangrado", "no puedo dormir", "emergencia"],
}

DAY_COMMANDS = {
    "/manana": 1,
    "/pasado": 2,
    "/lunes": "monday",
    "/martes": "tuesday",
    "/miercoles": "wednesday",
    "/jueves": "thursday",
    "/viernes": "friday",
}

# === CANCEL COMMAND ===
def handle_cancelar(phone: str) -> str:
    """Cancel the patient's next upcoming appointment."""
    rows = pg_query("""
        SELECT id, scheduled_at FROM wa_appointments
        WHERE phone = %s AND status IN ('scheduled', 'confirmed')
          AND scheduled_at > NOW()
        ORDER BY scheduled_at
        LIMIT 1
    """, [phone])

    if not rows:
        return "No tenés citas agendadas para cancelar. ✋"

    appt_id = rows[0][0]
    appt_time = rows[0][1]

    pg_exec("""
        UPDATE wa_appointments SET status = 'cancelled', updated_at = NOW()
        WHERE id = %s
    """, [appt_id])

    return f"""✅ Cita #{appt_id} cancelada.

Si querés reagendar, escribí /cita.

— Equipo Ometz Dental"""

AWAY_MESSAGE = """⏰ Estamos fuera de horario de atención ahora mismo.

Te respondo {when} cuando abramos.

📍 Auditores de la Guerra del Chaco 617, Mburucuyá
🕐 Lun-Vie 14:30 a 19:00

⚠️ Si es una urgencia dental (dolor fuerte, fractura, hinchazón):
Llamame al +595 987 126 790 o escribime "URGENCIA" y te priorizo.

— Equipo Ometz Dental"""


def auto_respond(text: str, is_business: bool, phone: str) -> str:
    text_lower = text.lower().strip()

    # Check if user is picking a slot
    if pending_slots.get(phone):
        pending = pending_slots[phone]
        if datetime.fromisoformat(pending["expires"]) > now_asuncion():
            return handle_slot_pick(phone, text)

    # Handle numbered menu responses (1-6) without pending slots
    if text.strip() in ("1", "2", "3", "4", "5", "6"):
        n = int(text.strip())
        if n == 1:
            # Planificar caso / rehabilitación
            return """🦷 ¡Buena elección! Para planificar tu caso necesitamos una consulta inicial.

¿Querés agendar? Escribí /cita para ver horarios disponibles, o /precio para ver nuestros honorarios.

— Equipo Ometz Dental"""
        elif n == 2:
            # Segunda opinión
            return """🔍 Segunda opinión. La consulta incluye:
✓ Examen clínico completo (45-60 min)
✓ Revisión de tus radiografías
✓ Plan alternativo por escrito (entrega 2-3 días)

Costo: Gs 450.000 a 600.000.

¿Tenés un plan previo? Mandame foto o PDF. Y /cita para agendar.

— Equipo Ometz Dental"""
        elif n == 3:
            # Consulta general
            return """🦷 Consulta general con evaluación completa.

¿Querés ver precios primero? /precio
¿Querés agendar? /cita

— Equipo Ometz Dental"""
        elif n == 4:
            # Blanqueamiento
            return """✨ Blanqueamiento consultorio.

El precio depende del caso. Te pasamos el detalle en la consulta inicial.

¿Querés agendar? /cita

— Equipo Ometz Dental"""
        elif n == 5:
            # Hablar con la doctora
            return """👩‍⚕️ Hablar con la doctora directo.

Si tenés una urgencia: llamame al +595 987 126 790 o escribí "URGENCIA".

Para una consulta donde la doctora te atienda: /cita

— Equipo Ometz Dental"""
        elif n == 6:
            # Precios
            return QUICK_REPLIES["/precio"]

    # Cancel command
    if text_lower in ("/cancelar", "cancelar", "cancelar cita"):
        return handle_cancelar(phone)

    # Day commands
    if text_lower in DAY_COMMANDS:
        offset = DAY_COMMANDS[text_lower]
        if isinstance(offset, int):
            response = handle_day_command(phone, offset)
        else:
            # Specific weekday
            target = now_asuncion()
            days_ahead = 0
            for i in range(1, 8):
                candidate = target + timedelta(days=i)
                weekday_name = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"][candidate.weekday()]
                if offset in weekday_name:
                    days_ahead = i
                    break
            if days_ahead == 0:
                return "No encuentro ese día en la semana."
            target = target + timedelta(days=days_ahead)
            slots = get_slots_for_date(target)
            set_user_pending(phone, target, slots)
            response = format_slots_message(target, slots)
        return response

    # Handle media (audio, image, doc, video)
    if text in ("[AUDIO]", "[IMAGEN]", "[DOCUMENTO]", "[VIDEO]"):
        if text == "[AUDIO]":
            return """🎙️ Recibí tu audio, pero el bot no puede escuchar todavía.

Por favor escribime tu consulta en texto y te respondo al toque.

Si es una urgencia, llamame al +595 987 126 790.

— Equipo Ometz Dental"""
        elif text == "[IMAGEN]":
            return """📸 Recibí tu imagen. Si es una radiografía o foto clínica, ya la tengo guardada.

Decime qué necesitás (consulta, segunda opinión, agendar) y te respondo.

— Equipo Ometz Dental"""
        elif text == "[DOCUMENTO]":
            return """📄 Recibí tu documento (PDF, presupuesto, etc.).

Ya lo guardé. Decime qué necesitás y te respondo al toque.

— Equipo Ometz Dental"""
        elif text == "[VIDEO]":
            return """🎥 Recibí tu video. Lo guardé en el sistema.

Si querés que lo revise la doctora, decime. Para casos urgentes, llamame al +595 987 126 790.

— Equipo Ometz Dental"""

    # Quick replies
    chosen = None
    category = None
    if text_lower in QUICK_REPLIES:
        chosen = QUICK_REPLIES[text_lower]
        category = text_lower.split("/")[1] if "/" in text_lower else "default"

    if not chosen:
        for cat, kws in KEYWORDS.items():
            if any(kw in text_lower for kw in kws):
                key = f"/{cat}"
                if key in QUICK_REPLIES:
                    chosen = QUICK_REPLIES[key]
                    category = cat
                    break

    if not chosen:
        # Check for citation/appointment request
        if any(kw in text_lower for kw in ["disponible", "libre", "cupo", "horario para"]):
            return handle_cita(phone)

        if len(text) < 200 and any(c in text_lower for c in ["?", "¿"]):
            chosen = """¡Hola! 👋 Soy el asistente de Ometz Dental.

Gracias por escribir. Te respondo en breve.

¿Qué necesitás?
1 — Quiero planificar mi caso
2 — Pedir una segunda opinión
3 — Consulta general / profilaxis
4 — Hablar con la doctora

O usá los atajos:
- /precio
- /direccion
- /horario
- /cita  (agendar)
- /manana, /lunes, etc. (otro día)

— Equipo Ometz Dental"""
            category = "default"
        else:
            return None

    # Special handling for /cita (always show slots, not the template)
    if text_lower == "/cita":
        return handle_cita(phone)

    # Special handling for /direccion (send image with location)
    if text_lower == "/direccion":
        return "__SEND_LOCATION_IMAGE__"

    if not is_business:
        when = hours_until_open()
        away_prefix = AWAY_MESSAGE.format(when=when)
        return f"{away_prefix}\n\n{chosen}"

    return chosen


# === HELPER: MESSAGE STORAGE ===
def is_message_seen(msg_id: str) -> bool:
    rows = pg_query("SELECT 1 FROM wa_messages WHERE message_id = %s LIMIT 1", [msg_id])
    return len(rows) > 0


def save_message(phone: str, direction: str, text: str, msg_id: str = None,
                 category: str = None, priority: str = None, auto: bool = False) -> bool:
    ok = pg_exec("""
        INSERT INTO wa_messages (phone, direction, text, message_id, category, priority, auto, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """, [phone, direction, text, msg_id, category, priority, auto])
    if ok and SUPABASE_URL:
        asyncio.create_task(supabase_mirror({
            "phone": phone, "direction": direction, "text": text[:1000],
            "message_id": msg_id, "category": category, "priority": priority, "auto": auto,
        }))
    return ok


def upsert_contact(phone: str, pushname: str = None) -> bool:
    if not pushname:
        pushname = "Unknown"
    ok = pg_exec("""
        INSERT INTO wa_contacts (phone, name, first_message_at, last_message_at, total_messages, updated_at)
        VALUES (%s, %s, NOW(), NOW(), 0, NOW())
        ON CONFLICT (phone) DO UPDATE
        SET last_message_at = NOW(),
            total_messages = wa_contacts.total_messages + 1,
            updated_at = NOW()
    """, [phone, pushname])
    if ok and SUPABASE_URL:
        asyncio.create_task(supabase_mirror({
            "phone": phone, "name": pushname, "source": "whatsapp",
        }, "wa_contacts"))
    return ok


def get_recent_messages_count(phone: str) -> int:
    rows = pg_query("""
        SELECT COUNT(*) FROM wa_messages
        WHERE phone = %s AND direction = 'inbound'
          AND created_at > NOW() - INTERVAL '1 hour'
    """, [phone])
    if rows:
        return int(rows[0][0])
    return 0


async def supabase_mirror(payload: dict, table: str = "wa_messages"):
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        return
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            result = await client.post(
                f"{SUPABASE_URL}/rest/v1/{table}",
                headers=SUPABASE_HEADERS,
                json=payload,
            )
            if result.status_code >= 400:
                logger.debug(f"Supabase mirror failed ({table}): {result.status_code}")
    except Exception as e:
        logger.debug(f"Supabase mirror error: {e}")


# === EVOLUTION ===
async def get_recent_messages(client):
    payload = {"where": {"key": {"fromMe": False}}, "limit": 50}
    result = await client.post(
        f"{EVOLUTION_API_URL}/chat/findMessages/{INSTANCE}",
        headers={"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"},
        json=payload, timeout=30,
    )
    return result.json()


async def send_message(client, phone: str, text: str):
    result = await client.post(
        f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE}",
        headers={"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"},
        json={"number": phone, "text": text}, timeout=30,
    )
    return result.json()


def extract_phone(record):
    key = record.get("key", {})
    remote = key.get("remoteJid", "")
    remote_alt = key.get("remoteJidAlt", "")
    if remote_alt and "@s.whatsapp.net" in remote_alt:
        return remote_alt.split("@")[0]
    if remote and "@s.whatsapp.net" in remote:
        return remote.split("@")[0]
    if remote:
        return remote.split("@")[0]
    return None


async def main():
    logger.info("🦷 Ometz Dental bot v4 starting (with appointment booking)")
    logger.info(f"Evolution API: {EVOLUTION_API_URL}")
    logger.info(f"Instance: {INSTANCE}")
    logger.info(f"Postgres: {PG_DB}")
    logger.info(f"Poll interval: {POLL_INTERVAL_SECONDS}s")

    async with httpx.AsyncClient() as client:
        while True:
            try:
                data = await get_recent_messages(client)
                records = data.get("messages", {}).get("records", [])

                for record in records:
                    if record.get("key", {}).get("fromMe", False):
                        continue

                    msg_id = record.get("id")
                    if not msg_id or is_message_seen(msg_id):
                        continue

                    msg = record.get("message", {})
                    text = (
                        msg.get("conversation") or
                        msg.get("extendedTextMessage", {}).get("text") or
                        ""
                    ).strip()

                    # Detect voice notes / audio / images
                    has_audio = bool(msg.get("audioMessage") or msg.get("pttMessage"))
                    has_image = bool(msg.get("imageMessage") or msg.get("stickerMessage"))
                    has_document = bool(msg.get("documentMessage"))
                    has_video = bool(msg.get("videoMessage"))

                    if not text:
                        if has_audio:
                            text = "[AUDIO]"
                        elif has_image:
                            text = "[IMAGEN]"
                        elif has_document:
                            text = "[DOCUMENTO]"
                        elif has_video:
                            text = "[VIDEO]"
                        else:
                            continue

                    phone = extract_phone(record)
                    if not phone:
                        continue

                    pushname = record.get("pushName", "unknown")
                    logger.info(f"📩 {pushname} ({phone}): {text[:80]}")

                    save_message(phone, "inbound", text, msg_id)
                    upsert_contact(phone, pushname)

                    business_hours = is_business_hours()
                    response = auto_respond(text, business_hours, phone)

                    # Special: send image + text
                    if response == "__SEND_LOCATION_IMAGE__":
                        # Send the image
                        try:
                            img_result = await client.post(
                                f"{EVOLUTION_API_URL}/message/sendImage/{INSTANCE}",
                                headers={"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"},
                                json={
                                    "number": phone,
                                    "mediatype": "image",
                                    "media": LOCATION_IMAGE_URL,
                                    "caption": LOCATION_TEXT,
                                },
                                timeout=30,
                            )
                            save_message(phone, "outbound", LOCATION_TEXT, None, "direccion", "GENERAL", True)
                            logger.info(f"✅ → {phone}: sent location image ({img_result.status_code})")
                        except Exception as e:
                            logger.error(f"Failed to send image: {e}")
                            await send_message(client, phone, LOCATION_TEXT)

                    elif response:
                        priority = "URGENT" if "urgencia" in text.lower() else "GENERAL"
                        await send_message(client, phone, response)
                        save_message(phone, "outbound", response, None, "auto", priority, True)
                        logger.info(f"✅ → {phone}")
                    else:
                        save_message(phone, "outbound", "ESCALATION", msg_id, "UNKNOWN", "GENERAL", False)
                        logger.warning(f"🚨 ESCALATION: {phone} sent: {text[:100]}")

                        # Save to wa_escalations table for tracking
                        priority_level = "URGENT" if any(kw in text.lower() for kw in ["dolor fuerte", "urgencia", "fractura", "hinchazón"]) else "GENERAL"
                        category = "UNKNOWN"
                        pg_exec(
                            """INSERT INTO wa_escalations (phone, category, priority, original_message, original_message_id, status, created_at)
                               VALUES (%s, %s, %s, %s, %s, 'pending', NOW())""",
                            [phone, category, priority_level, text[:1000], msg_id]
                        )

            except Exception as e:
                logger.error(f"Error: {e}", exc_info=True)

            await asyncio.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())
