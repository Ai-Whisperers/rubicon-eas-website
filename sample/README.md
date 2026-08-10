# Rubicón EAS — Sample Website Reference

This is the **sample website template** that demonstrates what a fully-built client
site looks like. It contains **all** the content a legal firm needs:

- Hero + value proposition
- Practice areas (Civil, Penal, Ambiental) with separate landing pages
- About / Credentials with Matrícula CSJ
- Case studies anonymized
- FAQ (15+ items)
- Testimonials
- Lead intake form (Hermes triage)
- Contact + WhatsApp handoff
- Legal disclaimer
- Multilingual sitemap ready

The content here is **fictional placeholder**. The client fills out the
`intake/01-10-*.json` questionnaire and Erebus replaces this content with real
copy. The structure stays — the words change.

## Architecture

```
sample/
├── index.html                  # Home
├── derecho-civil.html          # Civil law landing
├── derecho-penal.html          # Penal law landing
├── derecho-ambiental.html      # Ambiental law landing
├── nosotros.html               # About the attorney
├── casos.html                  # Case studies portfolio
├── contacto.html               # Contact + lead form
├── blog.html                   # Articles (stub)
├── assets/
│   ├── styles.css
│   ├── main.js
│   └── content.es.json         # Source of truth (clau-bellino pattern)
└── README.md                   # This file
```

## How to read this

1. Open `index.html` in a browser — that's the live preview.
2. Compare every section with the matching questionnaire file in `intake/`.
3. Every `{{placeholder}}` in the HTML corresponds to a real question in the
   questionnaire. Send the client the questionnaire, replace the placeholders
   with their answers, the site is ready.

## Content source

`assets/content.es.json` is the canonical source of truth. The HTML files
inline-reference this structure. To change copy, edit the JSON and re-run the
build script (or hand-edit the HTML — at this size either is fine).

## Live preview

This sample is deployed at `rubiconeas.paragu-ai.com` — see parent plan
`/opt/data/plans/2026-08-10-rubicon-eas-build.md` for the deploy mechanics.
