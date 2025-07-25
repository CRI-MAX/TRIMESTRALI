from models import db, Cliente, Scadenza
from utils import invia_email
from flask import Flask
from datetime import datetime, timedelta
import os

# Setup Flask app per accedere al database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 🔍 Giorni di anticipo per il promemoria
ANTICIPO_GIORNI = 3

with app.app_context():
    oggi = datetime.now()
    limite = oggi + timedelta(days=ANTICIPO_GIORNI)

    scadenze = Scadenza.query.filter(
        Scadenza.data_scadenza >= oggi,
        Scadenza.data_scadenza <= limite
    ).all()

    for scadenza in scadenze:
        cliente = Cliente.query.get(scadenza.cliente_id)
        invia_email(
            cliente.email,
            f"Promemoria: {scadenza.titolo}",
            f"Ciao {cliente.nome},\n\nTi ricordiamo che la scadenza \"{scadenza.titolo}\" è prevista per il {scadenza.data_scadenza.strftime('%d/%m/%Y')}."
        )
        print(f"✅ Email inviata a {cliente.email} per scadenza: {scadenza.titolo}")