# PAYMENT INFRASTRUCTURE — REAL COSTS & ONBOARDING GUIDE
> AI research | June 2026 | Human validation required for current fees

**Paraguay (PY) Market** | Operational costs | Source: Vendor websites, payment processor docs

---

## Purpose
Establish real costs and onboarding complexity for Paraguayan dental payment
infrastructure so Dra. GP's MVP pricing model is grounded in actual merchant
fees rather than hypotheticals.

---

## Stack Assessment

### Card / QR / Link Payments — Pagopar / Upay (MERCHANT of record)

**Status:** Pagopar acquired by Upay (ueno bank). Now operates under unified brand.
- Accepts: Visa/Mastercard debit & credit (local + international), QR, wallets
  (Tigo Money, Personal Pay, Giros Claro, Zimple, Wally), bank transfers, PIX.
- No merchant POS hardware needed to start (can send payment links via WhatsApp).
- Onboarding: online registration using Cedula + phone + email.
- API integration available for website checkout.
- Subscriptions module: auto-recurring debits for treatment plans.

**What we don’t know (must verify with Pagopar support):**
- Exact merchant fee % (interchange + acquirer fee) for small clinics
- Settlement timeline (T+1? T+3?)
- Minimum monthly volume to waive fixed fee
- Chargeback/dispute policy for services
- International card acceptance fees vs. local card fees
- Whether they issue physical POS terminal or just virtual links

**Estimated model (pending verification):**
- Typical Paraguayan acquirer rate for small merchants: ~2.5–4% + fixed fee
  (spread across interchange + scheme + acquirer margin).
- High-risk merchants (services / health) sometimes higher.
- Without direct contact with Pagopar, cannot confirm.

---

### Card Terminal Alternative — Bancard POS (Paper terminal / mobile)

**Status:** Bancard offers POS rental to merchants (physical card terminal).
- Rent fee: estimated USD 15–30/month (must confirm).
- Merchant discount rate: similar to Pagopar range (2–4%).
- Attorney / contract signing required for POS ownership (different from Pagopar signup).

**Why a physical POS still matters for Dra. GP:**
- In-clinic card payments at reception
- Patients who expect to hand over a card
- Cash-heavy culture + card = incomplete addressable market without a machine

**Recommendation (pending price confirm):**
- Start with Pagopar links (zero POS cost) for online bookings + WhatsApp payment
- Add Bancard POS after first month if >40% of in-clinic shows are card-paying

---

### Bank Accounts for Medical Clinic (EAS)

**What we know:**
- Private practice must register as EAS (Empresa Individual de Responsabilidad Limitada)
- EAS can open business bank accounts at: Banco Familiar, Itaú, Ueno (formerly
  Netbank), BANCOP, etc.
- Ueno Bank (owner of Pagopar) likely offers integrated merchant + business deposit.

**What we need to verify:**
- Individual EAS personal vs. business accounts (some banks allow personal cedula
  with business activity designation, others require full business onboarding)
- AML/KYC requirements for EAS opening
- Bank transfer fees inbound from clients (local SWIFT equivalent)

---

### International Payment Options for Expat Patients

- **Local Sueldo / check / bank transfer**: free for clinic — most used by
  Paraguayan patients
- **Pagopar link**: card from US/EU accepted at acquirer's inter + cross-border fee
- **Zelle / Western Union / Wise**: possible but not routine for clinic revenue
- **Cash (USD)**: common at border-area clinics but less in Asunción proper

---

## Cost Summary Table (AI-estimated, human-validated)

| Cost type | Estimate (USD) | Source confidence |
|-----------|---------------|-------------------|
| Pagopar merchant fee | ~2.5–4% + fixed / trans | Low — vendor doc not public |
| Bancard POS rental | ~$15–30/month | Low — vendor doc not public |
| EAS bank account opening | ~$0–50 (setup) | Medium — local knowledge |
| EAS monthly maintenance | ~$5–15/month | Medium |
| Card terminal (if purchase option exists) | ~$100–250 one-time | Low |
| Inbound transfer fee (local) | ~0% for client → clinic | High — convention |
| Cross-border card surcharge (US card) | ~1–2% additional | Medium |

---

## Actionable Next Steps (AI-ready research, human execution)

1. Email Pagopar/Upay merchant support: "¿Cuál es la comisión por transacción
   para un consultorio dental pequeño?' )
2. Call Banco Familiar and Itaú: ask "¿Puedo abrir una cuenta EAS para una
   clínica dental individual? What are the requirements and fees?"
3. Ask IPEO or Risus: "What payment processor do you use?" — competitive intel
4. Ask Clínica Codas if they accept international cards directly at reception
5. Check if there is a PPP (Punto de Pos) monthly commitment fee with Bancard

---

## Human Tasks

| Task | Why human needs to do it |
|------|--------------------------|
| Phone Pagopar support | No published fee schedule — needs direct call |
| Visit 2 bank branches to EAS account options | Opening procedure requires physical ID + form completion |
| Visit Bancard office re POS contract | Contract signing in person required |
| Confirm fee schedule by asking a clinic peer | Custom merchant pricing exists for larger volume accounts |

---

*Research conducted: web extraction |
Sources: pagopar.com, pagopar.com/vender, upay.com.py, expatsetle.com,
newholidays.co.uk, thingstodoinparaguay.com*
