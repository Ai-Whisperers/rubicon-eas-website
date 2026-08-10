# Evolution API — Ometz Dental

Self-hosted WhatsApp Business API bridge para Ometz Dental.

## ¿Qué es?

Evolution API es un middleware que te da acceso programático a WhatsApp Business **sin pagar la API oficial de Meta**. Funciona escaneando el QR de WA Business desde el celular con el chip Tigo.

## Arquitectura

```
[Paciente envía WA]
        ↓
[Evolution API (Baileys)]
        ↓
[Webhook → Ometz Webhook Handler]
        ↓
[OpenAI clasifica mensaje]
        ↓
[Supabase CRM registra]
        ↓
[Auto-respuesta o escalación a Gaby]
```

## Componentes

- **`evolution-api-config.json`** — config completa de Evolution API
- **`evolution-api-deployment.md`** — guía de deployment paso a paso
- **`webhook-handler/`** — FastAPI server que procesa mensajes
  - `app.py` — lógica de clasificación
  - `Dockerfile` — imagen del container
  - `requirements.txt` — dependencias Python
- **`hermes_mcp_integration.py`** — wrapper para que Hermes interactúe
- **`SUPABASE-SCHEMA.sql`** — schema del CRM
- **`templates/responses/`** — 12 quick replies pre-armadas
- **`../../scripts/deploy-evolution-api.sh`** — script de deploy

## Quick start

```bash
# 1. Deploy
cd /root/dentist
bash scripts/deploy-evolution-api.sh

# 2. Aplicar schema a Supabase
# Ir a https://supabase.com/dashboard/project/_/sql
# Pegar SUPABASE-SCHEMA.sql
# Run

# 3. Gaby escanea el QR
# WA Business → Ajustes → Herramientas para la empresa → Más herramientas → WhatsApp Business API
# Escanear el QR de Evolution API

# 4. Test
# Mandar un mensaje a +595 987 126 790 desde otro celular

# 5. Verificar
curl -f http://localhost:8080/health
```

## Variables de entorno requeridas

```bash
EVOLUTION_API_KEY=<openssl rand -hex 32>
JWT_SECRET=<openssl rand -hex 32>
WEBHOOK_HMAC_SECRET=<openssl rand -hex 32>
REDIS_PASSWORD=<openssl rand -hex 32>
POSTGRES_PASSWORD=<openssl rand -hex 32>
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGc...
OPENAI_API_KEY=sk-...
```

## Cost

- **Self-hosted Evolution API:** $0
- **Meta WhatsApp Business API oficial:** ~$0.05/msj
- **VPS:** $5-20/mes (si ya tenés uno, gratis)
- **OpenAI API:** ~$0.001/mensaje (clasificación)
- **Supabase (free tier):** $0

**Total: $0/mes para 500-1000 mensajes/día.**

## Cost de NO usar Evolution API

Si seguimos sin esto:
- ❌ Gaby responde manualmente cada WA (interrumpe atención)
- ❌ No hay datos de leads/conversion
- ❌ No hay auto-respuestas
- ❌ No hay métricas
- ❌ No hay escalación inteligente

## Comparación con otros approaches

| Approach | Cost | Complex | Mantenimiento | Features |
|---|---|---|---|---|
| **Evolution API** (este) | $0 | Media | Media | Full features, self-hosted |
| **WPPConnect** | $0 | Media | Media | Similar a Evolution |
| **Baileys directo** | $0 | Alta | Alta | Solo dev |
| **Meta Oficiail** | $0.05/msj | Baja | Baja | Solo conversational API |
| **Twilio** | $0.05/msj | Baja | Baja | Cloud |
| **360dialog** | $0.04/msj | Baja | Media | Cloud |

## Documentación oficial

- [Evolution API](https://github.com/EvolutionAPI/evolution-api)
- [Baileys](https://github.com/whiskeysockets/baileys)
- [Supabase Python](https://supabase.com/docs/reference/python)
- [OpenAI Chat Completions](https://platform.openai.com/docs/api-reference/chat)

## Owner

Erebus (Hermes-AI) — 27 jul 2026
