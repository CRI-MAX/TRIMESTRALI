from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from utils import invia_email
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# MODELLI
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    scadenze = db.relationship('Scadenza', backref='cliente', lazy=True)

class Scadenza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    titolo = db.Column(db.String(200))
    data_scadenza = db.Column(db.Date)
    ricorrenza_giorni = db.Column(db.Integer)
    documento = db.Column(db.String(300))
    email_alert = db.Column(db.String(300))

class LogEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scadenza_id = db.Column(db.Integer, db.ForeignKey('scadenza.id'), nullable=False)
    data_invio = db.Column(db.DateTime, default=datetime.utcnow)

def registra_log_email(scadenza_id):
    log = LogEmail(scadenza_id=scadenza_id)
    db.session.add(log)
    db.session.commit()

@app.route('/')
def index():
    scadenze = Scadenza.query.order_by(Scadenza.data_scadenza).all()
    return render_template('index.html', scadenze=scadenze)

@app.route('/nuovo_cliente', methods=['GET', 'POST'])
def nuovo_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefono = request.form['telefono'].strip()

        # Validazione telefono
        if not telefono.startswith("+") or not telefono[1:].isdigit() or len(telefono) < 10:
            errore = "❌ Numero WhatsApp non valido. Usa il formato internazionale, es. +393471234567"
            return render_template('nuovo_cliente.html', errore=errore, nome=nome, email=email, telefono=telefono)

        cliente = Cliente(nome=nome, email=email, telefono=telefono)
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('nuovo_cliente.html')

@app.route('/nuova_scadenza', methods=['GET', 'POST'])
def nuova_scadenza():
    clienti = Cliente.query.all()
    if request.method == 'POST':
        file = request.files['documento']
        path = ''
        if file and file.filename:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)

        scadenza = Scadenza(
            cliente_id=request.form['cliente_id'],
            titolo=request.form['titolo'],
            data_scadenza=datetime.strptime(request.form['data_scadenza'], '%Y-%m-%d'),
            ricorrenza_giorni=int(request.form.get('ricorrenza_giorni', 0)),
            documento=path,
            email_alert=request.form.get('email_alert', '')
        )
        db.session.add(scadenza)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('nuova_scadenza.html', clienti=clienti)

@app.route('/notifica/<int:id>')
def notifica(id):
    scadenza = Scadenza.query.get(id)
    cliente = Cliente.query.get(scadenza.cliente_id)

    corpo = f"""Ciao {cliente.nome},

Ti ricordiamo la scadenza:
📌 {scadenza.titolo}
📅 Data: {scadenza.data_scadenza.strftime('%d/%m/%Y')}

Cordiali saluti,
Scadenze App
"""

    cc = [email.strip() for email in scadenza.email_alert.split(",") if email.strip()]
    invia_email(destinatario=cliente.email, oggetto="🔔 Promemoria Scadenza", corpo=corpo, cc=cc)
    registra_log_email(scadenza.id)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)