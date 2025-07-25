import pywhatkit
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Messaggio da inviare
messaggio = "🔔 Messaggio di test da Scadenze App. Tutto funziona correttamente!"

# ✅ Numeri fissi da .env
numeri_raw = os.getenv("WHATSAPP_CC", "")
numeri = [n.strip() for n in numeri_raw.split(",") if n.strip()]

if not numeri:
    print("⚠️ Nessun numero WhatsApp trovato in WHATSAPP_CC.")
else:
    for numero in numeri:
        try:
            print(f"📤 Invio a {numero}...")
            pywhatkit.sendwhatmsg_instantly(numero, messaggio)
            print(f"✅ Messaggio inviato a {numero}")
        except Exception as e:
            print(f"❌ Errore con {numero}: {e}")