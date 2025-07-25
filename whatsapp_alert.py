import pywhatkit
from app import db, Scadenza, Cliente
from datetime import datetime, timedelta

# Imposta quanti giorni prima inviare l'avviso
giorni_avviso = 7
oggi = datetime.today().date()
limite = oggi + timedelta(days=giorni_avviso)

# Trova scadenze entro 7 giorni
scadenze = Scadenza.query.filter(Scadenza.data_scadenza <= limite).all()

for scadenza in scadenze:
    cliente = Cliente.query.get(scadenza.cliente_id)
    numero = cliente.telefono.strip() if cliente.telefono else ""

    # Verifica che il numero sia valido