from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
FROM = os.getenv("TWILIO_WHATSAPP_FROM")

def invia_whatsapp(to, messaggio):
    client.messages.create(
        body=messaggio,
        from_=FROM,
        to=to
    )