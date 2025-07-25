from app import app, db, Scadenza

def verifica_e_pulisci_scadenze_orfane():
    with app.app_context():
        tutte = Scadenza.query.all()
        orfane = [s for s in tutte if not s.cliente]

        if not orfane:
            print("✅ Nessuna scadenza orfana trovata.")
            return

        print(f"⚠️ Trovate {len(orfane)} scadenze orfane. Procedo con l'eliminazione...")
        for s in orfane:
            print(f"🗑️ Eliminata scadenza ID {s.id} - Titolo: {s.titolo}")
            db.session.delete(s)

        db.session.commit()
        print("✅ Pulizia completata.")

if __name__ == "__main__":
    verifica_e_pulisci_scadenze_orfane()