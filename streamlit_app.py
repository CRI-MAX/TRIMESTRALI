import streamlit as st
from supabase_utils import get_scadenze_prossime, segna_notificato
from whatsapp_utils import invia_whatsapp
from email_utils import invia_email

st.title("Gestione Scadenze Clienti")

scadenze = get_scadenze_prossime()

for s in scadenze:
    st.write(f"📌 {s['nome_cliente']} - {s['tipo_scadenza']} - {s['data_scadenza']}")
    messaggio = f"Ciao {s['nome_cliente']}, la tua scadenza '{s['tipo_scadenza']}' è prevista per il {s['data_scadenza']}."
    
    if st.button(f"Invia alert a {s['nome_cliente']}", key=s['id']):
        invia_whatsapp(s['telefono'], messaggio)
        invia_email(s['email'], "Promemoria Scadenza", messaggio)
        segna_notificato(s['id'])
        st.success("Notifica inviata!")