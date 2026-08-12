> **PRICING CROSS-REFERENCE:** All prices reference `00_STRATEGIC/financial-pricing/canonical-pricing-reference-v2.md`. When in doubt, the canonical doc wins.

# WHATSAPP BUSINESS SETUP GUIDE
## Dra. Gabriella González Pane
**Version:** 1.0 — June 2026
**Purpose:** Step-by-step instructions to set up WhatsApp Business and connect to Hermes agent

---

## BEFORE YOU START

You need:
- [ ] New phone number (can be eSIM, dedicated for business) OR existing number you're willing to convert
- [ ] Meta Business account (facebook.com/business)
- [ ] Hermes agent configured with WhatsApp MCP or himalaya
- [ ] Dra. GP's personal phone for monitoring

**IMPORTANT:** If using your existing number, chat history will be preserved but the number becomes a Business Account. Back up your chat history first.

---

## STEP 1: CREATE META BUSINESS ACCOUNT

**URL:** business.facebook.com

1. Go to business.facebook.com
2. Click "Create Account"
3. Enter: Name (your name or business name), Email, Business Name: "Dra. GP Odontología"
4. Follow prompts to verify email

**Why:** Required to access WhatsApp Business API and manage the business profile.

---

## STEP 2: SET UP WHATSAPP BUSINESS APP (Basic)

For launch, you can start with WhatsApp Business App (free) and upgrade to API later.

### Download WhatsApp Business
1. Download "WhatsApp Business" from App Store / Google Play (NOT regular WhatsApp)
2. Register with the **business phone number**
3. Verify with SMS code

### Set Up Business Profile
Fill in EVERYTHING:

```
Business name: Dra. Gabriella González Pane — Odontología con Criterio
Description: Odontología general, second opinions y planificación de tratamientos. 20 años de experiencia. Español y English.
Address: [LUQUE ADDRESS — when confirmed]
Website: [WEBSITE URL — when live]
Email: [EMAIL]
Hours: By appointment only
Categories: Dentist / Healthcare
```

### Business Profile Photo
- Use professional photo (or logo if you prefer)
- Clean, friendly, clearly you
- Not a dental chair or clinical photo

---

## STEP 3: CONFIGURE QUICK REPLIES

Quick replies are shortcuts for common responses. In WhatsApp Business App:

**Settings → Business tools → Quick replies**

Create these (you type the shortcut, app expands):

| Shortcut | Message |
|----------|---------|
| `hola` | Hola! Gracias por escribir. Soy la Dra. GP. En qué puedo ayudarte? |
| `precios` | Consulta Gs 300-400k, Restauración Gs 400-550k, Segunda opinión Gs 400-600k. Querés agendar? |
| `agenda` | Para coordinar un turno, escrebí tu nombre y te mando los horarios disponibles. |
| `horarios` | La atención es con cita previa. Escribime y coordinamos. |
| `ubicacion` | [DIRECCIÓN — when confirmed]. Por favor avísanos cuando llegues. |

---

## STEP 4: SET UP LABELS (CRM-INTEGRATED)

Labels help you organize contacts by where they are in the pipeline.

**In WhatsApp Business: Settings → Business tools → Labels**

Create these labels:

| Label | Color | For |
|-------|-------|-----|
| New Contact | 🟢 Green | Just messaged, unclassified |
| Pricing Inquiry | 🟡 Yellow | Asked about prices |
| Wants Appointment | 🔵 Blue | Ready to book |
| Second Opinion | 🔴 Red | Second opinion request (HOT) |
| Booked | 🟣 Purple | Appointment confirmed |
| Attended | 🟢 Green | Came to appointment |
| Treated | 🟣 Purple | Completed treatment |
| Cold Lead | ⚪ Gray | Didn't respond / not interested |
| Complaint | 🔴 Red | Needs attention |
| Urgent | 🔴 Red | Immediate response needed |

**How to use:** When a message comes in, assign label based on classification.

---

## STEP 5: SET UP CATALOG (Optional)

WhatsApp Business has a catalog feature to show your services:

**Settings → Business tools → Catalog**

Add services manually:

| Service | Price | Description |
|---------|-------|-------------|
| Consulta General | Gs 300-400k | Primera evaluación completa |
| Segunda Opinión | Gs 400-600k | Evaluación de diagnóstico existente |
| Restauración Simple | Gs 350-450k | 1 superficie, resina composite |
| Restauración Compleja | Gs 450-550k | 2+ superficies |
| Limpieza | Gs 150-250k | Profilaxis + fluor |

---

## STEP 6: CONNECT TO HERMES AGENT

### Option A: WhatsApp Business API (Production)
**Best for:** Full automation, broadcast messages, CRM integration

Requires:
- WhatsApp Business API via Meta Business Manager
- Approved WhatsApp Business Account
- Hermes MCP server with WhatsApp integration

**Setup:**
1. In Meta Business Manager → Add WhatsApp → Get phone number
2. Configure webhook to Hermes agent
3. Test with 5 messages
4. Go live

**Cost:** Varies by country — Paraguay ~$0.05-0.10 per message

### Option B: WhatsApp Web + Hermes (Launch)
**Best for:** Initial launch, simpler setup

**Setup:**
1. Open WhatsApp Web (web.whatsapp.com) on your business phone's WhatsApp Business
2. Or use WhatsApp Business app on phone + Hermes polls for new messages
3. Agent reads incoming, drafts responses, you approve and send OR send directly via web

**Limitation:** No automated responses, no broadcast messages

### Option C: himalaya CLI (Terminal)
**Best for:** Technical users, full automation possible

```bash
# Install himalaya
curl -sSL https://himalaya.com/install | sh

# Configure WhatsApp
himalaya account add --name dentist-gp --type whatsapp

# Configure Hermes to use himalaya
# (Agent uses himalaya as messaging backend)
```

---

## STEP 7: CONFIGURE AUTO-REPLIES (Without Agent)

WhatsApp Business has built-in auto-replies:

**Settings → Business tools → Away message**

### Away Message (When you're not online):
```
Hola! gracias por escribir.

Estoy temporalmente fuera. Te respondo dentro de las próximas horas.

Si tenés una urgencia dental, llamá al [NÚMERO DE EMERGENCIA].

任何人!
```

### Quick Replies (Instant, 24/7):
Set up in Business Tools → Quick replies → Auto-reply toggle ON

---

## STEP 8: GOOGLE SHEETS CRM SETUP

Create a Google Sheet named "DraGP Pipeline" with these tabs:

### Tab 1: Pipeline
Headers: Date | Name | Phone | Source | Referred_by | Last_Contact | Summary | Status | Next_Action | Next_Action_Date | Appts_Scheduled | Appts_Attended | Treatments | Revenue

### Tab 2: Referrals
Headers: Date | Referrer | Referred | Source | Outcome | Discount_Given

### Tab 3: Metrics
Create formulas:
- =COUNTA(Pipeline!A:A)-1 (total contacts)
- =COUNTIF(Pipeline!H:H,"Booked") (appointments)
- =COUNTIF(Pipeline!H:H,"Attended") (show rate)

---

## STEP 9: TEST BEFORE LIVE

Test every flow with 5 sample scenarios:

| Test | Who | Expected Result |
|------|-----|----------------|
| "Hola, cuánto cuesta una restauración" | Friend pretending to be patient | P1 pricing sent within 5 min |
| "Quiero agendar una consulta" | Friend | A1 sent, slots proposed |
| "Me dijo Dra. María que te contacte" | Friend | R1 sent, logged as referral |
| "Tengo un dolor muy fuerte" | Friend | U1 sent, alert to Dra. GP |
| "No estoy conforme con mi tratamiento" | Friend | ESC3 sent, alert to Dra. GP |

Review all responses — if something doesn't match brand voice, fix before going live.

---

## STEP 10: GO LIVE CHECKLIST

Before opening to real patients:

- [ ] WhatsApp Business App installed and configured
- [ ] Business profile 100% complete
- [ ] Quick replies set up and working
- [ ] Labels created and functional
- [ ] Auto-replies configured (away message + quick replies)
- [ ] Google Sheets CRM created and shared
- [ ] Hermes agent configured and tested
- [ ] All test conversations reviewed and approved
- [ ] Dra. GP phone set up with monitoring
- [ ] Emergency number confirmed (if different from business)
- [ ] First message sent to confirm WhatsApp working
- [ ] All flows logging to CRM correctly

---

## POST-LAUNCH MONITORING

### Daily (Dra. GP or assistant)
- Check new messages in WhatsApp Business
- Verify labels assigned correctly
- Check CRM updated for all new contacts
- Respond to any escalations

### Weekly (Dra. GP)
- Review CRM metrics
- Check conversion rates
- Review any complaints and resolutions
- Update message templates if needed

### Monthly (With Hermes agent review)
- Agent performance report
- Response time analysis
- Flow adjustments based on data

---

## COMMON ISSUES AND FIXES

### "WhatsApp got banned"
- Don't spam messages
- Don't send bulk messages to people who didn't opt in
- Use approved templates only
- If banned: appeal via Meta Business Manager

### "Business profile not showing"
- Verify business verification with Meta
- Add more business information
- Wait 24-48h for propagation

### "Messages not sending"
- Check internet connection
- Verify phone number is active
- Restart WhatsApp Business app
- Check if blocked by recipient

### "Agent not responding"
- Check Hermes agent is running
- Verify WhatsApp API connection
- Check if phone has internet

---

## COMPATIBILITY

| Tool | Works with WhatsApp Business? | Notes |
|------|-------------------------------|-------|
| WhatsApp Business App | ✅ Yes | Free, manual |
| WhatsApp Business API | ✅ Yes | Paid, automated |
| WhatsApp Web | ✅ Yes | Manual, browser |
| Hermes Agent | ✅ Yes | Via API or screen scrape |
| himalaya | ✅ Yes | Terminal-based |
| ManyChat | ❌ No | Only with WhatsApp API |
| Chatfuel | ❌ No | Only with WhatsApp API |

---

## WHATSAPP VS WHATSAPP BUSINESS API

| Feature | WhatsApp Business App | WhatsApp Business API |
|---------|------------------------|----------------------|
| Cost | Free | Per message |
| Auto-responses | Basic | Advanced |
| CRM integration | Manual | Automated |
| Broadcast messages | No | Yes (256 recipients) |
| Multi-user | No | Yes |
| Session management | Phone-based | Cloud-based |
|适合 | Day 1-30 | Day 30+ |

**Recommendation:** Start with WhatsApp Business App. Upgrade to API when volume justifies it.

---

**STATUS:** Setup guide complete. Ready to execute.