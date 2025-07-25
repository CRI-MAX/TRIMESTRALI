import requests

BASE_URL = "http://localhost:5000"

routes = {
    "/": "Home",
    "/nuovo_cliente": "Nuovo Cliente",
    "/nuova_scadenza": "Nuova Scadenza",
    "/calendario": "Calendario",
    "/log_email": "Storico Email",
    "/esporta_excel": "Esporta Excel",
    "/test_email": "Test Email"
}

print("🔍 Test delle rotte Flask...\n")

for route, name in routes.items():
    try:
        response = requests.get(BASE_URL + route)
        if response.status_code == 200:
            print(f"✅ {name} ({route}) → OK")
        else:
            print(f"⚠️ {name} ({route}) → Status {response.status_code}")
    except Exception as e:
        print(f"❌ {name} ({route}) → Errore: {e}")

print("\n📌 Assicurati che l'app Flask sia in esecuzione prima di lanciare questo test.")