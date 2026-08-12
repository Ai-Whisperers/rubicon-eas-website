# WHATSAPP CHANNEL — MASTER INDEX

> **PRICING CROSS-REFERENCE:** Pricing card in this doc reflects `00_STRATEGIC/financial-pricing/canonical-pricing-reference-v2.md`. Update prices by editing the canonical doc + re-running reconciliation, never inline here.
**Version:** 1.0 — June 2026

---

## PURPOSE

Complete operational blueprint for the WhatsApp patient acquisition channel, managed by Hermes agent.

---

## FILE STRUCTURE

```
whatsapp/
├── 00-whatsapp-operations-guide.md    ✅ MASTER GUIDE — architecture, flows, escalation
├── 01-message-templates-library.md    ✅ ALL MESSAGE TEMPLATES — 50+ approved messages
├── 02-conversation-flows.md           ✅ DECISION TREES — every possible path
├── 03-hermes-agent-protocol.md       ✅ AGENT BEHAVIOR — rules, memory, constraints
├── 04-whatsapp-setup-guide.md       ✅ SETUP GUIDE — step by step
└── 05-crm-template.md               ✅ GOOGLE SHEETS CRM TEMPLATE (in this file)
```

---

## QUICK REFERENCE

### Message Count
| Template Type | Count |
|--------------|-------|
| Welcome | 3 |
| Pricing | 5 |
| Appointment | 7 |
| Second Opinion | 5 |
| Existing Patient | 5 |
| Urgent/Emergency | 2 |
| Referral | 3 |
| Escalation | 4 |
| Outbound Proactive | 3 |
| Blocked/Spam | 3 |
| **TOTAL** | **50+** |

### Decision Trees
| Flow | Classification Trigger |
|------|----------------------|
| New Contact | Any message from unknown number |
| Existing Patient | Phone found in CRM |
| Pricing | "cuánto cuesta" / "precios" |
| Appointment | "agendar" / "turno" / "cita" |
| Second Opinion | "second opinion" / "me dijeron que necesito" |
| Urgent | "dolor" / "urgencia" / "sangre" |
| Referral | "me recomendó" / "me dijo que te contacte" |
| Complaint | "no estoy conforme" / "mal resultado" |

### Escalation Rules
| Type | SLA |
|------|-----|
| Urgent dental | < 5 min |
| Second Opinion | < 30 min |
| Complaint | < 2 hours |
| General | < 24 hours |

---

## GOOGLE SHEETS CRM TEMPLATE

### Tab 1: Pipeline

Create with headers (Row 1):

| Date | Name | Phone | Source | Referred_By | Last_Contact | Summary | Status | Next_Action | Next_Action_Date | Appts_Scheduled | Appts_Attended | Treatments | Revenue |
|------|------|-------|--------|-------------|--------------|---------|--------|-------------|-----------------|----------------|----------------|------------|---------|

**Status Values:**
- `new` — first contact
- `pricing_inquiry` — asked about prices
- `wants_appointment` — ready to book
- `second_opinion` — second opinion request (HOT)
- `booked` — appointment confirmed
- `attended` — came to appointment
- `treated` — completed treatment
- `cold_lead` — no response after follow-ups
- `complaint` — needs attention
- `not_interested` — explicitly said no

### Tab 2: Referrals

Headers:
| Date | Referrer_Name | Referred_Person | Source | Outcome | Discount_Given |

### Tab 3: Metrics

Create these calculated cells:

```
Total Contacts: =COUNTA(A2:A1000)-1
New This Week: =COUNTIFS(A:A,">="&TODAY()-7)
Appointments Booked: =COUNTIF(H:H,"booked")
Appointments Attended: =COUNTIF(H:H,"attended")
Show Rate: =IF(COUNTIF(H:H,"booked")>0,COUNTIF(H:H,"attended")/COUNTIF(H:H,"booked"),"N/A")
Hot Leads: =COUNTIF(H:H,"second_opinion")
Complaints: =COUNTIF(H:H,"complaint")
Revenue This Month: =SUMIF(M:M,">="&EOMONTH(TODAY(),-1)+1,N:N)
```

### Tab 4: Message Log

Headers:
| Timestamp | Contact | Direction | Type | Content_Summary | Agent_Action | Escalated |

---

## IMPLEMENTATION SEQUENCE

### Week 1: Setup
- [ ] Set up WhatsApp Business App
- [ ] Configure business profile
- [ ] Create Google Sheets CRM
- [ ] Test all templates manually
- [ ] Load templates into Hermes agent

### Week 2: Soft Launch
- [ ] Hermes agent monitoring WhatsApp
- [ ] Agent responds to pricing inquiries
- [ ] All responses logged to CRM
- [ ] Dra. GP reviews all responses daily

### Week 3: Full Auto
- [ ] Agent handling 80%+ first responses
- [ ] Escalations working correctly
- [ ] CRM fully populated
- [ ] Conversion tracking active

### Week 4+: Optimize
- [ ] Weekly metrics review
- [ ] Adjust templates based on data
- [ ] Add new flows as needed
- [ ] Scale to WhatsApp Business API when volume justifies

---

## KEY DECISION: WhatsApp Business App vs API

| | App | API |
|--|-----|-----|
| Cost | Free | ~$0.05-0.10/msg |
| Automation | Basic | Full |
| Scalability | Low | High |
| CRM Integration | Manual | Automatic |
| Best For | Launch | Month 3+ |

**Recommendation:** Start with App. Move to API when handling 50+ messages/week.

---

## METRICS TO TRACK

| Metric | Week 1 | Week 4 Target |
|--------|--------|---------------|
| Response time avg | < 2h | < 30 min |
| Response time urgent | < 15 min | < 5 min |
| Booking conversion | — | > 25% |
| Show rate | — | > 70% |
| Hot lead response | — | < 30 min |
| Escalation accuracy | > 90% | > 95% |
| CRM completeness | 100% | 100% |

---

## CONTACT SHEET — EMERGENCY NUMBERS

| Purpose | Number | Notes |
|---------|--------|-------|
| Business WhatsApp | [TO FILL] | Main channel |
| Dra. GP direct | [TO FILL] | For escalations |
| Emergency dental | 141 | Hospital de Clínicas |
| Hermes Agent Monitor | [TO FILL] | Agent alerts |

---

## APPROVED TEMPLATE REPOSITORY

All 50+ templates are in: `whatsapp/01-message-templates-library.md`

Agent instruction: Read from this file for every response. Never improvise outside approved templates without escalation.

---

## NOTES FOR HERMES AGENT

1. Every message → classify → respond from template → log to CRM
2. If uncertain → escalate, don't improvise
3. If patient says something unexpected → use ESC1 (clarification) template
4. If clinical → always escalate to Dra. GP
5. URGENT → immediate alert, never wait

---

**STATUS:** Complete WhatsApp operational system. Ready to execute.