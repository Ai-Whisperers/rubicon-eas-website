#!/usr/bin/env python3
"""
Rubicón EAS — Templates de Outreach
Genera los mensajes de primer contacto, follow-up, derivación, etc.
"""
from datetime import datetime, timedelta

# === DATA ===
SITE = {
    "name": "Rubicón EAS",
    "abrev": "REAS",
    "abogado": "Dr. Juan María Pérez González",
    "ciudad": "Asunción",
    "whatsapp": "+595 981 234 567",
    "email": "contacto@rubiconeas.com.py",
    "direccion": "Av. Mariscal López 1234, Piso 8 Of. 803, Asunción",
    "matricula": "Matrícula CSJ N° 23.456",
    "colegio": "Colegio de Abogados del Paraguay N° 8.921",
}

# === TEMPLATES ===

def whatsapp_colega(nombre, estudio, area="civil", idioma="es"):
    """Primer contacto: colega abogado."""
    if idioma == "es":
        return f"""Estimado/a {nombre},

Mi nombre es Juan María Pérez, abogado, fundé recientemente Rubicón EAS en Asunción (Matrícula CSJ N° 23.456, Colegio de Abogados N° 8.921).

Trabajo principalmente en {area.title()} y estoy armando una red de colegas para derivaciones recíprocas. La idea es simple: si me llega un caso que no es mi especialidad, le paso al colega más indicado, y viceversa.

¿Le parece si coordinamos un café la próxima semana para conocernos? Puedo llevar el mate.

Saludos,
Dr. Juan María Pérez
Rubicón EAS
{SITE['whatsapp']}"""
    else:
        return f"""Dear {nombre},

My name is Juan María Pérez, attorney-at-law. I recently founded Rubicón EAS in Asunción (Paraguay). I focus primarily on {area.title()} law and I'm building a network of colleague-lawyers for mutual referrals.

If you have a case outside your specialty, I refer to you. If I have one outside mine, I send it to you. No money changes hands — just trust.

Coffee next week? I can bring the mate (it's our thing here).

Best,
Dr. Juan María Pérez
Rubicón EAS
{SITE['whatsapp']}"""

def whatsapp_cliente_post_caso(nombre, area="civil"):
    """Después de cerrar caso: pedir reseña Google."""
    if area == "penal":
        msg = "Como abogado penalista entiendo que estos procesos son estresantes y privados"
    elif area == "ambiental":
        msg = "Como especialista en derecho ambiental, mi práctica depende de la confianza de las empresas y productores"
    else:
        msg = "Como abogado, mi práctica depende de la confianza de clientes que me recomiendan"

    return f"""Estimado/a {nombre},

Confío en que haya quedado conforme con el trabajo realizado.

Como usted sabe, {msg}. Si tuvo una experiencia satisfactoria, le agradecería mucho que me dejara una breve reseña en Google. Es de gran ayuda para que otros clientes potenciales puedan conocerme.

Aquí está el enlace: [LINK_GOOGLE_REVIEWS]

Si prefiere no dejar reseña, lo entiendo perfectamente. Y si tiene cualquier observación sobre cómo puedo mejorar mi servicio, estoy a disposición.

Gracias por confiar en Rubicón EAS.

Un cordial saludo,
Dr. Juan María Pérez
{SITE['whatsapp']}"""

def whatsapp_cliente_reactivar(nombre, dias_sin_contacto=180, area="civil"):
    """Cliente que no contacta hace tiempo. Reactivar con valor, no venta."""
    return f"""Estimado/a {nombre},

Espero que esté bien. Soy el Dr. Juan María Pérez de Rubicón EAS.

Hace un tiempo trabajamos juntos en su caso de {area.title()}. No escribo para venderle nada — escribo porque noté que hay [un cambio legislativo / un nuevo plazo / un artículo relevante para su situación] y quería compartirlo con usted por si es de su interés.

[Enlace al artículo o cambio]

Sin compromiso. Si le interesa conversar, agendamos cuando quiera.

Saludos,
Dr. Juan María Pérez
{SITE['whatsapp']}"""

def whatsapp_empresa_intro(nombre_contacto, nombre_empresa, sector="PyME"):
    """Primer contacto con una empresa (B2B)."""
    return f"""Estimado/a {nombre_contacto},

Mi nombre es Juan María Pérez, abogado de Rubicón EAS. Trabajo con empresas del sector {sector} en Paraguay en temas de derecho civil, comercial y ambiental.

Vi que [NOMBRE_EMPRESA] está [creciendo / lanzando nuevo producto / expandiendo]. En este tipo de etapas, contar con asesoramiento legal preventivo ahorra costos significativos más adelante.

¿Le parece si agendamos una llamada de 15 minutos esta semana para presentarle mi trabajo y ver si puede serle útil? Sin compromiso.

Saludos,
Dr. Juan María Pérez
Rubicón EAS · {SITE['matricula']}
{SITE['whatsapp']}
www.rubiconeas.com.py"""

def whatsapp_referral_request(nombre, nombre_colega, area="civil"):
    """Pedir derivación a un colega cuando se da el caso."""
    return f"""Estimado/a {nombre},

Le paso un caso que no es de mi área principal pero que es muy de su especialidad.

[Tema del caso anonimizado]

¿Le interesa? Si necesita más detalle, le envío por este medio o agendamos una llamada de 5 minutos.

Saludos,
Dr. Juan María Pérez
{SITE['whatsapp']}"""

def email_newsletter_invite(nombre, lead_source="colega"):
    """Email de invitación a la newsletter mensual."""
    return f"""Asunto: Actualidad jurídica + 1 caso del mes [mes]

Estimado/a {nombre},

Soy el Dr. Juan María Pérez, abogado en Asunción. Hace unos meses tuvimos contacto a través de {lead_source}.

Le escribo porque voy a publicar una newsletter mensual con:

1. Cambios legislativos relevantes del mes
2. Un caso de mi práctica (anonimizado) — qué aprendimos
3. Una reflexión profesional sobre un tema de actualidad

La primera edición sale este mes. Si le interesa recibirla, le agrego a la lista. Son 4-5 minutos de lectura. Sin spam, sin venta directa.

Saludos,
Dr. Juan María Pérez
Rubicón EAS · {SITE['whatsapp']}

PD: Si prefiere no recibirla, ignore este correo. Su dirección queda eliminada automáticamente."""

# === CLI ===
def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 outreach-templates.py colega <nombre> <estudio> [area]")
        print("  python3 outreach-templates.py review <nombre> [area]")
        print("  python3 outreach-templates.py reactivate <nombre> [dias] [area]")
        print("  python3 outreach-templates.py empresa <contacto> <empresa> [sector]")
        print("  python3 outreach-templates.py refer <nombre> <colega> [area]")
        print("  python3 outreach-templates.py newsletter <nombre> [fuente]")
        return

    cmd = sys.argv[1]
    if cmd == "colega":
        msg = whatsapp_colega(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "civil")
    elif cmd == "review":
        msg = whatsapp_cliente_post_caso(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "civil")
    elif cmd == "reactivate":
        dias = int(sys.argv[3]) if len(sys.argv) > 3 else 180
        area = sys.argv[4] if len(sys.argv) > 4 else "civil"
        msg = whatsapp_cliente_reactivar(sys.argv[2], dias, area)
    elif cmd == "empresa":
        sector = sys.argv[4] if len(sys.argv) > 4 else "PyME"
        msg = whatsapp_empresa_intro(sys.argv[2], sys.argv[3], sector)
    elif cmd == "refer":
        msg = whatsapp_referral_request(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "civil")
    elif cmd == "newsletter":
        msg = email_newsletter_invite(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "colega")
    else:
        print(f"Comando desconocido: {cmd}")
        return

    print(f"\n--- {cmd.upper()} ---\n")
    print(msg)

if __name__ == "__main__":
    main()
