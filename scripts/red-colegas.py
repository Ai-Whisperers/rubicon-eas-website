#!/usr/bin/env python3
"""
Rubicón EAS — Red de Colegas
Herramientas para la red de derivaciones.

Funcionalidades:
1. Importar lista de colegas desde CSV/JSON
2. Tracking del estado de cada colega (no contactado, contactado, acuerdo, etc.)
3. Generar scripts de WhatsApp de primer contacto
4. Reporte de la red
"""
import csv
import json
import os
from pathlib import Path
from datetime import datetime

DATA_DIR = Path('marketing/red-colegas')
DATA_DIR.mkdir(parents=True, exist_ok=True)

CSV_COLS = [
    "nombre",
    "estudio",
    "area_principal",
    "direccion",
    "telefono",
    "email",
    "estado",  # no-contactado, contactado, reunion, acuerdo, inactivo
    "fecha_ultimo_contacto",
    "notas",
    "fuente",  # google-maps, colegio, referido-por, linkedin
    "calificacion",  # 1-5
]

SAMPLE_DATA = [
    {
        "nombre": "Dr. [Nombre]",
        "estudio": "[Estudio Jurídico X]",
        "area_principal": "civil",
        "direccion": "[Dirección]",
        "telefono": "+595 9XX XXX XXX",
        "email": "contacto@estudio.com.py",
        "estado": "no-contactado",
        "fecha_ultimo_contacto": "",
        "notas": "",
        "fuente": "google-maps",
        "calificacion": "3"
    }
]

def ensure_csv():
    csv_path = DATA_DIR / 'colegas.csv'
    if not csv_path.exists():
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLS)
            writer.writeheader()
            for row in SAMPLE_DATA:
                writer.writerow(row)
    return csv_path

def read_colegas():
    csv_path = ensure_csv()
    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def update_estado(nombre, nuevo_estado, notas=""):
    """Update the state of a colleague in the network."""
    csv_path = ensure_csv()
    rows = read_colegas()
    found = False
    for row in rows:
        if row['nombre'] == nombre:
            row['estado'] = nuevo_estado
            row['fecha_ultimo_contacto'] = datetime.now().strftime('%Y-%m-%d')
            if notas:
                existing = row.get('notas', '')
                row['notas'] = f"{existing}\n[{datetime.now().strftime('%Y-%m-%d')}] {notas}".strip()
            found = True
            break
    if not found:
        print(f"  ! {nombre} no encontrado")
        return
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"  ✓ {nombre} → {nuevo_estado}")

def add_colega(nombre, estudio, area_principal, contacto="", fuente="manual"):
    """Add a new colleague to the network."""
    csv_path = ensure_csv()
    rows = read_colegas()
    if any(r['nombre'] == nombre for r in rows):
        print(f"  ! {nombre} ya existe")
        return
    rows.append({
        "nombre": nombre,
        "estudio": estudio,
        "area_principal": area_principal,
        "direccion": "",
        "telefono": contacto,
        "email": "",
        "estado": "no-contactado",
        "fecha_ultimo_contacto": "",
        "notas": "",
        "fuente": fuente,
        "calificacion": "3"
    })
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"  ✓ {nombre} agregado")

def reporte():
    """Generate a status report of the network."""
    rows = read_colegas()
    states = {}
    for row in rows:
        s = row.get('estado', 'no-contactado')
        states[s] = states.get(s, 0) + 1
    print(f"\n📊 Red de colegas")
    print(f"  Total: {len(rows)}")
    for state, count in sorted(states.items()):
        print(f"  {state}: {count}")
    # Por calificación
    by_calif = {}
    for row in rows:
        c = row.get('calificacion', '0')
        by_calif[c] = by_calif.get(c, 0) + 1
    if by_calif:
        print(f"\n  Por calificación:")
        for c, n in sorted(by_calif.items(), key=lambda x: -int(x[0])):
            print(f"    {c}★: {n}")

def whatsapp_first_contact(nombre, estudio, area="civil"):
    """Generate a first-contact WhatsApp message for a colleague."""
    a = {
        "civil": "Derecho Civil",
        "penal": "Derecho Penal",
        "ambiental": "Derecho Ambiental"
    }.get(area, "Derecho")
    msg = f"""Estimado/a {nombre}:

Mi nombre es Juan María Pérez, soy abogado y recientemente fundé Rubicón EAS en Asunción.

Trabajo principalmente en {a}, y estoy armando una red de colegas para derivaciones recíprocas. La idea es simple: si me llega un caso que no es mi especialidad, le paso al colega más indicado, y viceversa.

¿Le parece si coordinamos un café la próxima semana para conocernos? Puedo llevar el mate.

Saludos,
Dr. Juan María Pérez
Rubicón EAS · {a}
{SITE_INFO}"""
    return msg

SITE_INFO = "Av. Mariscal López 1234, Piso 8 Of. 803, Asunción · +595 981 234 567"

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 red-colegas.py init")
        print("  python3 red-colegas.py add '<nombre>' '<estudio>' <area> <contacto>")
        print("  python3 red-colegas.py update <nombre> <estado> [notas]")
        print("  python3 red-colegas.py report")
        print("  python3 red-colegas.py message <nombre> [area]")
        return

    cmd = sys.argv[1]

    if cmd == "init":
        ensure_csv()
        print("✓ CSV inicializado")
    elif cmd == "add":
        if len(sys.argv) < 5:
            print("Faltan args: <nombre> <estudio> <area> [contacto]")
            return
        nombre = sys.argv[2]
        estudio = sys.argv[3]
        area = sys.argv[4]
        contacto = sys.argv[5] if len(sys.argv) > 5 else ""
        add_colega(nombre, estudio, area, contacto)
    elif cmd == "update":
        if len(sys.argv) < 4:
            print("Faltan args: <nombre> <estado> [notas]")
            return
        nombre = sys.argv[2]
        estado = sys.argv[3]
        notas = sys.argv[4] if len(sys.argv) > 4 else ""
        update_estado(nombre, estado, notas)
    elif cmd == "report":
        reporte()
    elif cmd == "message":
        if len(sys.argv) < 3:
            print("Falta: <nombre> [area]")
            return
        nombre = sys.argv[2]
        area = sys.argv[3] if len(sys.argv) > 3 else "civil"
        rows = read_colegas()
        match = next((r for r in rows if r['nombre'] == nombre), None)
        if not match:
            print(f"  ! {nombre} no encontrado")
            return
        msg = whatsapp_first_contact(nombre, match['estudio'], area)
        print(f"\n--- Mensaje de primer contacto para {nombre} ({match['estudio']}) ---\n")
        print(msg)
    else:
        print(f"Comando desconocido: {cmd}")

if __name__ == "__main__":
    main()
