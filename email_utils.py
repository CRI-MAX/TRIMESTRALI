import smtplib
from email.mime.text import MIMEText

def invia_email(destinatario, descrizione, data):
    msg = MIMEText(f"Attenzione! Hai una scadenza: {descrizione} il {data}")
    msg["Subject"] = "🔔 Promemoria Scadenza"
    msg["From"] = "tuo@email.it"
    msg["To"] = destinatario

    try:
        with smtplib.SMTP("smtp.tuodominio.it", 587) as server:
            server.starttls()
            server.login("tuo@email.it", "password")
            server.send_message(msg)
    except Exception as e:
        print("Errore invio email:", e)