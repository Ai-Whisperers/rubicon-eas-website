# MODELO DE FACTURA / COMPROBANTE DE VENTA
## Dra. Gabriella González Pane — E.A.S.

---

**NOTA:** Este es un modelo de estructura. La emisión real requiere Timbrado activo obtenido de la SET. No emitir comprobantes sin Timbrado válido.

---

```
================================================================================
                              [TIMBRE FISCAL]
================================================================================

          GONZÁLEZ PANE SERVICIOS ODONTOLÓGICOS E.A.S.
          RUC: [RUC DE LA EMPRESA]
          Dirección: [DIRECCIÓN — cuando esté confirmada]
          Timbrado N°: [NÚMERO DE TIMBRADO]
          Inicio validez: [FECHA]
          Fin validez: [FECHA]

================================================================================

FACTURA ELECTRÓNICA

N°: 001-001-[NÚMERO CORRELATIVO]
Fecha: [FECHA]
Timbreado serie: [SERIE]

--------------------------------------------------------------------------------
DATOS DEL CONTRIBUYENTE / PACIENTE

Nombre/Razón Social: [NOMBRE DEL PACIENTE]
RUC/CI: [CÉDULA O RUC DEL PACIENTE]
Dirección: [DIRECCIÓN DEL PACIENTE — si aplica]
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
DETALLE DE SERVICIOS

  N° | Descripción                           | Cant. | P.Unitario   | Total
-----|--------------------------------------|-------|--------------|-------
  1  | Consulta odontológica                 |   1   | Gs [PRECIO]  | Gs [TOTAL]
  2  | [PROCEDIMIENTO]                      |   1   | Gs [PRECIO]  | Gs [TOTAL]
  3  |                                       |       |              |
     |                                       |       |              |
     |                                       |       |              |
     |                                       |       |              |
--------------------------------------------------------------------------------
                                    SUBTOTAL:   Gs [SUBTOTAL]
                                    IVA (10%):  Gs [IVA]
                                    TOTAL:      Gs [TOTAL A PAGAR]

--------------------------------------------------------------------------------
FORMA DE PAGO

[ ] Efectivo
[ ] Transferencia bancaria — Banco [BANCO], CTA [NÚMERO]
[ ] Tarjeta — Pagopar / Bancard
[ ] Cuotas — [NÚMERO] cuotas sin interés

--------------------------------------------------------------------------------
SON: [MONTO EN LETRAS]

================================================================================

Condiciones:
- Este comprobante es válido solo con Timbrado activo de la SET
- Los procedimientos realizados tienen garantía según términos publicados
- Para ejercicio de garantía, conservar este comprobante

Dra. Gabriella González Pane
Matrícula COP N°: [NÚMERO]

================================================================================
```

---

## NOTAS SOBRE FACTURACIÓN

### Timbrado
1. Obtener Timbrado en línea desde SET: servicios.set.gov.py
2. Solicitar serie de comprobantes (facturas, tickets, notas de crédito)
3. Cada comprobante debe incluir número de Timbrado y fechas de validez
4. Vencido el Timbrado, no emitir comprobantes hasta renovarlo

### IVA
- IVA general: 10% en Paraguay
- Algunos servicios de salud pueden estar exentos — consultar con contador

### Facturación Electrónica
- Paraguay tiene sistema de facturación electrónica (e-KUY)
- Para E.A.S. con bajo volumen, la SET permite facturación simplificada
- Consultar con contador la mejor opción para el volumen de la práctica

### Números Correlativos
- Formato: 001-001-000001 (establecimiento-serie-correlativo)
- Mantener libro de ventas con todos los comprobantes emitidos
- Conservar por 5 años mínimo según normativa SET

---

**STATUS:** Templates complete. Full invoicing requires: (1) E.A.S. registered, (2) RUC activo, (3) Timbrado solicitado, (4) Software de facturación o Portal SET. Consult with accountant before first billing.