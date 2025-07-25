import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from models import Scadenza
from utils import invia_email  # Assicurati che esista questa funzione

load_dotenv()

def invia_notifiche(session, giorni_avviso=7):
    oggi = datetime.today().date()
    limite = oggi + timedelta(days=giorni_avviso)

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

        # 📱 WhatsApp (solo link generato)
        messaggio = f"""🔔 Ciao {cliente.nome}!
Ti ricordiamo la scadenza:
📌 {scadenza.titolo}
📅 {scadenza.data_scadenza.strftime('%d/%m/%Y')}"""

        numeri = [cliente.telefono] + numeri_fissi
        for numero in numeri:
            numero_clean = numero.replace("+", "")
            link = f"https://wa.me/{numero_clean}?text={messaggio.replace(' ', '%20')}"
            print(f"📱 WhatsApp link per {numero}: {link}")