import streamlit as st

# Simulazione di una classe Scadenza
class Scadenza:
    def __init__(self, descrizione):
        self.descrizione = descrizione

# Esempio di scadenza esistente
scadenza = Scadenza("Pagamento trimestrale IVA")

st.title("Gestione Scadenze")

# Sezione: Inserimento nuova scadenza
st.subheader("Nuova Scadenza")
descrizione_nuova = st.text_area("Descrizione", key="descrizione_nuova")
if st.button("Aggiungi Scadenza"):
    st.success(f"Scadenza aggiunta: {descrizione_nuova}")

# Sezione: Modifica scadenza esistente
st.subheader("Modifica Scadenza Esistente")
nuova_descrizione = st.text_area("Descrizione", value=scadenza.descrizione, key="descrizione_modifica")
if st.button("Aggiorna Scadenza"):
    scadenza.descrizione = nuova_descrizione
    st.success(f"Scadenza aggiornata: {scadenza.descrizione}")