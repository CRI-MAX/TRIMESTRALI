import streamlit as st
from datetime import date

# Simulazione di una classe Scadenza
class Scadenza:
    def __init__(self, id, descrizione, data):
        self.id = id
        self.descrizione = descrizione
        self.data = data

# Simulazione di un database in memoria
scadenze = [
    Scadenza(1, "Pagamento IVA", date(2025, 7, 31)),
    Scadenza(2, "Versamento INPS", date(2025, 8, 15)),
]

st.set_page_config(page_title="Gestione Scadenze", layout="centered")
st.title("📅 Gestione Scadenze Trimestrali")

# Sezione: Inserimento nuova scadenza
st.subheader("➕ Aggiungi Nuova Scadenza")
descrizione_nuova = st.text_area("Descrizione", key="descrizione_nuova")
data_nuova = st.date_input("Data", key="data_nuova")

if st.button("Aggiungi", key="btn_aggiungi"):
    nuovo_id = max([s.id for s in scadenze]) + 1 if scadenze else 1
    scadenze.append(Scadenza(nuovo_id, descrizione_nuova, data_nuova))
    st.success(f"✅ Scadenza aggiunta: {descrizione_nuova} ({data_nuova})")

# Sezione: Modifica scadenza esistente
st.subheader("✏️ Modifica Scadenza Esistente")
scelte = {f"{s.id} - {s.descrizione}": s for s in scadenze}
scelta = st.selectbox("Seleziona una scadenza", list(scelte.keys()), key="select_modifica")

scadenza_selezionata = scelte[scelta]
nuova_descrizione = st.text_area("Descrizione", value=scadenza_selezionata.descrizione, key="descrizione_modifica")
nuova_data = st.date_input("Data", value=scadenza_selezionata.data, key="data_modifica")

if st.button("Aggiorna", key="btn_aggiorna"):
    scadenza_selezionata.descrizione = nuova_descrizione
    scadenza_selezionata.data = nuova_data
    st.success(f"✅ Scadenza aggiornata: {nuova_descrizione} ({nuova_data})")

# Sezione: Elenco scadenze
st.subheader("📋 Elenco Scadenze")
for s in scadenze:
    st.markdown(f"- **{s.descrizione}** – {s.data.strftime('%d/%m/%Y')}")