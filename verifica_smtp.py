import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

# 1. Carica variabili dal file .env
load_dotenv()

mittente = os.getenv("EMAIL_SENDER")
password = os.getenv("EMAIL_PASSWORD")

# 2. Determina il server SMTP in base al dominio
if mittente and "@gmail.com" in mittente:
    smtp_server = "smtp.gmail.com"
elif mittente and "@outlook.com" in mittente:
    smtp_server = "smtp.office365.com"
else:
    smtp_server = "smtp.gmail.com"  # Default

print("📦 Variabili caricate:")
print("EMAIL_SENDER:", mittente if mittente else "❌ MANCANTE")
print("EMAIL_PASSWORD:", "✔️" if password else "❌ MANCANTE")
print("SMTP Server selezionato:", smtp_server)

# 3. Prepara il messaggio
destinatario = mittente or "test@example.com"
msg = MIMEText("Ciao Massimo,\n\nQuesta è una email di test per verificare la connessione SMTP.")
msg['Subject'] = "🔧 Test SMTP"
msg['From'] = mittente
msg['To'] = destinatario

# 4. Connessione al server SMTP
try:
    print(f"\n🔌 Connessione a {smtp_server}...")
    with smtplib.SMTP(smtp_server, 587) as server:
        server.set_debuglevel(1)  # Mostra dettagli della connessione
        server.starttls()
        server.login(mittente, password)
        server.send_message(msg)
    print("\n✅ Email inviata con successo.")
except smtplib.SMTPAuthenticationError as auth_err:
    print("\n❌ Errore di autenticazione SMTP:")
    print("➡️ Verifica che la password sia corretta.")
    print("➡️ Se hai 2FA, usa una password per app.")
    print("Dettagli:", auth_err)
except Exception as e:
    print("\n❌ Errore generico durante l'invio:")
    print("Dettagli:", e)