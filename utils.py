import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def invia_email(destinatari, oggetto, corpo):
    mittente = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = mittente
    msg['To'] = ", ".join(destinatari)
    msg['Subject'] = oggetto
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(mittente, password)
        server.sendmail(mittente, destinatari, msg.as_string())
        server.quit()
    except Exception as e:
        print("❌ Errore invio email:", e)