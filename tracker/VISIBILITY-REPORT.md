# Rubicón EAS — Visibility & Outreach — DELIVERED 2026-08-10

## 1 resumen

**Pregunta del cliente:** "how can we setup visibility and outreach"

**Respuesta:** Construí 4 entregables ejecutables + 1 dashboard live + 60 docs de referencia de Ometz Dental adaptados a legal vertical.

## Entregables

### A. Documentos estratégicos
| Doc | Tamaño | Para qué |
|---|---|---|
| `marketing/PLAYBOOK.md` | 22.8KB · 546 líneas · 3,789 palabras · 74 secciones | Plan maestro de visibilidad |
| `marketing/CONTENT-CALENDAR.md` | 9.5KB · 244+ slots de contenido | Calendario 12 meses |
| `marketing/CHANNELS-SUMMARY.md` | 4.0KB · 1 página resumen | Vista executive |

### B. Reference material adaptado
| Folder | Contenido |
|---|---|
| `marketing/ometz-reference/` | 60 archivos · 561KB · SEO local, Meta Ads, Doctoralia, GBP, Instagram, LinkedIn, WhatsApp, referral program, content calendar, B2B institutional sales |

### C. Tooling de generación
| Script | Tamaño | Función |
|---|---|---|
| `scripts/generate-content.py` | 12KB | Genera 54 templates listos para llenar |
| `scripts/red-colegas.py` | 7KB | CLI para gestión de red de derivaciones |
| `scripts/outreach-templates.py` | 7.4KB | 6 plantillas de WhatsApp + email |
| `marketing/generated/*.md` | 42KB · 54 archivos | Templates pre-armados |

### D. Dashboard live
| URL | Función |
|---|---|
| https://rubiconeas.paragu-ai.com/red-colegas.html | CRM local de colegas (localStorage) |

## Cobertura de canales (10 canales)

| # | Canal | ROI | Costo | Mes de inicio |
|---|---|---|---|---|
| 1 | Google Business Profile | Muy alto | Gs. 0 | Mes 1 |
| 2 | Directorios jurídicos (8+) | Alto | Gs. 0 | Mes 1-2 |
| 3 | Red de colegas | Muy alto (mes 6+) | Gs. 50k/mes | Mes 1 |
| 4 | LinkedIn personal | Medio-alto | Gs. 0 | Mes 1 |
| 5 | SEO local | Muy alto (compuesto) | Gs. 200k/mes | Mes 1-3 |
| 6 | WhatsApp Business App | Alto inmediato | Gs. 0 | Mes 1 |
| 7 | WhatsApp Business API | Alto (mes 4+) | Gs. 100-300k setup | Mes 4+ |
| 8 | Google Ads | Alto (intención) | Gs. 1.5M/mes | Mes 4+ |
| 9 | Meta Ads | Medio | Gs. 1M/mes | Mes 4+ |
| 10 | Email / Newsletter | Bajo al inicio | Gs. 0 | Mes 6+ |

## Canales NO recomendados (2026)

- Print (diarios, folletos) — alto costo, baja segmentación
- Radio AM/FM — masivo, no medible
- TV — completamente fuera de rango
- LinkedIn Premium — no se justifica
- TikTok / Instagram para legal — audiencia no profesional suficiente
- Twitter/X — no es el canal en PY

## Compliance Colegio de Abogados PY

- PROHIBIDO: claims superlativos ("los mejores", "garantizamos")
- PROHIBIDO: promesas de resultado
- PROHIBIDO: comparaciones directas con otros estudios
- REQUERIDO: Matrícula CSJ visible
- REQUERIDO: Política de Privacidad
- REQUERIDO: Disclaimer "no constituye asesoramiento jurídico"

## KPIs por mes

### Mes 1
- GBP verificado + 5 reseñas
- 8+ directorios registrados
- LinkedIn perfil completo
- WhatsApp Business App
- 5 colegas contactados
- 1 artículo blog

### Mes 3
- 15+ reseñas
- 500+ conexiones LinkedIn
- 10+ posts LinkedIn
- 6+ artículos blog
- 3 acuerdos derivación
- 5 leads/mes (orgánico)

### Mes 6
- 30+ reseñas, top 10
- 1000+ conexiones LinkedIn
- 30+ posts LinkedIn
- 12+ artículos blog
- 10+ acuerdos derivación
- 10+ leads/mes (mixto)
- Newsletter activo

### Mes 12
- 50+ reseñas, top 3
- 2000+ conexiones LinkedIn
- 100+ posts LinkedIn
- 48+ artículos blog
- 20+ colegas
- 30+ leads/mes
- 500 subs newsletter

## Costos anuales

| Tier | Setup | Mensual | Esperado |
|---|---|---|---|
| Plan A (mínimo viable) | Gs. 100k | Gs. 50-100k | 5 leads/mes mes 6 |
| Plan B (recomendado) | Gs. 200-500k | Gs. 200-400k | 5-10 leads/mes mes 6 |
| Plan C (agresivo) | Gs. 1-2M | Gs. 3-5M | 20-30 leads/mes mes 6 |

## Próximos pasos

1. **Cliente revisa `marketing/PLAYBOOK.md`** y aprueba
2. **Cliente revisa `marketing/CONTENT-CALENDAR.md`** y edita
3. **Cliente elige tier** (A/B/C)
4. **Erebus ejecuta** setup correspondiente
5. **Setup de contenido:** content-editor opcional o interno
6. **Tracking mensual** de KPIs

## Referencia de Ometz Dental (60 docs)

El cliente puede leer cualquiera de estos para entender el "qué" y "por qué" detrás de cada canal. Los más importantes:

- `marketing/ometz-reference/06_MARKETING__digital-marketing-playbook.md`
- `marketing/ometz-reference/06_MARKETING__google-business-profile-setup-guide.md`
- `marketing/ometz-reference/06_MARKETING__meta-ads-playbook.md`
- `marketing/ometz-reference/06_MARKETING__influencer-marketing-ecosystem.md`
- `marketing/ometz-reference/03_LAUNCH__referral-program__referral-program-plan.md`
- `marketing/ometz-reference/03_LAUNCH__institutional-sales__institutional-sales-playbook.md`
- `marketing/ometz-reference/01_RESEARCH__marketing__DG03_dental_marketing_patient_acquisition_2026-07-06.md`

## Scripts ejecutables

### Generar 54 templates de contenido
```bash
python3 scripts/generate-content.py --area all --count 5
# Output: marketing/generated/*.md
```

### Red de colegas CRM
```bash
python3 scripts/red-colegas.py init
python3 scripts/red-colegas.py add "Dr. García" "Estudio García" civil +595 9XX
python3 scripts/red-colegas.py update "Dr. García" acuerdo
python3 scripts/red-colegas.py report
```

### Outreach templates
```bash
python3 scripts/outreach-templates.py colega "Dr. X" "Estudio" civil
python3 scripts/outreach-templates.py review "Cliente" civil
python3 scripts/outreach-templates.py reactivate "Cliente" 180 civil
```

## Live URLs

- https://rubiconeas.paragu-ai.com/ (sitio principal)
- https://rubiconeas.paragu-ai.com/red-colegas.html (CRM colegas)
- https://rubiconeas.paragu-ai.com/sitemap.xml (10 URLs)
- https://rubiconeas.paragu-ai.com/robots.txt (noindex admin/api/red-colegas)

## Repo state

- 12 commits este session
- 150+ archivos tracked
- 100% de los deliverables de marketing/outreach live

---

*Erebus — 2026-08-10 23:55 UTC*
