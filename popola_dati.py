from app import db, Cliente, Scadenza, app
from datetime import datetime, timedelta

with app.app_context():
    # Cancella tutto (opzionale, solo per test)
    db.drop_all()
    db.create_all()

    # Clienti di esempio
    clienti = [
        Cliente(nome="Mario Rossi", email="mario.rossi@example.com"),
        Cliente(nome="Luca Bianchi", email="luca.bianchi@example.com"),
        Cliente(nome="Anna Verdi", email="anna.verdi@example.com")
    ]

    db.session.add_all(clienti)
    db.session.commit()

    # Scadenze di esempio
    oggi = datetime.today()
    scadenze = [
        Scadenza(cliente_id=clienti[0].id, titolo="Fattura Aprile", data_scadenza=oggi + timedelta(days=5), ricorrenza_giorni=0),
        Scadenza(cliente_id=clienti[1].id, titolo="Contratto da rinnovare", data_scadenza=oggi + timedelta(days=10), ricorrenza_giorni=30),
        Scadenza(cliente_id=clienti[2].id, titolo="Pagamento trimestrale", data_scadenza=oggi + timedelta(days=15), ricorrenza_giorni=90)
    ]

    db.session.add_all(scadenze)
    db.session.commit()

    print("✅ Dati di esempio inseriti con successo.")