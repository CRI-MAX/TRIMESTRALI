from twilio.rest import Client

def invia_whatsapp(numero, descrizione, data):
    account_sid = "TUO_ACCOUNT_SID"
    auth_token = "TUO_AUTH_TOKEN"
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=f"🔔 Hai una scadenza: {descrizione} il {data}",
            from_="whatsapp:+14155238886",  # numero Twilio
            to=f"whatsapp:{numero}"
        )
    except Exception as e:
        print("Errore invio WhatsApp:", e)