from utils import invia_email

# Dati di test
destinatario = "tuo_account@outlook.com"  # Puoi usare anche un altro indirizzo
oggetto = "🔔 Test Email da script"
corpo = """Ciao Massimo,

Questa è una email di test inviata direttamente da test_email.py.
Se la ricevi, significa che la configurazione SMTP funziona correttamente!

Cordiali saluti,
Scadenze App
"""

# Invio
invia_email(destinatario, oggetto, corpo)