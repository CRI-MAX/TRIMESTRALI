from app import app, db, Cliente

def verifica_clienti_senza_scadenze():
    with app.app_context():
        clienti = Cliente.query.all()
        senza_scadenze = [c for c in clienti if not c.scadenze]

        if not senza_scadenze:
            print("✅ Tutti i clienti hanno almeno una scadenza.")
            return

        print(f"⚠️ Trovati {len(senza_scadenze)} clienti senza scadenze:")
        for c in senza_scadenze:
            print(f"👤 {c.nome} - Email: {c.email} - Telefono: {c.telefono}")

if __name__ == "__main__":
    verifica_clienti_senza_scadenze()