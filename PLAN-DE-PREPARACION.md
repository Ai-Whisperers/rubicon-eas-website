# Rubicón EAS — Plan maestro de preparación

> **Auditoría completa de repos, contenido y capacidades para entregar Rubicón EAS listo.**
> **Estado:** 2026-08-10. **Owner:** Erebus. **Cliente:** Dr. Juan María Pérez González.

---

## 0. Lo que ya está hecho

| Componente | Estado | Link |
|---|---|---|
| Sitio demo live | ✅ 200 OK | https://rubiconeas.paragu-ai.com/ |
| GitHub repo | ✅ push | https://github.com/Ai-Whisperers/rubicon-eas-website |
| 290-question intake | ✅ 10 JSON files | `intake/01-10-*.json` |
| Sample 8-page site | ✅ 134 KB | `sample/` |
| CF Worker + R2 deploy | ✅ 12 files | `worker.js` |
| Propuesta comercial 3-tier | ✅ 12.5 KB | `propuesta/PROPUESTA-COMERCIAL.md` |
| 55 reference docs downloaded | ✅ 452 KB | `legales/` |
| Issue #1 con checklist | ✅ abierto | https://github.com/Ai-Whisperers/rubicon-eas-website/issues/1 |

---

## 1. Repo audit — qué tenemos y qué no

### 1.1 Repos directamente relevantes para Rubicón EAS

| Repo | What it has | How it helps | Action |
|---|---|---|---|
| **`Ai-Whisperers/legal`** | 44 files, EAS formation docs, corporate templates, compliance (Privacidad, Data Protection, IS, Code of Conduct) | Rubicón es EAS nueva — exactamente el mismo vehicle jurídico usado para AI Whisperers. Plantillas listas. | **FORK + ADAPTAR** |
| **`Ai-Whisperers/escribania-paraguay`** | 53 files, Next.js 16 + Tailwind v4 + Docker Swarm, **complete production site** | Escribanía = servicio profesional legal. Arquitectura idéntica. | **FORKEAR el repo** como base |
| **`Ai-Whisperers/villamayor-asociados`** | 50 files, **mismo cliente legal** (estudio jurídico), tiene brand-guide, questionnaire, cookie-consent | Estudios jurídicos pequeños con markup similar. Verbatim reusable. | **FORKEAR contenido** |
| **`Ai-Whisperers/bufete-mendez`** | 35 files, tiene admin/content panel, whatsapp-ai-integration.md | Admin API pattern + integración WhatsApp AI | **REFERENCIA** |
| **`Ai-Whisperers/estudio-contable-paraguay`** | 52 files, accounting trust-profile similar | Mismo target high-trust B2B | **REFERENCIA** |
| **`Ai-Whisperers/alejandro-villamayor`** | 5 files, standalone tied to villamayor | Sub-project | Ignorar |
| **`Ai-Whisperers/dentist`** | 579 files, **gold standard** EAS legal compliance + WhatsApp bot stack | Ometz Dental EAS = mismo vehicle. WhatsApp bot v4 production-ready. | **FORK massive** |
| **`Ai-Whisperers/ai-whisperers-central`** | 32 KB, Java backend | Core agency | **REFERENCIA** |
| **`Ai-Whisperers/ai-whisperers.org`** | 44 KB, marketing site | Marketing reference | **REFERENCIA** |
| **`Ai-Whisperers/paragu-ai-leads`** | 8.6 MB, lead data | B2B prospectus | **REFERENCIA** |
| **`Ai-Whisperers/paragu-ai-platform`** | 850 MB, monorepo | Master monorepo | **REFERENCIA** |
| **`Ai-Whisperers/paragu-ai-builder`** | 467 MB, AI website builder | AI builder | **REFERENCIA** |
| **`Ai-Whisperers/site-template`** | 49 KB, Next.js 16 template | Universal template | **FORK como base** |
| **`Ai-Whisperers/client-kit`** | 14 KB, shared React components | Header, Footer, WhatsAppFloat, CookieConsent | **REUSAR** |

### 1.2 Repos NO relevantes
- ~85 repos de e-commerce, gym, spa, barber, etc. — belleza y wellness, no legal.
- Internal repos (Company-Information, Management, etc.) — sin valor para cliente.

### 1.3 Skills + patrones operativos

| Skill | Para qué |
|---|---|
| `vps-aiw-static-deploy` | CF Worker + R2 deploy (ya usado) |
| `vps-aiw-client-sites` | Live audit pattern |
| `vps-aiw-deploy-pipeline` | Deploy automation |
| `vps-aiw-autonomous-ops` | VPS ops |
| `vps-aiw-dns-fix` | CF 522 / DNS issues |
| `aiw-git-safety` | Destructive git ops |
| `aiw-ops-discipline` | Validation before completion |
| `evolution-api-destructive-ops` | Evolution API utilization |
| `trademark-compliance-scrub` | Trademark banlist scrub |
| `hermes-mensaje-via-evolution` | WhatsApp via Evolution API |
| `hermes-mensaje-setup` | Bridge setup |
| `aiw-deploy-discipline` | Verification before deploy |
| `software-development/aiw-deploy-discipline` | Host A Swarm deploy |

---

## 2. Comparación de patrones verticales

| Vertical | Repos | Patrón dominante | Para Rubicón |
|---|---|---|---|
| **Dental** (Ometz) | dentist, ometz-dental | App Next.js 16, bot WhatsApp v4, EAS legal, sitio bilingüe | **Modelo a seguir** |
| **Legal** | villamayor-asociados, bufete-mendez, escribania-paraguay, estudio-contable-paraguay | Next.js 16, questionnaire, cookie-consent, brand-guide | **Modelo vertical específico** |
| **Beauty** (cronos, xxgym, scott-tatuajes, etc.) | 19 apps en paragu-ai-leads-monorepo | Template Next.js, contenido JSON, escalado rápido | **Background ops** |
| **Plataforma** | paragu-ai-platform, paragu-ai-builder | 850 MB monorepo, builder AI | **Infra de referencia** |

---

## 3. Lo que vamos a entregar cuando el cliente diga "go"

### 3.1 Brand + Identity (8h)

| Item | Source | Status |
|---|---|---|
| Razón social + nombre comercial | `intake/01-IC-01..02` | ✅ pregunta estructurada |
| Logo | cliente | ⏳ TBD |
| Paleta de color final | `intake/01-IC-10..14` | 🟡 DRAFT (navy+bronze) |
| Tipografía | `intake/01-IC-13` | ✅ DRAFT (Source Serif + Inter) |
| Tagline | `intake/01-IC-18` | 🟡 DRAFT ("Justicia con criterio") |
| Disclaimer legal | `legenales/09-Privacy-Policy-Template.md` | ✅ plantilla reusable |
| Foto del abogado | `intake/02-PR-11` | ⏳ TBD |

### 3.2 Sitio Next.js 16 (16h)

| Page | Source | Para qué |
|---|---|---|
| `app/page.tsx` | `escribania-paraguay/app/page.tsx` | Home |
| `app/derecho-civil/page.tsx` | sample built | Vertical |
| `app/derecho-penal/page.tsx` | sample built | Vertical |
| `app/derecho-ambiental/page.tsx` | sample built | Vertical |
| `app/nosotros/page.tsx` | sample built | About |
| `app/casos/page.tsx` | sample built | Portfolio |
| `app/casos/[slug]/page.tsx` | villamayor-asociados pattern | Caso individual |
| `app/contacto/page.tsx` | sample built | Lead form |
| `app/gestion-de-datos/page.tsx` | `legales/12-Data-Protection-Policy.md` | GDPR/Ley 1682 |
| `app/aviso-legal/page.tsx` | `legales/01-EAS` + disclaimer | Aviso legal |
| `app/robots.ts` + `app/sitemap.ts` | escribania-paraguay | SEO |
| `app/api/lead/route.ts` | New — n8n webhook | Hermes handoff |
| `app/faq/page.tsx` | new | FAQ estructurada |

### 3.3 Triaje bot (Hermes Paralegal) (8h)

| Componente | Source | Para qué |
|---|---|---|
| `evolution-api-config.json` | `dentist/08_WHATSAPP/evolution-api/evolution-api-config.json` | Modo "lead triage" no "appointment" |
| `bot/main.py` | dentist fork | Adaptar de "appointment" a "capturar área + datos + derivar" |
| `bot/escalate.py` | dentist fork | Escala al abogado según categoría |
| `templates/responses/` | dentist, reescrito | civil/penal/ambiental/deriv/urgente |
| `templates/quick-replies/` | dentist fork | Quick replies para retry |
| `bot/dashboard.html` | dentist fork | Panel de triage |
| `hermes_mcp_integration.py` | dentist | Integración Hermés |
| `webhook-handler/app.py` | dentist fork | Webhook Flask-style |
| `SUPABASE-SCHEMA.sql` | dentist fork | Caso + triage schema |

### 3.4 Compliance + Legal (4h)

| Item | Source | Para qué |
|---|---|---|
| `PoliticaPrivacidad` | `legales/09-Privacy-Policy-Template.md` | Ley 1682/01 + GDPR-style |
| `AvisoLegal` | `legales/03-EAS-Constitution-Template.md` + adapt | Términos de uso |
| `Botón "Gestionar mis datos"` | new | Derecho al olvido |
| `CookieConsent` | `villamayor-asociados/components/cookie-consent.tsx` | GDPR |
| `Matrícula CSJ` prominently | `intake/02-PR-16` | Colegio Abogados |
| `Ley 19.550` disclaimers | new | Compliance ética publicitaria |

### 3.5 Deploy infrastructure (4h)

| Item | Source | Para qué |
|---|---|---|
| Dockerfile | `escribania-paraguay/Dockerfile` | Next.js standalone |
| docker-compose.yml | `escribania-paraguay/docker-compose.yml` | Traefik + Swarm |
| `.env.example` | new | Variables |
| `worker.js` | current | CF Worker |
| `legales/whatsapp-bot/` | dentist fork | WhatsApp bot runtime |
| Hetzner VPS guide | `vps-knowledge` | Host A Swarm |

---

## 4. Contenido a redactar cuando llegue el intake

### 4.1 Copy (12h)

| Item | Source | Length |
|---|---|---|
| Hero 3 párrafos | `intake/07-CX-01..04` | ~200 palabras |
| Civil: pitch + 6 servicios | `intake/03-SV-05..14` + sample | ~600 palabras |
| Penal: pitch + 6 servicios | `intake/03-SV-09..13` + sample | ~600 palabras |
| Ambiental: pitch + 6 servicios | `intake/03-SV-14..17` + sample | ~600 palabras |
| Sobre nosotros | `intake/02-PR-12..13` | ~400 palabras |
| Casos (3-9 anonimizados) | `intake/04-PO-05..10` | ~50 palabras cada uno |
| FAQ 15 items | `intake/07-CX-27..30` + sample | ~30 palabras cada uno |
| Disclaimers 5 | `legales/01-..05` | ~100 palabras cada uno |
| Bot copy | `intake/09-MK-23..25` | ~50 mensajes |
| Mensaje de WhatsApp | `dentist/08_WHATSAPP/.../responses/` | plantilla |

### 4.2 Disclaimers profesionales

| Disclaimer | Source |
|---|---|
| "La información publicada no constituye asesoramiento jurídico" | `legales/09-Privacy-Policy-Template.md` §4 |
| "Para conferir consulta formal, agende cita" | sample/contacto.html |
| "Ley 1682/01 - Sus datos son confidenciales" | Ley 1682 compliance |
| "Ley 6006/17 - UIAF (si aplica)" | `legales/13-Seven-Flag-Business-Model.md` |
| "Reglas Colegio de Abogados del Paraguay" | `sample/contacto.html` |

---

## 5. Context a recopilar ANTES de empezar

### 5.1 Identidad (de intake/01)

- [ ] Razón social exacta
- [ ] Nombre comercial
- [ ] Dominios (rubiconeas.com.py + variantes)
- [ ] RUC
- [ ] Logo
- [ ] Paleta de color HEX
- [ ] Tipografía preferida
- [ ] Idioma del sitio

### 5.2 Abogado (de intake/02)

- [ ] Nombre completo
- [ ] Matrícula CSJ (formato: "N° 23.456")
- [ ] Matrícula Colegio de Abogados
- [ ] Foto profesional
- [ ] Bio 3-5 párrafos
- [ ] Formación académica
- [ ] Idiomas

### 5.3 Servicios (de intake/03)

- [ ] Lista de servicios por área (Civil, Penal, Ambiental)
- [ ] Casos reales para portfolio (anonimizar)
- [ ] Tarifas públicas o "consultar"
- [ ] Modalidad (presencial/virtual)

### 5.4 Operación (de intake/05)

- [ ] WhatsApp institucional
- [ ] Línea de urgencias penales
- [ ] Email institucional
- [ ] Dirección física
- [ ] Horarios

### 5.5 Domain (bloqueante)

- [ ] Dominio registrado en nic.py
- [ ] CF access (compartido o transferido)

---

## 6. Pricing y propuesta (ya en propuesta/)

| Tier | Setup | Monthly | Triggers |
|---|---|---|---|
| A Base | Gs. 2.000.000 | Gs. 550.000 | Mes 0, validez 30d |
| B Profesional | Gs. 4.500.000 | Gs. 1.300.000 | Mes 0 + 90 días |
| C Premium | Gs. 9.000.000 | Gs. 2.500.000 | Mes 4+ |

---

## 7. Roadmap de entrega (5 working days)

| Day | Deliverable | Hours |
|---|---|---|
| 0 | Brief intake completa del cliente | 8h |
| 0.5 | Logo + foto del abogado (cliente provides) | - |
| 1 | Discovery session + sitemap + content wireframe | 6h |
| 2 | Next.js fork + brand + 8 páginas base | 16h |
| 3 | Triage bot + Evolution API integration | 8h |
| 2 | Copy legal (3 áreas + casos + FAQ) | 12h |
| 4 | Compliance (Ley 1682, GDPR-style, Colegio) | 4h |
| 4 | Deploy to Host A Swarm + R2 + DNS | 4h |
| 5 | UAT + legal review + handoff | 6h |
| **Total** | | **64h** |

---

## 8. Riesgos identificados

| Risk | Mitigation |
|---|---|
| Cliente no llena intake | Walkthrough session 2h |
| Cliente no tiene logo | Mock-up basado en paleta |
| Datos sensibles de matrícula | Solo display público, no almacenar |
| Imágenes de casos sin consentimiento | No usar fotos. Solo texto + íconos. |
| Trademark compliance | Scrub todo copy contra banlist |
| Casos confidenciales | Anonimizar O usar placeholders fiction |
| Dominio no registrado | Live preview funciona en `rubiconeas.paragu-ai.com` |
| WhatsApp institucional no listo | Stand-by: site CTA apunta a `wa.me/000000000` |
| Inbox diario sin responder | Triage bot fallback + escalado |
| Pago del abogado | Mostrar Política de pagos + factura tipo |

---

## 9. Próximos pasos (cuando el cliente confirm)

1. Email al cliente: `propuesta/PROPUESTA-COMERCIAL.md` + `intake/01-10-*.json` + URL demo
2. Llamada de discovery (60 min) — cerrar scope
3. Comisión 50% setup al firmar
4. Asignar equipo (1 dev + 1 director de proyecto)
5. Iniciar fork del `escribania-paraguay` repo → `Ai-Whisperers/rubicon-eas`
6. Esperar intake completo
7. Construir en 5 días
8. Handoff + soporte 30 días

---

## 10. Repositorio Rubicón EAS — estado final

```
Ai-Whisperers/rubicon-eas-website (GitHub)
├── README.md
├── DEPLOY.md
├── PLAN-DE-PREPARACION.md                ← este archivo
├── intake/                                (10 JSON, 290 questions)
├── sample/                                (8 HTML live at rubiconeas.paragu-ai.com)
├── propuesta/PROPUESTA-COMERCIAL.md       (3-tier pricing)
├── legales/                               (55 reference docs, 452 KB)
│   ├── 01-EAS-..-Guide.md
│   ├── 02-EAS-Formation-Checklist.md
│   ├── 03-EAS-Constitution-Template.md
│   ├── 04-EAS-Formation-Plan.md
│   ├── 05-Paraguay-Corporate-Forms-Comparison.md
│   ├── 06-Master-Service-Agreement-Template.md
│   ├── 07-Independent-Contractor-Agreement.md
│   ├── 08-NDA-Template.md
│   ├── 09-Privacy-Policy-Template.md
│   ├── 10-Code-of-Conduct-Template.md
│   ├── 11-Information-Security-Policy.md
│   ├── 12-Data-Protection-Policy.md
│   ├── 13-Seven-Flag-Business-Model.md
│   ├── research/                          (7 docs, formación + habilitación)
│   ├── practice-legal/                    (8 docs, contrato + estatutos)
│   ├── patient-legal/                     (4 docs, paciente + privacidad)
│   ├── whatsapp-bot/                       (Bot v4 fork + responses)
│   └── quick-replies/                      (Objection library)
└── worker.js
```

---

## 11. What's still missing

| Item | Risk | Plan |
|---|---|---|
| Perfil de abogado real | Bloqueante | Side-discovery 1h |
| Logo y foto | Bloqueante | Walkthrough sesión |
| Casos reales o autorización | Bloqueante | Discusión legal |
| WhatsApp Business | Bloqueante | Setup si tiene |
| Dominio `rubiconeas.com.py` | Bloqueante | Client registers at nic.py |
| Política privacidad final | Bloqueante | Lawyer reviews |
| 1 ronda de UAT del abogado | Necesario | 1h |

---

## 12. De un vistazo: el repositorio Rubicón EAS

| Tier | Estado | Siguiente |
|---|---|---|
| **Tier 1: Demo** | ✅ Live | Cliente visita URL |
| **Tier 2: Lead capture** | 🟡 Bot draft | Wire n8n cuando llegue WhatsApp |
| **Tier 3: Production** | 🟡 Placeholders reales | Reemplazar cuando llegue intake |
| **Tier 4: Compliance** | 🟡 Templates | Customize para Paraguay PY |
| **Tier 5: Client repo** | 🟡 Monorepo | Fork `escribania-paraguay` como base |

---

## 13. Resumen ejecutivo

**Tenemos el 90% del trabajo preparatorio listo.**

- ✅ Sitio demo live con contenido completo
- ✅ Cuestionario de 290 preguntas estructurado
- ✅ Propuesta comercial de 3 tiers
- ✅ 55 documentos de referencia legal y de compliance
- ✅ Patrón de WhatsApp bot listo para fork
- ✅ Plantilla Next.js 16 lista para producción
- ✅ Esquema de deploy a Host A Swarm documentado

**Lo que falta es 100% información del cliente:**
- Partner bio + foto
- Datos reales (matrícula, contacto)
- Casos anonimizados
- WhatsApp institucional
- Dominio registrado
- Confirmación de plan (A, B o C)

**Una vez llegue el intake, 5 días de trabajo end-to-end.**

---

*Plan actualizado 2026-08-10. Versión 1.0.*
