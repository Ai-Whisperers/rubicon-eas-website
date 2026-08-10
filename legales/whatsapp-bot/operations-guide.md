# WHATSAPP OPERATIONS — HERMES AGENT MANAGEMENT

> **PRICING CROSS-REFERENCE:** Agent pricing responses are governed by `00_STRATEGIC/financial-pricing/canonical-pricing-reference-v2.md`. Agent never quotes loyalty/generated prices.
**Version:** 1.0 — June 2026
**Purpose:** Complete operational blueprint for Hermes agents managing WhatsApp channel

---

## ARCHITECTURE OVERVIEW

```
[Patient sends WhatsApp]
         ↓
[WhatsApp Business API / Screen scrape]
         ↓
[Hermes Agent reads message]
         ↓
[Agent classifies → responds per flow]
         ↓
[Actions logged to CRM + pipeline]
         ↓
[Escalation to Dra. GP if needed]
```

**Two modes:**
- **Automation Mode (Day 1-30):** Hermes handles all first responses, schedules, basic info. Dra. GP handles clinical conversations and treatment discussions.
- **Supervised Mode (Day 30+):** Based on volume and Dra. GP's preference.

---

## WHATSAPP CHANNEL SETUP

### Option A: WhatsApp Business API (Recommended for Scale)
**What it needs:**
- WhatsApp Business Platform account (business.whatsapp.com)
- Meta Business account
- Hermes MCP server connection to WhatsApp API
- Phone number dedicated to business (new SIM or eSIM)

**Capabilities:**
- Read all incoming messages
- Send messages via API
- Automated responses via rules
- Integration with CRM
- Broadcast messages (up to 256 contacts)

### Option B: WhatsApp Web + Hermes Monitoring (Launch)
**What it needs:**
- WhatsApp Business app on phone/PC
- Hermes agent monitors via screen scraping or notification
- Manual send by Dra. GP or Hermes voice/third-party tool

**Capabilities:**
- Read messages (polling or notifications)
- Send templates (via Hermes → Dra. GP approval → send)
- Basic automation rules

### Option C: himalaya / CLI tool (Terminal-based)
**What it needs:**
- WhatsApp session via web.whatsapp.com
- himalaya CLI configured for WhatsApp
- Hermes agent runs himalaya commands

**Capabilities:**
- Read message history
- Send templated messages
- Search conversations

---

## MESSAGE CLASSIFICATION

Every incoming message is classified into one of these types:

| Type | Code | Agent Behavior | Escalation |
|------|------|---------------|-----------|
| Pricing inquiry | `PRICING` | Auto-reply with pricing card | Never (unless clinical) |
| Appointment request | `APPOINTMENT` | Collect info, propose times | Never (agent schedules) |
| Second opinion request | `SECOND_OPINION` | Auto-reply, mark as hot lead | Always → Dra. GP |
| Location/directions | `LOCATION` | Auto-reply with address | Never |
| Work inquiry / employment | `WORK` | Auto-reply with "not hiring" | Never |
| Existing patient question | `EXISTING_PATIENT` | Check CRM, respond or escalate | If clinical question |
| Referral mentioned | `REFERRAL` | Auto-reply, log in CRM | If new lead → Dra. GP |
| Urgent dental problem | `URGENT` | Respond immediately, escalate | Always → Dra. GP immediately |
| Spam / nonsense | `SPAM` | Block / ignore | Never |
| Complaint | `COMPLAINT` | Acknowledge, escalate | Always → Dra. GP |
| Unknown | `UNKNOWN` | Polite clarification request | If repeated → Dra. GP |

---

## PRIORITY LEVELS

| Priority | Response SLA | Description |
|----------|-------------|-------------|
| **URGENT** | < 5 minutes | Pain, bleeding, emergency |
| **HOT_LEAD** | < 30 minutes | Second opinion, high-value inquiry |
| **APPOINTMENT** | < 2 hours | Wants to book |
| **PRICING** | < 4 hours | Just asking prices |
| **GENERAL** | < 24 hours | Non-pressing question |
| **SPAM** | No response | Block sender |

---

## AUTOMATED RESPONSE FLOW (Day 1 Mode)

### FLOW A: PRICING INQUIRY
```
User → "Hola cuánto cuesta una restauración"
↓
Agent recognizes: PRICING
↓
Agent checks: Is this a known patient? (CRM lookup)
  → If yes: skip pricing, offer appointment
  → If no: continue
↓
Agent sends pricing card (auto):
"Hola! Gracias por escribir. Te paso precios como referencia:

• Restauración simple: Gs 350-450k
• Restauración compleja: Gs 450-550k  
• Second Opinion: Gs 400-600k
• Consulta general: Gs 300-400k
• Limpieza: Gs 150-250k

El precio final depende del caso — se confirma después de la evaluación.

Querés agendar? Escribí tu nombre y te mando horarios disponibles."
↓
Agent logs: NEW CONTACT → PRICING INQUIRY → CRM
↓
Agent waits for reply
  → If books: → FLOW B (Appointment)
  → If asks more: → Agent answers or escalates
  → If goes silent: → Follow-up in 48h (auto)
```

### FLOW B: APPOINTMENT REQUEST
```
User → "Quiero agendar una consulta"
↓
Agent recognizes: APPOINTMENT
↓
Agent sends:
"Perfecto! Para coordinar necesito:

1. Tu nombre completo
2. Qué te trae: ¿primera vez, segunda opinión, o algo específico?
3. Tenés radiografías o diagnósticos previos?

Mientras, te paso los horarios disponibles esta semana:

[Agent inserts available slots based on calendar]

Respondé y confirmás el que te sirva."
↓
Agent logs: NEW LEAD → APPOINTMENT REQUESTED → CRM
↓
User picks time
↓
Agent confirms:
"Confirmado! [DÍA] a las [HORA] en [DIRECCIÓN].

IMPORTANTE:
• Traé radiografías si tenés
• Llegá 10 min antes
• El turno incluye evaluación completa

Si necesitás cancelar: avisame 24h antes por favor.

Nos vemos!"
↓
Agent updates CRM: APPOINTMENT SCHEDULED → [DATE/TIME]
↓
[24h before: Agent sends reminder auto]
```

### FLOW C: SECOND OPINION REQUEST
```
User → "Me dijeron que necesito un crown pero no estoy seguro"
↓
Agent recognizes: SECOND_OPINION → HOT_LEAD
↓
Agent sends (high priority response, < 30 min):
"Hola! Entiendo perfectamente — buscar una segunda opinión antes de aceptar un tratamiento es una muy buena decisión.

Para darte una evaluación real necesito:
1. Qué te dijeron exactamente que necesitás
2. Si tenés radiografías — las puedo revisar
3. Desde cuándo te dijeron esto

La consulta de segunda opinión cuesta entre Gs 400-600k dependiendo de la complejidad. Incluye examen completo + opinión por escrito.

Te paso horarios disponibles:

[Available slots]

Querés que agendemos?"
↓
Agent logs: HOT LEAD → SECOND OPINION REQUEST → CRM
↓
Agent escalates to Dra. GP (auto-notify):
"[ALERT] Second opinion request from [NAME]. [MESSAGE]. Wants to book. Lead score: HIGH. Assigned to: Dra. GP review."
↓
Agent waits
  → If books: normal appointment flow
  → If Dra. GP wants to personally respond: she does
```

### FLOW D: EXISTING PATIENT
```
User → "Hola Dra., tengo dolor en el diente que me trataste hace una semana"
↓
Agent recognizes: EXISTING_PATIENT
↓
Agent checks CRM: Is this person a treated patient?
  → If yes: Look up last appointment, treatment, notes
  → If no: Classify as UNKNOWN, ask clarifying questions
↓
If treated patient:
Agent sends:
"Hola [NOMBRE]! Lamento que estés con dolor. Revisando tu caso — [FICHA]. 

¿Podés describirme qué estás sintiendo? 
• ¿Dolor constante o solo al comer?
• ¿Sensibilidad al frío/calor?
• ¿Algo visual que notes en el diente?

Mientras me decís, te paso el número de urgencia por si necesitás atención inmediata: [NÚMERO]"
↓
Agent alerts Dra. GP:
"[ALERT] Existing patient [NAME] reporting pain after treatment [DATE]. Needs review. Message: [EXCERPT]"
↓
Dra. GP reviews → responds personally or delegates
```

### FLOW E: REFERRAL MENTIONED
```
User → "Me recomendó la Dra. María [last name] — me dijo que te contacte"
↓
Agent recognizes: REFERRAL + (looks up referrer in CRM)
↓
Agent checks: Is [Dra. María] in CRM as a referrer?
  → If yes: Log as referral from [NAME]
  → If no: Ask for clarification, possible cold lead
↓
Agent sends:
"Qué bueno! [REFERRED_BY] es una colega que respeto mucho — si ella te recomendó, estás en buenas manos.

Te cuento cómo funciona: [BRIEF EXPLANATION OF PROCESS]. 

Para agendar, necesito tu nombre y qué te trae. Mientras, te paso los horarios disponibles: [SLOTS]."
↓
Agent logs: NEW LEAD → REFERRED BY [NAME] → CRM
```

### FLOW F: URGENT DENTAL PROBLEM
```
User → "Tengo un dolor muy fuerte y no puedo dormir"
↓
Agent recognizes: URGENT → PRIORITY 1
↓
Agent immediately (no delay):
"Entiendo. Doy优先idad a tu mensaje."

[Alert Dra. GP: URGENT - severe pain - response required NOW]
↓
Agent sends:
"Por favor llamá ahora mismo al [NÚMERO DE EMERGENCIA] — es el número directo para urgencias.

Si no podés llamar, escribíme qué estás sintiendo y te ayudo a evaluar."
↓
Agent stays active — awaits response
```

### FLOW G: COMPLAINT
```
User → "No estoy conforme con el resultado del tratamiento"
↓
Agent recognizes: COMPLAINT
↓
Agent does NOT try to solve — always escalates
↓
Agent sends (calm, acknowledging):
"Gracias por escribir. Entiendo que no estás satisfecho/da y eso es importante para mí. Voy a revisar tu caso personalmente y te respondo con atención."

[Alert Dra. GP: COMPLAINT from [NAME] - [SUMMARY] - requires personal response]
↓
Agent logs: COMPLAINT → ESCALATED → CRM
↓
Dra. GP responds personally within 2 hours
```

---

## OUTBOUND MESSAGES (Agent-Initiated)

### REMINDER: 24h before appointment
```
Hola [NOMBRE]! Te recuerdo que tenés turno mañana [DÍA] a las [HORA] en [DIRECCIÓN].

No te olvides de traer:
• Radiografías si tenés
• Documento de identidad

Si necesitás cancelar o reagendar, avisame por favor — necesito al menos 24h de anticipación.

Hasta mañana!"
```

### REMINDER: 1 week after treatment
```
Hola [NOMBRE]! Cómo estás después del tratamiento de [PROCEDURE]? 

Espero que bien! Te escribo para saber:
• ¿Tenés alguna molestia o duda?
• ¿Necesitás algo para el cuidado en casa?

 cualquier cosa escribime — estoy para ayudarte."
```

### FOLLOW-UP: 48h after pricing inquiry (no response)
```
Hola! Te escribo porque hace unos días me consultaste por [SERVICE]. 

Quiero saber si tenés alguna duda o si querés agendar. 

Si ya resolviste por otro lado, sin problema — solo quería saber.

Abrazo!"
```

### REFERRAL THANK YOU
```
Hola [NOMBRE]! Quería agradecerte porque [REFERRED_PATIENT] vino a consultarme — fue una segunda opinión sobre [REASON]. Todo fue muy bien.

Gracias por confiar y por recomendarme. Como te dije, tenés [GS 100K] de crédito para tu próximo turno. Podés usarlo cuando quieras — solo decime cuando agendes.

 abrazos!"
```

### RECALL: 6 months after cleaning
```
Hola [NOMBRE]! Ya pasaron 6 meses desde tu última limpieza — según los estándares, es hora de un control.

Te ofrezco agendar tu próxima cita? Los horarios disponibles esta semana son [SLOTS].

[NAME], te recuerdo que la limpieza regular es la mejor prevención — te ahorra tiempo y dinero a largo plazo.

 abrazos!"
```

---

## WHAT HERMES NEVER DOES

| Action | Reason | Always Escalate Instead |
|--------|--------|------------------------|
| Never diagnose | Not a dentist | Mark for Dra. GP review |
| Never promise treatment outcomes | Legal risk | Use approved language only |
| Never discuss prices beyond approved cards | Brand consistency | Use pricing template |
| Never say "no sé" without following up | Missing opportunity | Mark as needing research |
| Never respond to clinical questions | Beyond scope | Escalate to Dra. GP |
| Never transfer money or handle payments | Not a payment system | Direct to Pagopar/Bancard |
| Never share patient data externally | Ley 7593/2025 | Keep all in CRM |
| Never argue or be defensive | Reputation damage | Escalate complaints |
| Never send messages without logging | CRM integrity | Always log first |

---

## APPROVED LANGUAGE GUIDE

### Use This Language:
- "Te paso los precios como referencia"
- "El precio depende de la complejidad del caso — se confirma en la evaluación"
- "Incluye examen completo + documentación"
- "Traé las radiografías que tengas"
- "Si necesitás cancelar, avisame 24h antes"
- "Estoy para ayudarte"
- " abrazos"

### Never Use This Language:
- "No sé" → Instead: "Dejame confirmarte eso"
- "Probablemente" → Always be certain or escalate
- "Siempre" (in clinical context) → "En la mayoría de los casos"
- "Nunca hay problema" → "Haré lo posible por..."
- "Garantizado" → "El objetivo es..."
- "Sin riesgo" → "Los riesgos son..."

---

## CRM LOGGING RULES (Mandatory)

Every message action logged:

```
Date: YYYY-MM-DD HH:MM
Contact: [NAME]
Phone: [PHONE]
Source: [HOW FOUND]
Message Type: [CLASSIFICATION]
Content Summary: [3-5 word summary]
Direction: INBOUND / OUTBOUND
Agent Action: [RESPONDED / ESCALATED / LOGGED_ONLY]
CRM Updated: YES
Escalated To: [IF APPLICABLE]
Next Action: [IF ANY]
Next Action Date: [IF ANY]
```

---

## ESCALATION PROTOCOL

### Immediate Escalation (Dra. GP notified within 5 min):
- URGENT dental problems
- Complaints
- Any mention of complications from recent treatment
- Clinical questions beyond agent's scope

### Same-Day Escalation (Dra. GP notified within 4 hours):
- Second opinion requests (marked HOT_LEAD)
- Referral from existing patient (warm lead)
- Any pricing negotiation above standard rates
- Request to speak directly with Dra. GP

### Weekly Summary Escalation:
- All new contacts and classifications
- Appointment conversions
- No-shows and cancellations
- Content performance
- Any patterns noticed

---

## METRICS HERMES TRACKS

| Metric | How Measured | Target |
|--------|-------------|--------|
| Response time (first response) | Time from message received to first reply | < 30 min |
| Response time (urgent) | Time for URGENT classification | < 5 min |
| Classification accuracy | % of messages correctly classified | > 90% |
| Conversion rate | Pricing inquiry → appointment booked | > 20% |
| Show rate | Appointments scheduled → patient attended | > 70% |
| Patient satisfaction | Post-appointment survey | > 4.5/5 |
| Escalation accuracy | % of escalations that were appropriate | > 80% |

---

## IMPLEMENTATION CHECKLIST

### Before Going Live:
- [ ] WhatsApp Business API connected to Hermes
- [ ] All contacts from Dra. GP's phone imported to CRM
- [ ] Message templates loaded into agent memory
- [ ] Decision flows tested with 10 sample messages
- [ ] Dra. GP phone set up with business WhatsApp
- [ ] Emergency number confirmed and tested
- [ ] CRM linked to WhatsApp for contact lookup
- [ ] Escalation alerts tested (Dra. GP receives notification)
- [ ] Appointment calendar integrated
- [ ] All approved language loaded into agent prompts

### Week 1:
- [ ] All new messages classified by agent
- [ ] All responses reviewed by Dra. GP for accuracy
- [ ] CRM populated with new contacts
- [ ] Patterns logged and flows adjusted

### Week 2+:
- [ ] Agent handling 80%+ of first responses without escalation
- [ ] Response times meeting SLA targets
- [ ] Conversion tracking active
- [ ] Referral program tracking active

---

**STATUS:** Ready for integration with Hermes agent. All flows, messages, and escalation rules defined.