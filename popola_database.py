from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Cliente, Scadenza, TipoScadenza

# Connessione al database
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

# Inizializza il database (se non già fatto)
Base.metadata.create_all(engine)

# ✅ Inserisci tipi di scadenza
tipo1 = TipoScadenza(nome="Fattura")
tipo2 = TipoScadenza(nome="Certificato")
session.add_all([tipo1, tipo2])
session.commit()

# ✅ Inserisci clienti
cliente1 = Cliente(nome="Mario Rossi", email="mario@example.com", telefono="+393491234567")
cliente2 = Cliente(nome="Anna Bianchi", email="anna@example.com", telefono="+393477778888")
session.add_all([cliente1, cliente2])
session.commit()

# ✅ Inserisci scadenze
scadenza1 = Scadenza(
    cliente_id=cliente1.id,
    tipo_id=tipo1.id,
    titolo="Fattura Luglio",
    data_scadenza=datetime.today().date() + timedelta(days=3),
    ricorrenza_giorni=30,
    documento="https://example.com/fattura-luglio.pdf",
    email_alert="contabile@example.com"
)

scadenza2 = Scadenza(
    cliente_id=cliente2.id,
    tipo_id=tipo2.id,
    titolo="Certificato SSL",
    data_scadenza=datetime.today().date() + timedelta(days=5),
    ricorrenza_giorni=365,
    documento="https://example.com/certificato-ssl.pdf",
    email_alert="tecnico@example.com"
)

session.add_all([scadenza1, scadenza2])
session.commit()

print("✅ Dati di esempio inseriti con successo.")