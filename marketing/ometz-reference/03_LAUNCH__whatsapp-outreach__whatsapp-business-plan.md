## PRICING CROSS-REFERENCE (June 2026)

> Service prices in this document are NOT authoritative. The master reference is:
> `00_STRATEGIC/financial-pricing/canonical-pricing-reference-v2.md`
>
> Any price update should happen in the canonical file only.

---

# WHATSAPP BUSINESS AUTOMATION FLOWS
## Dra. Gabriella González Pane
**Phase:** Planning (not building)
**Version:** 1.0 — June 2026

---

## PURPOSE

WhatsApp Business is the primary patient acquisition and communication channel. This document specifies all automated flows, message sequences, and manual responses needed.

**Why WhatsApp over other channels:**
- Paraguayan market expects WhatsApp communication
- Expat audience uses WhatsApp as primary messaging
- Lower friction than phone calls for first contact
- Direct, personal, not corporate
- Rich communication (can send photos, voice notes, documents)

---

## CHANNELS

### WhatsApp Business App (Free Tier)
- Suitable for initial launch
- Can handle up to ~100 conversations/month
- Limited automation (quick replies only)
- No broadcast messaging capability

### WhatsApp Business Platform (WhatsApp Business API)
- For later scale (when volume increases)
- Broadcast messaging (up to 256 recipients)
- Advanced automation and CRM integration
- Token-based verification
- Recommended to upgrade when: 20+ patients/month and/or launch referral program

**For launch:** WhatsApp Business App free tier is sufficient.

---

## CONTACT POINTS — INCOMING MESSAGES

Every message from a potential patient will fall into one of these categories:

| Message Type | Expected Frequency | Automated Response? |
|---|---|---|
| pricing inquiry | High | Yes — automation or quick reply |
| appointment request | High | Yes — automated availability request |
| second opinion question | Medium | Yes — automated but needs personal follow-up |
| location/directions | Medium | Yes — quick reply |
| "I was referred by X" | Low-Medium | No — personal response (track referral) |
| urgent dental problem | Low | No — personal, immediate response |
| existing patient question | Low | No — personal response |

---

## AUTOMATED FLOW 1: FIRST CONTACT — PRICING INQUIRY

**Trigger:** Someone messages asking "cuánto cuesta" or "precios" or "how much"

**Flow:**

```
USER: "Hola, cuánto cuesta una restauración?"
↓
SYSTEM AUTO-REPLY:
"Hola! Gracias por escribir. Te paso los precios generales como referencia:

• Restauración simple: Gs 350-450k
• Restauración compleja: Gs 450-550k
• Consulta / Second Opinion: Gs 400-600k
• Limpieza: Gs 150-250k

El precio exacto depende de la complexity del caso — necesito ver tu situación para darte un presupuesto preciso.

Si tenés una evaluación o radiografías existentes, podemos hacer una segunda opinión formal.

Para agendar una consulta -> [BUTTON: Agendar por WhatsApp]

Respondé este mensaje o escribime directamente si tenés más preguntas!"
↓
[60% move to appointment request]
[30% ask follow-up question — manual]
[10% go silent]
```

**Quick Reply Setup (free tier):**
- "Precios consulta" — sends pricing overview
- "Segunda opinión" — sends second opinion explanation
- "Agendar" — sends "Escribí tu nombre y número para coordinar turno"

---

## AUTOMATED FLOW 2: APPOINTMENT REQUEST

**Trigger:** Someone says they want to schedule / "agendar"

**Flow:**

```
USER: "Quiero agendar una consulta" / "Me gustaría un turno"
↓
AUTO-REPLY:
"Hola! Con gusto te ayudo a coordinar. 

Para poder ofrecerte horarios disponibles, necesito:

1. Tu nombre
2. Qué te trae: ¿Estás buscando una primera consulta, segunda opinión, o necesitas algo específico?
3. Tenés radiografías o diagnósticos previos?

Después de tu respuesta te mandamos opciones de horarios disponibles."

[CUSTOMER RESPONDS WITH INFO]
↓
MANUAL: Dra. GP or staff checks availability, sends specific times
↓
CUSTOMER: Chooses time
↓
CONFIRM:
"Perfecto! Quedás confirmada/o para [DATE] a las [TIME] en Luque.
Dirección: [ADDRESS — once confirmed]
IMPORTANTE: Traé cualquier X-ray o documentación que tengas sobre tu caso.

Si necesitás cancelar o reagendar, escribime con anticipation."

[Appointment is booked in Dra. GP's personal calendar for now — no system needed at launch]
```

---

## AUTOMATED FLOW 3: SECOND OPINION INQUIRY

**Trigger:** Someone messages about a treatment plan they were given / "me dijeron que necesito"

**Flow:**

```
USER: "Otro dentista me dijo que necesito un crown / root canal / extracción... quiero saber si es cierto"
↓
AUTO-REPLY:
"Entiendo — buscar una segunda opinión antes de avanzar es una muy buena decisión.

Para poder darte una evaluación real, necesito:

1. Si tenés X-rays o tomografía del caso, las puedo revisar
2. Qué te dijo el otro dentista exactamente
3. Hace cuánto tiempo te dijeron esto

Si no tenés rayos现有的, en la consulta podemos tomar nuevas radiografías para hacer una evaluación completa.

La consulta de segunda opinión cuesta entre Gs 400-600k dependiendo de la complejidad del caso. Incluye:
- Examen completo
- Documentación de hallazgos
- Opciones de tratamiento explicadas por escrito

Querés que agendemos una fecha?"

[CUSTOMER RESPONDS]
↓
MANUAL FOLLOW-UP: Dra. GP handles personally — this is a high-value inquiry
```

---

## WELCOME MESSAGE (for new contacts not in address book)

**Trigger:** When a new contact starts a conversation (after 24h+ gap)

**Text:**
```
Hola! 👋

Soy la Dra. Gabriella González Pane. Mi consultorio está en Luque, Asunción.

Me especializo en second opinions y tratamiento dental con planificación cuidadosa — no hago procedimientos que no son necesarios.

¿En qué puedo ayudarte?
```

---

## QUICK REPLIES (Free Tier — for common questions)

| Shortcut | Message |
|----------|---------|
| `precios` | *Sends pricing card with main procedure prices* |
| `agenda` | *Sends "Escribí tu nombre y número para coordinar" and available time slots* |
| `segunda` | *Sends brief explanation of second opinion + pricing* |
| `ubicacion` | *Sends address (once confirmed) + note about appointment-only* |
| `horarios` | *Sends "Atención solo con cita previa. Escribime para coordinar"* |

---

## EXISTING PATIENT FOLLOW-UP FLOWS

### Post-Appointment (Manual but templated)
After sending messages like:
```
"Hola [NOMBRE]! Espero que estés bien. Te escribo para saber cómo va todo después del tratamiento de [DATE].

¿Tenés alguna pregunta o querés contarme cómo te sentís?

Si todo está bien, te veo en [NEXT APPOINTMENT DATE]!"
```

### Post-Treatment Instructions
Can be templated messages for common procedures:
```
"After your restoration today:
- Don't eat hard foods for 2 hours
- You may feel sensitivity for a few days — that's normal
- If you feel pain after 48h, write me immediately
- We're available on WhatsApp if you need anything"
```

---

## BROADCAST MESSAGES (Once on WhatsApp Business API)

Can only be sent to contacts who opted in. Use for:

| Message Type | Frequency | Example |
|---|---|---|
| New service announcement | Monthly or less | "Now offering second opinions as a standalone service" |
| Referral program reminder | Quarterly | "Know someone who needs a second opinion? Send them my way — both get a Gs 100k discount" |
| Holiday greeting | On holidays | Brief, professional |

**IMPORTANT:** Never send promotional spam. Never message patients who didn't opt in. Never message more than 2x/month max.

---

## REFERRAL TRACKING IN WHATSAPP

When someone messages and mentions they were referred:

```
"¿Cómo nos encontraste?" / "Who referred you?"
↓
Response: "[Name of referrer]"
↓
LOG IN CRM: [Date] [Name of referrer] referred [New patient name]
```

This is tracked manually in a spreadsheet at launch:
Columns: Date | Referred by | Referred to | Outcome | Discount given (Y/N)

---

## FORWARD-LOOKING: CRM INTEGRATION (Phase 2)

Once volume increases, consider connecting WhatsApp Business API to:
- Notion CRM (free, simple)
- Google Sheets + integromat/zapier
- Airtable

For now: WhatsApp Business App + manual spreadsheet tracking is sufficient.

---

## WHAT NOT TO AUTOMATE

- Responses to complex clinical questions (always sends to manual)
- Billing or payment discussions (always personal)
- Patient complaints or concerns (always personal, immediate)
- Scheduling changes within 24h of appointment (always personal)
- Any message from an existing patient in active treatment (always personal)

---

## MESSAGE RESPONSE TIME EXPECTATIONS

At launch: Dra. GP responds personally to all WhatsApp messages within 24 hours on weekdays.

**Target SLAs:**
- First contact (new prospect): < 24 hours
- Appointment requests: < 12 hours (same day if possible)
- Urgent dental issues: < 2 hours (give her personal number for emergencies: specify this)

**If volume becomes unmanageable:**
- Add dedicated assistant
- Implement scheduling software (Calendly or similar)
- Move to WhatsApp Business API

---

## LAUNCH CHECKLIST — WHATSAPP

- [ ] WhatsApp Business app installed on her phone
- [ ] Business profile created (photo, bio, address)
- [ ] Quick replies set up for: precios, agenda, segunda, ubicacion, horarios
- [ ] Welcome message scripted and enabled
- [ ] Auto-reply for "away" hours set up
- [ ] Response time commitment set (24h weekdays)
- [ ] Urgent issues number shared with existing patients (separate from business WhatsApp)
- [ ] Incoming message tracking spreadsheet created
- [ ] Referral tracking column added to spreadsheet

---

**STATUS:** Planning complete. Ready for Dra. GP review and approval.
