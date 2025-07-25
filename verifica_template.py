import os

# Percorso base del progetto
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, 'templates')

# File richiesti
required_files = [
    'index.html',
    'nuovo_cliente.html',
    'nuova_scadenza.html',
    'modifica_scadenza.html',
    'calendario.html',
    'log_email.html'
]

print(f"📁 Cartella progetto: {base_dir}")
print(f"🔍 Verifica cartella 'templates'...")

if not os.path.isdir(templates_dir):
    print("❌ Cartella 'templates' NON trovata.")
else:
    print("✅ Cartella 'templates' trovata.")
    print("🔍 Verifica file HTML...")

    missing = []
    for filename in required_files:
        path = os.path.join(templates_dir, filename)
        if not os.path.isfile(path):
            missing.append(filename)

    if missing:
        print("❌ Mancano i seguenti file HTML:")
        for f in missing:
            print(f"   - {f}")
    else:
        print("✅ Tutti i file HTML sono presenti!")

print("\n📌 Se qualcosa manca, copia i file HTML che ti ho inviato nella cartella 'templates'.")