#!/usr/bin/env python3
"""
Rubicón EAS — Content Generator
Generates ready-to-fill templates for LinkedIn, blog, GBP, newsletter.

Run: python3 scripts/generate-content.py [--area civil|penal|ambiental] [--count N]
Output: marketing/generated/ directory with .md files
"""
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# ==== DATA ====
SITE = {
    "name": "Rubicón EAS",
    "tagline": "Justicia con criterio. Defensa con oficio.",
    "matricula_csj": "Matrícula CSJ N° 23.456",
    "matricula_cap": "Colegio de Abogados del Paraguay N° 8.921",
    "phone": "+595 21 123 456",
    "whatsapp": "+595 981 234 567",
    "email": "contacto@rubiconeas.com.py",
    "address": "Av. Mariscal López 1234, Piso 8 Of. 803, Asunción",
}

AREAS = {
    "civil": {
        "name": "Derecho Civil",
        "description": "Contratos, sucesiones, responsabilidad civil, propiedad, derecho comercial",
        "subareas": [
            "Contratos civiles y comerciales",
            "Responsabilidad civil extracontractual",
            "Sucesiones y planificación patrimonial",
            "Propiedad, reivindicación y prescripción",
            "Reestructuración de deuda para PyMEs",
            "Litigios civiles y comerciales",
            "Derecho de familia",
            "Derecho inmobiliario",
        ],
        "common_questions": [
            "¿Cuánto tarda un juicio civil en Paraguay?",
            "¿Qué pasa si no pago una deuda?",
            "¿Cómo se hace una sucesión sin testamento?",
            "¿Puedo reclamar daños por incumplimiento de contrato?",
            "¿Qué es la prescripción adquisitiva?",
            "¿Cómo saber si un contrato es legal?",
            "¿Puedo rescindir un alquiler antes de tiempo?",
            "¿Cómo hacer un poder general?",
        ],
        "case_topics": [
            "Reestructuración comercial",
            "Sucesión compleja",
            "Responsabilidad civil",
            "Prescripción adquisitiva",
            "Incumplimiento contractual",
            "Derecho de familia",
        ]
    },
    "penal": {
        "name": "Derecho Penal",
        "description": "Defensa penal estratégica en todas las etapas del proceso. Atención inmediata en flagrancia.",
        "subareas": [
            "Defensa en instrucción e intermedia",
            "Juicio oral y recursos",
            "Asistencia al detenido en flagrancia",
            "Querellas y denuncias",
            "Delitos económicos y funcionarios",
            "Medidas cautelares y libertad ambulatoria",
            "Ejecución penal",
            "Compliance penal corporativo",
        ],
        "common_questions": [
            "¿Qué hago si me detienen?",
            "¿Cuándo prescribe un delito en Paraguay?",
            "¿Puedo salir bajo fianza?",
            "¿Qué es el juicio abreviado?",
            "¿Cuánto tarda un proceso penal?",
            "¿Puedo apelar una condena?",
            "¿Qué es la suspensión condicional del procedimiento?",
            "¿Cómo funciona la probation?",
        ],
        "case_topics": [
            "Defensa por delito económico",
            "Asistencia en flagrancia",
            "Apelación y recurso",
            "Absolución",
            "Sobreseimiento",
            "Probation",
        ]
    },
    "ambiental": {
        "name": "Derecho Ambiental",
        "description": "Asesoramiento integral en cumplimiento, infracciones administrativas y litigio ambiental.",
        "subareas": [
            "Evaluación de impacto ambiental",
            "Infracciones administrativas y recursos",
            "Derecho de aguas y recursos naturales",
            "Deforestación y áreas protegidas",
            "Cumplimiento corporativo ESG",
            "Mediación y resolución de conflictos",
            "Derecho minero y energético",
            "Cambio climático y regulación",
        ],
        "common_questions": [
            "¿Cómo funciona el proceso de EIA en Paraguay?",
            "¿Qué pasa si deforeto sin permiso?",
            "¿Cómo recurrir una multa del MADES?",
            "¿Qué es el derecho de aguas en Paraguay?",
            "¿Cómo evitar infracciones ambientales en una empresa?",
            "¿Qué obligaciones ESG tiene mi empresa?",
            "¿Cómo funciona la Ley 294/93?",
            "¿Puedo mediar un conflicto ambiental?",
        ],
        "case_topics": [
            "Infracción administrativa",
            "Derecho de aguas",
            "Cumplimiento corporativo ESG",
            "Deforestación",
            "Concesión minera",
            "Residuos industriales",
        ]
    }
}

# ==== TEMPLATES ====

def linkedin_long(area, topic):
    a = AREAS[area]
    return f"""# LinkedIn — Artículo largo ({a['name']})

**Fecha de publicación:** [Lunes semana X]
**Longitud:** 800-1500 palabras
**CTA:** Consulta inicial

## Título (max 100 chars)
[Pregunta fuerte o afirmación con keyword]

## Hook (primeras 2 líneas)
"¿Sabías que [dato impactante sobre {a['name'].lower()} en Paraguay]?"

## Estructura
1. **Contexto** (3 párrafos)
   - Por qué este tema importa
   - Marco legal aplicable (leyes PY relevantes)
   - Dato oficial (CSJ, MADES, etc.)

2. **Insight** (2 párrafos)
   - Lo que la mayoría no sabe
   - Error común

3. **Solución** (lista numerada, 3-5 puntos)
   - Acción concreta 1
   - Acción concreta 2
   - Acción concreta 3

4. **Cierre** (1 párrafo + pregunta)
   - Reflexión final
   - Pregunta abierta para engagement

## Keywords a incluir
- {a['name']}
- {a['name']} Paraguay
- [ciudad] (Asunción, Central, etc.)

## Hashtags (5-7)
#{a['name'].replace(' ', '')} #Paraguay #Asunción #abogadoPY #derecho

## Llamada a la acción final
"En Rubicón EAS asesoramos en {a['name']}. Primera consulta bonificada si contratamos. WhatsApp: {SITE['whatsapp']}"

## Disclaimer
"La información publicada no constituye asesoramiento jurídico. Para conferir una consulta formal, agende una cita."
"""

def linkedin_short(area, topic):
    a = AREAS[area]
    return f"""# LinkedIn — Análisis corto ({a['name']})

**Fecha:** Miércoles semana X
**Longitud:** 200-400 palabras

## Estructura

[Sentencia / tema] — [1 línea resumen en activo]

Contexto (3 líneas):
Qué pasó, cuándo, dónde, quién. Cita textual del fallo si la tenés.

Por qué importa (2 líneas):
Relevancia para clientes PY. Por qué debería importarte.

Lo que cambia en la práctica (3 líneas):
Implicación concreta. Qué significa para tu próxima decisión legal.

[Pregunta para engagement]
¿Conocías este caso? ¿Cómo lo manejas en tu estudio?

## Hashtags
#{a['name'].replace(' ', '')} #paraguay #derecho #asuncion
"""

def linkedin_visual(area, topic):
    return f"""# LinkedIn — Visual (foto)

**Fecha:** Viernes semana X
**Foto:** [Fachada / oficina / firma / evento]
**Tamaño:** 1200x627 px (link preview) o 1080x1080 px (cuadrado)

## Caption (50-100 palabras)

[Foto adjunta]

[1 frase de contexto sobre la imagen]
[2 frases de insight profesional]

#abogadoasuncion #paraguay #derecho
"""

def blog_post(area, keyword):
    a = AREAS[area]
    return f"""# Blog — Artículo SEO

**Keyword objetivo:** {keyword}
**URL slug:** /blog/{keyword.lower().replace(' ', '-')}
**Longitud:** 1200-1800 palabras
**Meta description:** [150 chars con keyword + Asunción]
**Schema.org:** BlogPosting + Article

## H1
{keyword.title()} en Paraguay: guía completa [año actual]

## H2 secciones (3-5)

### ¿Qué es [tema]? (250 palabras)
[Definición legal, marco normativo PY, casos típicos]

### ¿Cuándo aplica? (300 palabras)
[Escenarios comunes, jurisprudencia relevante]

### Marco legal en Paraguay (350 palabras)
[Ley X/YY, decreto Z, Constitución artículos relevantes]

### Procedimiento paso a paso (350 palabras)
[Timeline, costos aproximados, documentos necesarios]

### Preguntas frecuentes (300 palabras)
[Listar 4-5 preguntas sobre {a['name'].lower()}]

## Conclusión + CTA
"¿Necesita asesoramiento en {a['name'].lower()}? Agende una consulta: {SITE['whatsapp']}"

## Schema.org JSON-LD
```json
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "...",
  "datePublished": "...",
  "author": {{"@type": "Person", "name": "Dr. Juan María Pérez"}},
  "publisher": {{"@type": "Organization", "name": "Rubicón EAS"}}
}}
```
"""

def gbp_post(area, theme):
    return f"""# Google Business Profile — Post semanal

**Fecha:** [día semana]
**Imagen:** 1080x1080 px (cuadrada) o 1200x900 px

## Texto (500-1500 caracteres)

[Hook: pregunta o afirmación]

[Contexto: lo que el cliente necesita saber]

[Valor: insight útil, no venta]

[CTA: contactenos]

#abogadoasuncion #{area}asuncion
"""

def newsletter_issue(month, theme):
    return f"""# Newsletter #{month} — {theme}

**Subject lines (A/B test):**
A: "{theme} — y otras cosas que importan este mes"
B: "Caso del mes: {theme}"

## Estructura

### Hola Dr. Pérez,
[1 párrafo de bienvenida con tu voz]

### Esto es lo que escribimos este mes
- [Link post LinkedIn 1]
- [Link post LinkedIn 2]
- [Link artículo blog 1]

### Caso del mes (anonimizado)
[2-3 párrafos contando un caso real, anonimizado, con el resultado]

### Cambio legislativo relevante
[Si hay algo reciente del Congreso o la CSJ]

### Próximas fechas
- [Eventos, conferencias, etc.]

### ¿Necesitas asesoramiento?
[CTA claro: "Agenda una consulta"]

---
Dr. Juan María Pérez · {SITE['matricula_csj']}
Rubicón EAS · {SITE['address']}
WhatsApp: {SITE['whatsapp']}
"""

# ==== MAIN ====

def main():
    parser = argparse.ArgumentParser(description="Generate Rubicón EAS content templates")
    parser.add_argument("--area", choices=list(AREAS.keys()) + ["all"], default="all")
    parser.add_argument("--count", type=int, default=5, help="Items per area per type")
    parser.add_argument("--output", default="marketing/generated")
    args = parser.parse_args()

    areas = list(AREAS.keys()) if args.area == "all" else [args.area]
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    generators = [
        ("linkedin-long", linkedin_long),
        ("linkedin-short", linkedin_short),
        ("linkedin-visual", linkedin_visual),
        ("blog-post", blog_post),
        ("gbp-post", gbp_post),
        ("newsletter-issue", newsletter_issue),
    ]

    total = 0
    for area in areas:
        a = AREAS[area]
        for name, gen in generators:
            count = args.count
            for i in range(count):
                if name == "newsletter-issue":
                    theme = a["subareas"][i % len(a["subareas"])]
                    content = gen(i + 1, f"{a['name']}: {theme}")
                else:
                    # Use a subarea or common question as topic
                    sources = a["subareas"] + a["common_questions"] + a["case_topics"]
                    topic = sources[i % len(sources)]
                    if name == "blog-post":
                        content = gen(area, topic)
                    else:
                        content = gen(area, topic)
                # Replace the placeholder section header
                # Write file
                fn = out_dir / f"{area}-{name}-{i+1:02d}.md"
                with open(fn, "w") as f:
                    f.write(content)
                total += 1

    print(f"✓ Generated {total} templates in {out_dir}")
    print(f"\nBreakdown:")
    for area in areas:
        count = sum(1 for _ in out_dir.glob(f"{area}-*"))
        print(f"  {area}: {count} files")

if __name__ == "__main__":
    main()
