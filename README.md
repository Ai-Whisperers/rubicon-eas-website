# Rubicón EAS — Build Repo

**Status:** Live preview deployed. Awaiting client brief.
**Live URL:** https://rubiconeas.paragu-ai.com/
**Live Worker:** `rubicon-eas-site` in CF account `9eb1832f3e42a1dbd6ba854f8d6a1cb2`
**Storage:** `s3://ai-whisperers-backups/rubicon-eas/` (12 files, 134KB total)

---

## What's in this repo

```
/opt/data/build/rubicon-eas/
├── README.md                           # This file
├── intake/                             # 200-question client questionnaire
│   ├── 01-identidad-corporativa.json   # 20 questions
│   ├── 02-perfil-profesional.json     # 30 questions
│   ├── 03-servicios-juridicos.json     # 30 questions
│   ├── 04-portfolio-casos.json         # 30 questions
│   ├── 05-oficina-equipo.json          # 30 questions
│   ├── 06-web-objetivos.json           # 30 questions
│   ├── 07-contenido-ux.json            # 30 questions
│   ├── 08-seo-legal.json               # 30 questions
│   ├── 09-marketing-comercial.json     # 30 questions
│   ├── 10-seguridad-ops.json           # 30 questions
│   └── _totals.json                    # 290 questions total
├── sample/                             # 8-page sample website
│   ├── index.html
│   ├── derecho-civil.html
│   ├── derecho-penal.html
│   ├── derecho-ambiental.html
│   ├── nosotros.html
│   ├── casos.html
│   ├── contacto.html
│   ├── blog.html
│   ├── assets/
│   │   ├── styles.css                  # 23KB — full design system
│   │   ├── main.js                     # 2KB — nav, FAQ, form
│   │   └── content.es.json             # 18KB — source of truth
│   └── README.md
├── sample-urls.json                    # 12 presigned R2 URLs
├── worker.js                           # 5.9KB CF Worker code
└── DEPLOY.md                           # Deploy + iteration playbook
```

---

## How to use this with the client

### Session 1 — fill the questionnaire (`intake/01-10-*.json`)

Send the client a single message:

> "Hola. Para arrancar el proyecto de tu web Rubicón EAS necesito que
> respondas 290 preguntas estructuradas. Las organicé en 10 secciones de
> 20-30 preguntas. Te las paso adjuntas. Respondé con el mismo formato
> que te doy (texto libre, archivos adjuntos, opciones). Si no sabés una
> respuesta, dejala en blanco y seguimos."

The intake covers:
- Identity, branding, language preferences
- Partner bio, credentials, formation
- Service catalog (Civil / Penal / Ambiental)
- Case studies + testimonials
- Office, team, ops
- Web goals, audience, KPIs
- Content copy, microcopy
- SEO + legal compliance
- Marketing, funnel, automation
- Hosting, security, observability

### Session 2 — replace placeholder content

Once the client fills `intake/`, Erebus:
1. Parses the JSON file
2. Replaces `{{placeholder}}` marks in `sample/assets/content.es.json` with real values
3. Re-runs the page generator (or hand-edits since each page is <300 lines)
4. Re-uploads to R2 + Pushes new Worker version
5. URL stays the same: `rubiconeas.paragu-ai.com`

### Session 3 — domain + custom Worker route

Once client registers `rubiconeas.com.py` at nic.py:
1. Add zone to CF
2. Add apex + www → CF proxy (or grey-cloud + Host A Swarm)
3. Add Worker route for apex
4. Update worker.js with apex-specific logic
5. Or replace Worker with Host A Swarm `nexa-paraguay`-style Next.js deploy

### Session 4 — Next.js build (canonical)

Once content is final:
1. Fork `paragu-ai-leads-monorepo/apps/Clau-Bellino/` → `apps/rubicon-eas/`
2. Replace `content/es.json` with `sample/assets/content.es.json` (already in canonical schema)
3. Add additional pages: `/derecho-civil`, `/derecho-penal`, `/derecho-ambiental`, `/casos/[slug]`, `/blog/[slug]`
4. `pnpm install && pnpm build`
5. Push to Host A Swarm via `/opt/stacks/rubicon-eas/docker-compose.yml`
6. Grey-cloud DNS → Traefik → service with Let's Encrypt

### Session 5 — Triage bot integration

Wire n8n workflow → Evolution API → WhatsApp:
- Lead form on `contacto.html` POSTs to `/api/lead`
- Webhook forwards to n8n
- n8n formats Mensaje message and sends via Evolution API
- Partner's WhatsApp = `+595 981 234 567` (fictional placeholder)

---

## Live preview

**Domain:** https://rubiconeas.paragu-ai.com/

The site is live NOW with placeholder content. Anyone with the URL can see:
- Full home page with hero, trust strip, 3 area cards, why-us, sample cases, testimonials, FAQ, contact
- 7 inner pages with consistent navigation
- Working lead form (form-related JS only — no backend wired yet)
- Floating WhatsApp button → `wa.me/595981234567`
- Mobile-responsive design
- All FAQ accordions work
- All internal links navigate

This is the **demo for the client**. The questionnaire `intake/` is the **brief**.

---

## What is fictional vs. real

| Item | Status |
|---|---|
| Site architecture | Real (final, deployable) |
| Color palette, typography, copy structure | Real (final, deployable) |
| Page layout, CSS, JS | Real (final, deployable) |
| Persona "Dr. Juan María Pérez" | **Fictional placeholder** |
| Matrícula CSJ 23.456 | **Fictional placeholder** |
| Phone numbers (+595 981 234 567, etc.) | **Fictional placeholder** |
| Email (contacto@rubiconeas.com.py) | **Fictional placeholder** |
| Address (Av. Mariscal López 1234) | **Fictional placeholder** |
| 9 case studies | **Fictional placeholder** — anonymized; can be replaced with real |
| 15 FAQ items | **Draft copy** — needs review by attorney |
| 3 testimonials | **Fictional placeholder** — replace with real or remove |

The client sees: a real-looking site that demos the architecture. The structure stays the same; only the words change.

---

## Domain status

**NOT registered yet.** Client must register `rubiconeas.com.py` at nic.py
(~gs. 200-300k/yr). Until then, the site lives on `*.paragu-ai.com`.

When the client has the domain:
- Add to Cloudflare (free plan works)
- I can add the zone, configure DNS, deploy to Host A Swarm
- Or use CF Pages directly

---

## What I'll do once we have the brief

1. Replace placeholder content in `sample/assets/content.es.json`
2. Regenerate any pages that need copy changes
3. Add real photo of the partner
4. Update Matrícula, phone, email, address
5. Add real case studies (or remove if no consent)
6. Legal review of disclaimer + privacy policy
7. Wire the lead form to n8n + Evolution API
8. Deploy to production (Host A Swarm or CF Pages)
9. Bind to `rubiconeas.com.py` if/when registered

Working estimate: **5–7 days** end-to-end after brief is filled.

---

## Files for the client

When sending the questionnaire to the client, include:
- `intake/01-10-*.json` (10 files, ~290 questions)
- `sample/README.md` (explains the demo)
- Live URL: https://rubiconeas.paragu-ai.com/

The client can respond either in the JSON files (replace `null` with answers)
or in free-form text. Erebus will parse and integrate.

---

## Live verification (recorded 2026-08-10)

```
URLs returning HTTP 200:
  ✓ /                          16,443 bytes  "Rubicón EAS · Asesoría jurídica..."
  ✓ /index.html                16,443 bytes  same
  ✓ /derecho-civil.html        11,645 bytes  "Derecho Civil · Rubicón EAS"
  ✓ /derecho-penal.html        11,232 bytes  "Derecho Penal · Rubicón EAS"
  ✓ /derecho-ambiental.html    11,020 bytes  "Derecho Ambiental · Rubicón EAS"
  ✓ /nosotros.html              9,132 bytes  "Nosotros · Rubicón EAS"
  ✓ /casos.html                10,778 bytes  "Casos atendidos · Rubicón EAS"
  ✓ /contacto.html             15,037 bytes  "Contacto · Rubicón EAS"
  ✓ /blog.html                  7,851 bytes  "Artículos · Rubicón EAS"
  ✓ /assets/styles.css         23,161 bytes  CSS
  ✓ /assets/main.js             2,375 bytes  JS
  ✓ /assets/content.es.json    18,473 bytes  Source-of-truth JSON

Worker:  rubicon-eas-site in CF account 9eb1832f3e42a1dbd6ba854f8d6a1cb2
R2:      s3://ai-whisperers-backups/rubicon-eas/ (12 files, 134KB)
DNS:     rubiconeas.paragu-ai.com → 38.9.96.179 (proxied, Worker route)
Status:  ALL GREEN
```

---

## Y si el cliente lo ve antes que nosotros

Eso es el demo. Funciona. Comparte el URL.
