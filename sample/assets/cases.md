# Detalle de Casos — Rubicón EAS

Cuando el cliente apruebe los casos reales, cada uno tendrá su propia URL:

```
/casos/civil-001-reestructuracion-comercial
/casos/civil-002-sucesion-compleja
/casos/penal-003-defensa-delito-economico
/casos/penal-004-defensa-flagrancia
/casos/penal-008-apelacion-recurso
/casos/ambiental-005-infraccion-administrativa
/casos/ambiental-006-derecho-aguas
/casos/ambiental-009-cumplimiento-corporativo-esg
/casos/civil-007-responsabilidad-civil
```

## Estructura de página de detalle

```markdown
# [Subárea] — [título del caso]

**Cliente:** [tipo — PyME, persona, corporativo]
**Jurisdicción:** [lugar]
**Año:** [año]
**Resultado:** [resumen en 1 línea]

## Contexto
[100-200 palabras]

## Estrategia
[100-200 palabras]

## Resultado
[100-200 palabras cuantificando]

## Duración
[N meses]

## Áreas relacionadas
[lista]
```

## Schema.org

```json
{
  "@context": "https://schema.org",
  "@type": "LegalCase",
  "name": "Caso civil-001",
  "outcome": "Acuerdo homologado",
  "dateModified": "2024-12-15",
  "provider": {
    "@type": "Attorney",
    "name": "Dr. Juan María Pérez"
  }
}
```

## Pendiente

- [ ] Cliente aprueba qué casos se publican
- [ ] Cliente confirma anonimización
- [ ] Erebus crea las páginas individuales
- [ ] Wire schema LegalCase
- [ ] Wire OG image por caso
