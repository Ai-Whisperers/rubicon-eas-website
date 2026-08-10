# Rubicón EAS — Project Tracker

> **Estado del proyecto al 2026-08-10.**
> **Owner:** Erebus. **Cliente:** Dr. Juan María Pérez González.

## Resumen

| Fase | Estado | % | Bloqueante |
|---|---|---|---|
| 1. Demo sitio | ✅ Live | 100% | — |
| 2. Brief intake | 🟡 56% respondido | 56% | cliente |
| 3. Lead pipeline | ✅ Live | 100% | — |
| 4. CI/CD | ✅ Live | 100% | — |
| 5. Compliance docs | ✅ Plantillas | 90% | cliente |
| 6. Brand assets | 🟡 DRAFT | 30% | cliente |
| 7. Copy final | 🟡 Placeholder | 50% | cliente |
| 8. Producción (próximo) | ⚪ No iniciado | 0% | cliente |
| **TOTAL** | **🟡 53%** | **53%** | **bloqueado en cliente** |

## Bloqueantes activos

| # | Bloqueante | Owner | Critical |
|---|---|---|---|
| 1 | Partner bio + foto | cliente | CRITICAL |
| 2 | Matrícula CSJ + Colegio | cliente | CRITICAL |
| 3 | WhatsApp institucional | cliente | CRITICAL |
| 4 | Casos anonimizados | cliente | CRITICAL |
| 5 | Domain `rubiconeas.com.py` | cliente | CRITICAL |
| 6 | Logo + brand manual | cliente | HIGH |
| 7 | Honorarios (publicar o no) | cliente | HIGH |
| 8 | Consentimiento tratados del Colegio | cliente | MEDIUM |

## Status detallado

### 1. Demo sitio (✅ 100%)

- [x] Repo creado: `Ai-Whisperers/rubicon-eas-website` (público)
- [x] Issue #1 con checklist
- [x] 8 páginas HTML corriendo en `rubiconeas.paragu-ai.com`
- [x] 290-question intake estructurado
- [x] Propuesta comercial 3-tier
- [x] 55 docs de referencia legal
- [x] Master plan (PLAN-DE-PREPARACION.md)

### 2. Brief intake (🟡 56%)

- [x] 290 preguntas estructuradas (10 JSON files)
- [x] 195 required fields
- [x] 39 answered (placeholder / example)
- [x] 156 unanswered (cliente debe llenar)
- [ ] **Cliente responde intake** — bloqueado

### 3. Lead pipeline (✅ 100%)

- [x] CF Worker `rubicon-eas-lead` deployed
- [x] Endpoint: `POST /api/lead`
- [x] Validación: name, phone, email, area, summary
- [x] Clasificación: PENAL=URGENT, CIVIL=AMBIENTAL=NORMAL
- [x] Markdown brief format
- [x] Honeypot anti-bot
- [x] KV logging (90-day)
- [x] Frontend form wired
- [ ] **Production webhook** (n8n deployment) — espera cliente

### 4. CI/CD (✅ 100%)

- [x] `validate-intake.py` — JSON schema (10 files, 290 questions valid)
- [x] `check-required.py` — required fields tracker
- [x] `validate-content.py` — content schema
- [x] `trademark-scrub.py` — Hostinger banlist (word-boundary)
- [x] `smoke-test.py` — live URL probe
- [x] `validate.yml` workflow (5 jobs)
- [x] Live smoke test: 10/10 pages serve

### 5. Compliance docs (✅ 90%)

- [x] Templates listos:
  - `legales/03-EAS-Constitution-Template.md` (16.6 KB)
  - `legales/04-EAS-Formation-Plan.md` (22.4 KB)
  - `legales/05-Paraguay-Corporate-Forms-Comparison.md`
  - `legales/09-Privacy-Policy-Template.md` (9.3 KB)
  - `legales/12-Data-Protection-Policy.md` (12.2 KB)
- [x] Ley 1682/01 + GDPR-style compliance listo
- [ ] **Cliente revisa + aprueba** — bloqueado

### 6. Brand assets (🟡 30%)

- [x] Paleta navy + bronze (DRAFT)
- [x] Tipografía Source Serif 4 + Inter (DRAFT)
- [x] Logo placeholder
- [ ] **Logo real** — bloqueado en cliente
- [ ] **Foto del abogado** — bloqueado

### 7. Copy final (🟡 50%)

- [x] Hero placeholder
- [x] 3 practice areas con contenido
- [x] 9 case studies (placeholder)
- [x] 15 FAQ (draft)
- [x] Disclaimer legal
- [ ] **Bio real abogado** — bloqueado
- [ ] **Casos anonimizados reales** — bloqueado
- [ ] **Tarifas reales** — bloqueado

### 8. Producción (⚪ 0%)

- [ ] Fork `escribania-paraguay` → `Ai-Whisperers/rubicon-eas`
- [ ] Build Next.js
- [ ] Deploy Host A Swarm + Traefik + LE
- [ ] Bind `rubiconeas.com.py`
- [ ] Wire n8n webhook
- [ ] Configure Evolution API

## Métricas

| Metric | Value |
|---|---|
| Total preguntas | 290 |
| Required | 195 |
| Answered (placeholder) | 39 |
| **Answered (real)** | 0 |
| **% complete** | 0% real, 56% placeholder |
| Documentos preparados | 56 (intake + reference + plan) |
| Líneas de código | 0 → ~3000 (cuando arranque) |
| ETA al go-live | 5 días hábiles post-intake |

## Próximos pasos (orden)

1. ✋ **Cliente completa `intake/01-10-*.json`** con respuestas reales
2. ✋ **Cliente** envía: hoja de vida, foto, logo, diploma, matrícula
3. ✋ **Cliente** confirma: WhatsApp línea, dominio, dirección, horarios
4. 🚀 **Erebus** arranca: fork escribania-paraguay, build, deploy
5. 🚀 **Erebus** wire: n8n → Evolution API → WhatsApp
6. 🚀 **Erebus** deploy: Host A Swarm + Traefik + LE
7. 🚀 **Erebus** UAT con cliente
8. 🚀 **Handoff** + soporte 30 días

## Lo que puedo hacer sin cliente

- [ ] Fork y dejé el sitio production-ready en un branch
- [ ] Configurar n8n workflow sin webhook live
- [ ] Crear los Evolution API sandboxes
- [ ] Escribir los 4 manuales de operación para el abogado
- [ ] Preparar el Slack/Telegram bridge para el abogado
- [ ] Auditar la competencia en línea (cliente pidió)

## Critical path

```
cliente.intake → 5 días hábiles → producción
   ↓                       ↓
   0% hoy                 100% en 5 días
```

**El único bloqueante es el cliente.**

## Referencias

| Doc | URL |
|---|---|
| Plan maestro | `PLAN-DE-PREPARACION.md` |
| Propuesta | `propuesta/PROPUESTA-COMERCIAL.md` |
| Brief | `intake/01-10-*.json` |
| Issue #1 | https://github.com/Ai-Whisperers/rubicon-eas-website/issues/1 |
| Live | https://rubiconeas.paragu-ai.com/ |
| Repo | https://github.com/Ai-Whisperers/rubicon-eas-website |

---

*Snapshot 2026-08-10 23:08 UTC. Auto-refresh: run `python3 scripts/check-required.py`.*
