"""
Ometz Dental — Evolution API Webhook Handler
=============================================
Receives incoming WhatsApp messages from Evolution API, classifies them
using OpenAI (or rule-based fallback), and writes to Supabase CRM.

Stack:
- FastAPI (HTTP server)
- OpenAI (message classification)
- Supabase (CRM, conversations, appointments)
- Evolution API (responses)

Endpoints:
- POST /webhooks/evolution — receives Evolution API events
- GET  /health — health check
- POST /send — manual send (admin/debug)
- GET  /metrics — Prometheus metrics (optional)

Owner: Erebus (Hermes-AI)
Status: v1.0 — 27 jul 2026
"""

import os
import json
import logging
import hashlib
import hmac
from datetime import datetime, timezone
from typing import Optional, Literal
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
from supabase import create_client, Client

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ometsdental-webhook")

# === CONFIG ===
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://evolution-api:8080")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")
WEBHOOK_HMAC_SECRET = os.getenv("WEBHOOK_HMAC_SECRET", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "+595 987 126 790")

# === CLIENTS ===
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
supabase: Optional[Client] = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY) if SUPABASE_URL and SUPABASE_SERVICE_KEY else None

# === APP ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Ometz Dental webhook handler starting up")
    logger.info(f"Evolution API: {EVOLUTION_API_URL}")
    logger.info(f"Supabase: {SUPABASE_URL or 'NOT CONFIGURED'}")
    logger.info(f"OpenAI: {'configured' if openai_client else 'NOT CONFIGURED'}")
    yield
    logger.info("Ometz Dental webhook handler shutting down")

app = FastAPI(
    title="Ometz Dental WhatsApp Webhook",
    version="1.0.0",
    lifespan=lifespan,
)

# === MODELS ===
class ClassificationResult(BaseModel):
    category: Literal[
        "PRICING", "APPOINTMENT", "SECOND_OPINION", "LOCATION",
        "WORK_INQUIRY", "EXISTING_PATIENT", "REFERRAL",
        "URGENT", "SPAM", "COMPLAINT", "UNKNOWN"
    ]
    priority: Literal["URGENT", "HOT_LEAD", "APPOINTMENT", "PRICING", "GENERAL", "SPAM"]
    confidence: float = Field(ge=0.0, le=1.0)
    escalation_needed: bool
    escalation_target: Optional[str] = None
    suggested_response: str
    auto_respond: bool = True
    reasoning: str = ""

class EvolutionMessage(BaseModel):
    event: str = "MESSAGES_UPSERT"
    instance: str = "ometsdental-business"
    data: dict
    sender: Optional[str] = None
    server_url: Optional[str] = None
    apikey: Optional[str] = None

# === HELPERS ===
async def verify_hmac(request: Request, signature: str = Header(None, alias="X-Webhook-Signature")) -> bool:
    """Verify webhook signature from Evolution API."""
    if not WEBHOOK_HMAC_SECRET:
        return True  # Disabled
    if not signature:
        return False
    body = await request.body()
    expected = hmac.new(WEBHOOK_HMAC_SECRET.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


def extract_phone(jid: str) -> str:
    """Extract phone from WhatsApp JID: 595987126790@s.whatsapp.net → +595 987 126 790."""
    phone = jid.split("@")[0]
    if phone.startswith("595"):
        return f"+{phone[:3]} {phone[3:6]} {phone[6:9]} {phone[9:]}"
    return phone


async def classify_message(message: str) -> ClassificationResult:
    """Classify a WhatsApp message using OpenAI; fallback to rule-based."""

    if openai_client:
        try:
            response = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.2,
                max_tokens=400,
                messages=[
                    {
                        "role": "system",
                        "content": """Sos el clasificador de mensajes de Ometz Dental, una clínica dental en Asunción, Paraguay.

Tu único trabajo es leer un mensaje de WhatsApp y clasificarlo en UNA de estas categorías:

CATEGORIES:
- PRICING: pregunta sobre precios, costos, honorarios
- APPOINTMENT: quiere agendar un turno, coordinar cita
- SECOND_OPINION: quiere una segunda opinión odontológica
- LOCATION: pregunta dirección, cómo llegar, estacionamiento
- WORK_INQUIRY: preguntando por trabajo, empleo
- EXISTING_PATIENT: paciente existente con pregunta clínica
- REFERRAL: viene derivado por otro profesional
- URGENT: dolor fuerte, fractura, hinchazón, emergencia real
- SPAM: promotional, scam, no relacionado
- COMPLAINT: queja, insatisfecho, mal resultado
- UNKNOWN: no encaja en otras

PRIORITY:
- URGENT: dolor fuerte, fractura, emergencia. SLA 5 min
- HOT_LEAD: segunda opinión, paciente referido. SLA 30 min
- APPOINTMENT: quiere agendar. SLA 2 horas
- PRICING: solo pregunta precios. SLA 4 horas
- GENERAL: general. SLA 24 horas
- SPAM: no responder

AUTO_RESPOND: ¿podemos responder automáticamente con templates?
- true: para LOCATION, PRICING, GENERAL
- false: para URGENT, COMPLAINT, SECOND_OPINION (escalar a Gaby)

Respondé SOLO con JSON válido en este formato:
{
  "category": "...",
  "priority": "...",
  "confidence": 0.0-1.0,
  "escalation_needed": true/false,
  "escalation_target": "dra.gabi" or null,
  "suggested_response": "Mensaje corto en español a enviar",
  "auto_respond": true/false,
  "reasoning": "Razón breve de la clasificación"
}"""
                    },
                    {"role": "user", "content": message}
                ],
            )
            content = response.choices[0].message.content or "{}"
            content = content.strip()
            data = json.loads(content)
            return ClassificationResult(**data)
        except Exception as e:
            logger.error(f"OpenAI classification failed: {e}, falling back to rules")

    # Fallback: rule-based
    return rule_based_classify(message)


def rule_based_classify(message: str) -> ClassificationResult:
    """Simple rule-based classifier (Spanish keywords)."""
    msg = message.lower()

    # URGENT
    urgent_keywords = ["dolor fuerte", "urgencia", "fractura", "hinchazón", "sangrado", "no puedo dormir", "emergencia"]
    if any(k in msg for k in urgent_keywords):
        return ClassificationResult(
            category="URGENT",
            priority="URGENT",
            confidence=0.9,
            escalation_needed=True,
            escalation_target="dra.gabi",
            suggested_response="Entiendo. Por favor llamame al +595 987 126 790 o escribime 'URGENCIA' y te priorizo.",
            auto_respond=False,
            reasoning="Detectada palabra clave de emergencia"
        )

    # SPAM
    spam_keywords = ["promoción", "descuento", "ven y conoce", "sorteo", "gratis"]
    if any(k in msg for k in spam_keywords) and len(msg) < 50:
        return ClassificationResult(
            category="SPAM",
            priority="SPAM",
            confidence=0.7,
            escalation_needed=False,
            suggested_response="",
            auto_respond=False,
            reasoning="Mensaje publicitario"
        )

    # PRICING
    if any(k in msg for k in ["cuánto", "precio", "cuesta", "costo", "honorario", "tarifa"]):
        return ClassificationResult(
            category="PRICING",
            priority="PRICING",
            confidence=0.85,
            escalation_needed=False,
            suggested_response="""Precios de referencia Ometz Dental:

CONSULTAS
- Consulta general: Gs 300.000-400.000
- Segunda opinión: Gs 450.000-600.000

RESTAURACIONES
- Simple: Gs 350.000-450.000
- Compleja: Gs 450.000-550.000

Todos los precios se confirman después de la evaluación.

¿Querés agendar? Escribí /cita""",
            auto_respond=True,
            reasoning="Consulta de precios"
        )

    # APPOINTMENT
    if any(k in msg for k in ["agendar", "turno", "cita", "reservar", "coordinar", "horario"]):
        return ClassificationResult(
            category="APPOINTMENT",
            priority="APPOINTMENT",
            confidence=0.85,
            escalation_needed=False,
            suggested_response="""¡Perfecto! Para agendarte necesito:

1. Tu nombre completo
2. Qué te gustaría atender
3. Día y horario preferido (lun-vie 14:30-19:00)
4. Si tenés radiografías previas

Te confirmo el turno a la brevedad.""",
            auto_respond=True,
            reasoning="Quiere agendar"
        )

    # SECOND_OPINION
    if any(k in msg for k in ["segunda opinión", "segunda opinion", "no estoy seguro", "duda"]):
        return ClassificationResult(
            category="SECOND_OPINION",
            priority="HOT_LEAD",
            confidence=0.9,
            escalation_needed=True,
            escalation_target="dra.gabi",
            suggested_response="""Buena decisión. La segunda opinión en Ometz incluye:

✓ Consulta 45-60 minutos
✓ Examen clínico completo
✓ Revisión de tus radiografías
✓ Plan alternativo por escrito (entrega 2-3 días)

Costo: Gs 450.000 a 600.000.

¿Tenés un plan o presupuesto previo? Mandame foto o PDF.""",
            auto_respond=True,
            reasoning="Quiere segunda opinión"
        )

    # LOCATION
    if any(k in msg for k in ["dirección", "direccion", "donde", "cómo llegar", "mapa", "ubicación"]):
        return ClassificationResult(
            category="LOCATION",
            priority="GENERAL",
            confidence=0.95,
            escalation_needed=False,
            suggested_response="""📍 Ometz Dental
Auditores de la Guerra del Chaco 617
Barrio Mburucuyá, Asunción

Es una casa con rejas verdes. Toca timbre "Ometz Dental".

Lun-Vie 14:30-19:00""",
            auto_respond=True,
            reasoning="Pregunta dirección"
        )

    # REFERRAL
    if any(k in msg for k in ["me dijo", "me recomendó", "me mando", "derivad"]):
        return ClassificationResult(
            category="REFERRAL",
            priority="HOT_LEAD",
            confidence=0.85,
            escalation_needed=True,
            escalation_target="dra.gabi",
            suggested_response="""Qué bueno. ¿Quién te derivó? Si me decís el nombre lo registro en nuestro sistema.

Para coordinar la cita, contame brevemente qué te trajo al consultorio y qué tenés disponible esta semana.""",
            auto_respond=True,
            reasoning="Viene por derivación"
        )

    # DEFAULT
    return ClassificationResult(
        category="UNKNOWN",
        priority="GENERAL",
        confidence=0.3,
        escalation_needed=False,
        suggested_response="""¡Hola! 👋 Soy el asistente de Ometz Dental.

Gracias por escribir. Te respondo en breve.

Mientras tanto, decime:
1 — Quiero planificar mi caso
2 — Pedir una segunda opinión
3 — Consulta general
4 — Hablar con la doctora""",
        auto_respond=True,
        reasoning="Mensaje genérico"
    )


async def log_to_supabase(data: dict, table: str):
    """Log to Supabase if configured."""
    if not supabase:
        logger.debug(f"Supabase not configured, skipping log to {table}")
        return
    try:
        result = supabase.table(table).insert(data).execute()
        logger.info(f"Logged to {table}: {result}")
    except Exception as e:
        logger.error(f"Supabase log failed for {table}: {e}")


async def send_whatsapp_message(to_phone: str, message: str):
    """Send a message via Evolution API."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{EVOLUTION_API_URL}/message/sendText/ometsdental-business",
                headers={"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"},
                json={
                    "number": to_phone.replace("+", "").replace(" ", ""),
                    "text": message,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            logger.info(f"Sent message to {to_phone}: {response.json()}")
        except Exception as e:
            logger.error(f"Failed to send message to {to_phone}: {e}")


# === ENDPOINTS ===

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "ometsdental-webhook",
        "version": "1.0.0",
        "supabase": bool(supabase),
        "openai": bool(openai_client),
        "evolution_api": bool(EVOLUTION_API_KEY),
    }


@app.post("/webhooks/evolution")
async def evolution_webhook(request: Request, valid: bool = Depends(verify_hmac)):
    """Main webhook endpoint for Evolution API events."""
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    event = body.get("event", "")
    instance = body.get("instance", "")
    data = body.get("data", {})

    logger.info(f"Event: {event} | Instance: {instance}")

    # Handle MESSAGES_UPSERT (incoming messages)
    if event == "MESSAGES_UPSERT":
        await handle_message(data)
    # Handle CONNECTION_UPDATE
    elif event == "CONNECTION_UPDATE":
        await handle_connection_update(data)
    # Handle other events (log only)
    else:
        logger.debug(f"Unhandled event: {event}")

    return {"status": "ok"}


async def handle_message(data: dict):
    """Process an incoming WhatsApp message."""
    try:
        key = data.get("key", {})
        remote_jid = key.get("remoteJid", "")
        from_me = key.get("fromMe", False)
        message = data.get("message", {})
        message_text = (
            message.get("conversation") or
            message.get("extendedTextMessage", {}).get("text") or
            ""
        )

        # Skip: messages from us, group messages, status updates
        if from_me or not remote_jid or "@g.us" in remote_jid or "status@broadcast" in remote_jid:
            return

        phone = extract_phone(remote_jid)
        logger.info(f"Message from {phone}: {message_text[:100]}")

        # Classify
        classification = await classify_message(message_text)

        # Log to Supabase
        await log_to_supabase({
            "phone": phone,
            "direction": "inbound",
            "text": message_text,
            "category": classification.category,
            "priority": classification.priority,
            "confidence": classification.confidence,
            "escalation_needed": classification.escalation_needed,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }, "wa_messages")

        # Auto-respond
        if classification.auto_respond and classification.suggested_response:
            await send_whatsapp_message(phone, classification.suggested_response)
            await log_to_supabase({
                "phone": phone,
                "direction": "outbound",
                "text": classification.suggested_response,
                "category": classification.category,
                "priority": classification.priority,
                "auto": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }, "wa_messages")

        # Escalate if needed
        if classification.escalation_needed:
            await escalate_to_human(phone, classification, message_text)

    except Exception as e:
        logger.error(f"Error handling message: {e}", exc_info=True)


async def handle_connection_update(data: dict):
    """Track connection state changes."""
    state = data.get("state", "")
    logger.info(f"Connection state: {state}")
    await log_to_supabase({
        "event": "connection_update",
        "state": state,
        "instance": "ometsdental-business",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }, "wa_events")


async def escalate_to_human(phone: str, classification: ClassificationResult, original_message: str):
    """Notify Gaby via email or Slack for urgent messages."""
    # TODO: Send notification to Gaby
    # Options: email, Slack, Telegram bot
    logger.warning(
        f"ESCALATION: {phone} | {classification.category} | {classification.priority} | "
        f"target: {classification.escalation_target}"
    )

    # Log to Supabase for Kiki to review
    await log_to_supabase({
        "phone": phone,
        "category": classification.category,
        "priority": classification.priority,
        "escalation_target": classification.escalation_target,
        "original_message": original_message,
        "status": "pending_response",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }, "wa_escalations")


# === ADMIN ENDPOINTS ===

class SendMessageRequest(BaseModel):
    to: str
    message: str

@app.post("/send")
async def send_message(req: SendMessageRequest):
    """Manual send (admin/debug)."""
    if not req.to or not req.message:
        raise HTTPException(status_code=400, detail="Phone and message required")
    await send_whatsapp_message(req.to, req.message)
    return {"status": "sent", "to": req.to}


@app.post("/classify")
async def classify_endpoint(message: str):
    """Test the classifier without sending a message."""
    result = await classify_message(message)
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
