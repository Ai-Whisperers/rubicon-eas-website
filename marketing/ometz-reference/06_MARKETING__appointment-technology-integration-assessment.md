# APPOINTMENT TECHNOLOGY — DD / SAM INTEGRATION ASSESSMENT
> AI research | June 2026 | Technical validation recommended

**Dra. GP clinic** | Systems analysis | Source: Project docs + public market research

---

## Purpose
Determine whether existing appointment technology (DW / SAM Citas module)
already supports the automation stack Dra. GP needs — WhatsApp scheduling,
online booking, reminders, reactivation — or whether a separate system is
required.

---

## Current State (from project docs)

System **SAM Citas module** is currently used for:
- Appointment scheduling
- Patient record linkage (Fichas)
- Insurance/workflow tracking

Previous discovery notes note:
- 601 appointments exported
- 62.5% completion rate documented (Jan-May 2026)
- 38.5% late-arrival rate (operational bottleneck)

---

## What SAM Citas module does NOT confirm (from docs reviewed)

- WhatsApp API integration (mutex/bot side)
- Online patient self-booking portal
- SMS reminder automation
- Recall / reactivation queue
- Two-way calendar sync
- Payment hold or deposit at booking
- English-language interface

---

## WhatsApp Scheduling Options (AI assessment)

### Option A — Direct WhatsApp API (recommended)
- Patient messages clinic number → bot parses intent → calls SAM API
- Stack: WhatsApp Business API (via Meta or provider) + SAM webhook + simple
  queue/booking bot sending confirmed response
- Requires SAM API documentation (or screen-scraping fallback)
- **Best for:** reducing admin load, bilingual support, after-hours

### Option B — Third-party bridge (iaO / DialogTech)
- Some LATAM dental clinics use DialogTech / Dialogo type services
- Likely subscription + API
- **Best for:** quick launch without SAM API access

### Option C — WhatsApp link + human confirmation (minimum viable)
- Patient sends structured message → assistant manually enters SAM
- Cost: assistant time
- Works as stepping stone until Option A is ready

---

## Assessment: Online Booking Portal Feasible?

**Short answer: not confirmed.**

SAM Citas module documentation reviewed does not show a patient-facing
booking endpoint. Without one, online booking requires a parallel system:

| Approach | Effort | Risk | When to choose |
|----------|--------|------|----------------|
| Build custom booking app + write to SAM DB | High | Medium | If SAM DB structure is documented |
| Use Calendly + manual SAM entry | Low | High | Phase 0 testing only |
| Use Google Calendar as bridge | Low | Medium | Single-doctor clinics |
| Wait for SAM to expose booking API | None | Doesn't solve now | Passive |

**Recommended approach for Dra. GP MVP:**
1. Week 0–2: Manual WhatsApp scheduling — no middle-tier software
2. Week 4: Build or buy simple calendar bridge (Google Calendar + reminder bot)
3. Month 2–3: Evaluate SAM API access via DW account manager

---

## What This Means for the Launch Stack

Minimum viable automations (without SAM integration):
- **WhatsApp Business with quick replies** for scheduling FAQs
- **Google Calendar** as the visible calendar
- **Assistant manually enters SAM** after each confirmed WhatsApp booking
- **Follow-up SMS/WA** sent via simple cron script (scheduled reminders)

Advanced stack (with SAM API access):
- Full WhatsApp chatbot booking
- Automated pre-appt forms
- Insurance verification via API
- Post-appt reactivation drip

---

## SAM Integration Risks to Flag

1. **Data residency** — SAM is a hosted system; confirm API/export access is
   allowed under their contract with DW
2. **Fields mismatch** — SAM custom fields may not map cleanly to WhatsApp
   structured messages
3. **Concurrency** — what if WhatsApp bot and assistant update same slot
   simultaneously? Locking required.
4. **Language** — SAM UI may be Spanish-only; API returns must be consistent

---

## Recommended Action Sequence

| Priority | Action | Owner |
|----------|--------|-------|
| P0 | Confirm SAM Citas has API or webhook endpoint | Erebus / DW account manager |
| P0 | Confirm SAM data export rights | Erebus |
| P1 | Set up WhatsApp Business number (before any ops) | Human |
| P1 | Build WhatsApp quick-reply templates (FAQ-based) | Erebus + Copy |
| P2 | Build appointment reminder cron (Google Calendar → WA) | Erebus |
| P2 | Shadow booking SOP — assistant uses duplicate calendar | Dra. GP + assistant |
| P3 | If SAM API confirmed: build WhatsApp bot booking | Erebus |
| P3 | If SAM API blocked: explore DW internal scheduling tools | Erebus |

---

## Human Tasks

| Task | Why human required |
|------|--------------------|
| Call DW / SAM support: "Does Citas module have an API?" | Vendor conversation |
| Confirm SAM contract term for data export rights | Legal/contract |
| Provide sample WhatsApp scheduling scenarios to bot | Product decision |
| Decide pricing for online booking (free, deposit, pay-later) | Business decision |
| Draft patient data handling acceptance language | Legal/compliance |

---

*Research conducted: project doc review + public web;
Sources: SAM Citas module reference, expatsetle.com, ip*
