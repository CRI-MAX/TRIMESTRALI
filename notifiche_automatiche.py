from app import app, db, Scadenza, Cliente
from utils import invia_email
import pywhatkit
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

def invia_notifiche():
    with app.app_context():
        giorni_avviso = 7
        oggi = datetime.today().date()
        limite = oggi + timedelta(days=giorni_avviso)

        scadenze = Scadenza.query.filter(Scadenza.data_scadenza <= limite).all()
        numeri_fissi = [n.strip() for n in os.getenv("WHATSAPP_CC", "").split(",") if n.strip()]
        email_fisse = [e.strip() for e in os.getenv("EMAIL_CC", "").split(",") if e.strip()]

        for scadenza in scadenze:
            cliente = scadenza.cliente
            if not cliente:
                continue

            # 📧 Email
            corpo = f"""Ciao {cliente.nome},

Ti ricordiamo la scadenza:
📌 {scadenza.titolo}
📅 Data: {scadenza.data_scadenza.strftime('%d/%m/%Y')}

Cordiali saluti,
Scadenze App
"""
            cc = email_fisse + [e.strip() for e in scadenza.email_alert.split(",") if e.strip()]
            invia_email(destinatario=cliente.email, oggetto="🔔 Promemoria Scadenza", corpo=corpo, cc=cc)

            # 📱 WhatsApp
            messaggio = f"""🔔 Ciao {cliente.nome}!
Ti ricordiamo la scadenza:
📌 {scadenza.titolo}
📅 {scadenza.data_scadenza.strftime('%d/%m/%Y')}"""

            numeri = [cliente.telefono] + numeri_fissi
            for numero in numeri:
                if numero and numero.startswith("+"):
                    try:
                        pywhatkit.sendwhatmsg_instantly(numero, messaggio)
                        print(f"✅ WhatsApp inviato a {numero}")
                    except Exception as e:
                        print(f"❌ Errore WhatsApp con {numero}: {e}")

if __name__ == "__main__":
    invia_notifiche()