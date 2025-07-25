import streamlit as st
from datetime import date, timedelta
from supabase import create_client, Client

# 🔐 Configura Supabase
SUPABASE_URL = "https://xgoblqkmusvzghhjqomt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhnb2JscWttdXN2emdoaGpxb210Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM0MzA0MjAsImV4cCI6MjA2OTAwNjQyMH0.1NohMQFSb2l1qPdEpcnztxS3HCkO0e4JwxgFnjEIp0M"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 📦 Funzioni Supabase
def get_scadenze_prossime(giorni=30):
    try:
        limite = date.today() + timedelta(days=giorni)
        response = supabase.table("scadenze_clienti") \
            .select("*") \
            .lte("data_scadenza", limite.isoformat()) \
            .eq("notificato", False) \
            .execute()
        return response.data
    except Exception as e:
        st.error(f"Errore Supabase: {e}")
        return []

def inserisci_scadenza(cliente, descrizione, data_scadenza):
    try:
        nuovo_record = {
            "cliente": cliente,
            "descrizione": descrizione,
            "data_scadenza": data_scadenza.isoformat(),
            "notificato": False
        }
        response = supabase.table("scadenze_clienti").insert(nuovo_record).execute()
        st.success("Scadenza inserita correttamente!")
    except Exception as e:
        st.error(f"Errore inserimento: {e}")

def marca_notificato(id):
    try:
        response = supabase.table("scadenze_clienti") \
            .update({"notificato": True}) \
            .eq("id", id) \
            .execute()
        st.success("Scadenza marcata come notificata!")
    except Exception as e:
        st.error(f"Errore aggiornamento: {e}")

# 🎯 Interfaccia Streamlit
st.title("Gestione Scadenze Clienti")

# ➕ Form per inserimento
with st.form("inserisci_scadenza"):
    st.subheader("Aggiungi nuova scadenza")
    cliente = st.text_input("Cliente")
    descrizione = st.text_input("Descrizione")
    data_scadenza = st.date_input("Data di scadenza", min_value=date.today())
    submitted = st.form_submit_button("Inserisci")
    if submitted:
        inserisci_scadenza(cliente, descrizione, data_scadenza)

# 📋 Lista scadenze
st.subheader("Scadenze prossime (entro 30 giorni)")
scadenze = get_scadenze_prossime()

if scadenze:
    for scadenza in scadenze:
        with st.expander(f"{scadenza['cliente']} - {scadenza['data_scadenza']}"):
            st.write(f"**Descrizione:** {scadenza['descrizione']}")
            st.write(f"**Notificato:** {scadenza['notificato']}")
            if st.button("Marca come notificata", key=scadenza['id']):
                marca_notificato(scadenza['id'])
else:
    st.info("Nessuna scadenza prossima trovata.")