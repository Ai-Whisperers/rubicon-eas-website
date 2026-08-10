# Lead Capture API · Rubicón EAS

Production Cloudflare Worker for the static landing site. Captures inquiry forms, validates, formats, and forwards to a webhook (n8n → Evolution API → WhatsApp).

## Architecture

```
client (HTML)
   ↓ POST /api/lead
[CF Worker · rubicon-eas-lead]
   ↓ validate (name, phone, email, area, summary)
   ↓ format (markdown brief)
   ↓ log to KV (90 days)
   ↓ notify webhook (n8n)
[Webhook]
   ↓ POST /message/sendText
[Evolution API]
   ↓ wa.me → Partner's WhatsApp
```

## Endpoint

```
POST /api/lead
Content-Type: application/json

{
  "name": "Juan Pérez",
  "phone": "+595 981 234 567",
  "email": "juan@example.com",  // optional
  "area": "civil|penal|ambiental|otro",
  "summary": "...",
  "consent": true,
  "website": "..."  // honeypot — ignored if present
}
```

**Response 200 OK:**
```json
{
  "ok": true,
  "id": "lead:1723331234:abc123",
  "brief": "📋 Consulta\n\n*Lead desde web · Rubicón EAS*\n—...",
  "webhook": { "ok": true, "status": 200 },
  "priority": "URGENT|NORMAL",
  "instructions": "..."
}
```

**Response 400 (validation):**
```json
{ "error": "Validation failed", "fields": ["phone", "summary"] }
```

**Health check:**
```
GET /api/lead/health
→ { "ok": true, "name": "rubicon-eas-lead", "ts": "..." }
```

## Priority rules

- `area = "penal"` → `URGENT` (response <30 min SLA, partner's urgent line)
- otherwise → `NORMAL` (response <24h hábiles)

## Deploy

```bash
# 1. Create KV namespace
wrangler kv:namespace create LEADS
# → outputs ID, paste into wrangler.toml

# 2. Set webhook secret
wrangler secret put WEBHOOK_URL
# → paste n8n webhook URL

# 3. Deploy
wrangler deploy
```

## Local dev

```bash
# Use test variant (no KV, no webhook forwarding)
wrangler dev --local api/lead-worker.test.js
```

## Test

```bash
# Health
curl https://YOUR_DOMAIN/api/lead/health

# Submit
curl -X POST https://YOUR_DOMAIN/api/lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Test",
    "phone": "+595 981 234 567",
    "email": "juan@test.com",
    "area": "penal",
    "summary": "Necesito abogado penal urgente, me citaron para mañana.",
    "consent": true
  }'
```

## n8n workflow

```
Webhook:  POST /rubicon-eas-lead
Filter:   body.priority == "URGENT"
   ├─ yes → format Mensaje message → POST Evolution API /message/sendText to partner-urgent
   └─ no  → format Mensaje message → POST Evolution API /message/sendText to partner-main
```

**Webhook payload (matches `lead` shape):**
```json
{
  "name": "Juan Pérez",
  "phone": "+595 981 234 567",
  "email": "juan@example.com",
  "area": "civil",
  "summary": "...",
  "consent": true,
  "ts": "2026-08-10T22:30:00.000Z",
  "source": "rubiconeas.com.py",
  "brief": "...formatted..."
}
```

## Schema.org + consent

- All posts require `consent: true` (Ley 1682/01 compliance)
- Honeypot field `website` or `company_url` ignored (anti-bot)
- IP + User-Agent captured for abuse detection
- 90-day log retention in KV (consent-based, no auto-renewal)
- Client can request deletion via `/gestionar-datos` page
