import os

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, 'templates')
os.makedirs(templates_dir, exist_ok=True)

files_content = {
    "index.html": """<!DOCTYPE html>
<html><head><title>Scadenze</title></head>
<body><h1>📋 Elenco Scadenze</h1></body></html>""",

    "nuovo_cliente.html": """<!DOCTYPE html>
<html><head><title>Nuovo Cliente</title></head>
<body><h1>➕ Nuovo Cliente</h1></body></html>""",

    "nuova_scadenza.html": """<!DOCTYPE html>
<html><head><title>Nuova Scadenza</title></head>
<body><h1>➕ Nuova Scadenza</h1></body></html>""",

    "modifica_scadenza.html": """<!DOCTYPE html>
<html><head><title>Modifica Scadenza</title></head>
<body><h1>✏️ Modifica Scadenza</h1></body></html>""",

    "calendario.html": """<!DOCTYPE html>
<html><head><title>Calendario</title></head>
<body><h1>📆 Calendario Scadenze</h1></body></html>""",

    "log_email.html": """<!DOCTYPE html>
<html><head><title>Storico Email</title></head>
<body><h1>📬 Storico Email Inviate</h1></body></html>"""
}

print(f"📁 Cartella progetto: {base_dir}")
print(f"🔧 Ripristino file HTML nella cartella 'templates'...")

for filename, content in files_content.items():
    path = os.path.join(templates_dir, filename)
    if not os.path.isfile(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Creato: {filename}")
    else:
        print(f"✔️ Già presente: {filename}")

print("\n📌 Tutti i file HTML sono ora disponibili nella cartella 'templates'.")