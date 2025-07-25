import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from utils import invia_email  # Assicurati di avere questa funzione
import pywhatkit

load_dotenv()

def invia_notifiche(session, giorni_avviso=7):
    oggi = datetime.today().date()
    limite = oggi + timedelta(days=giorni_avviso)

    from models import Scadenza
    scadenze = session.query(Scadenza).filter(Scadenza.data_scadenza <= limite).all()

    email_fisse = [e.strip() for e in os.getenv("EMAIL_CC", "").split(",") if e.strip()]
    numeri_fissi = [n.strip() for n in os.getenv("WHATSAPP_CC", "").split(",") if n.strip()]

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
        destinatari = [cliente.email] + email_fisse
        invia_email(destinatari, "🔔 Promemoria Scadenza", corpo)

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