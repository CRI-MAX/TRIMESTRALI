import streamlit as st
import sqlite3
from datetime import date, timedelta
from email_utils import invia_email
from whatsapp_utils import invia_whatsapp

# Connessione al database
conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

# Creazione tabelle
c.execute("""CREATE TABLE IF NOT EXISTS clienti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT,
    telefono TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS scadenze (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    descrizione TEXT,
    data DATE,
    FOREIGN KEY(cliente_id) REFERENCES clienti(id)
)""")

conn.commit()

# Funzioni di utilità
def get_clienti():
    return c.execute("SELECT * FROM clienti").fetchall()

def get_scadenze(cliente_id):
    return c.execute("SELECT * FROM scadenze WHERE cliente_id = ?", (cliente_id,)).fetchall()

# UI Streamlit
st.set_page_config(page_title="Gestione Scadenze", layout="centered")
st.title("📬 Gestione Scadenze Clienti")

# Sezione: Aggiungi cliente
st.sidebar.subheader("➕ Nuovo Cliente")
nome = st.sidebar.text_input("Nome")
email = st.sidebar.text_input("Email")
telefono = st.sidebar.text_input("Telefono")

if st.sidebar.button("Aggiungi Cliente"):
    c.execute("INSERT INTO clienti (nome, email, telefono) VALUES (?, ?, ?)", (nome, email, telefono))
    conn.commit()
    st.sidebar.success("Cliente aggiunto!")

# Selezione cliente
st.subheader("👤 Seleziona Cliente")
clienti = get_clienti()
cliente_opzioni = {f"{c[1]} ({c[0]})": c for c in clienti}
cliente_scelto = st.selectbox("Cliente", list(cliente_opzioni.keys())) if cliente_opzioni else None

if cliente_scelto:
    cliente = cliente_opzioni[cliente_scelto]

    # Sezione: Aggiungi scadenza
    st.subheader("📅 Nuova Scadenza")
    descrizione = st.text_input("Descrizione scadenza")
    data_scadenza = st.date_input("Data", min_value=date.today())

    if st.button("Aggiungi Scadenza"):
        c.execute("INSERT INTO scadenze (cliente_id, descrizione, data) VALUES (?, ?, ?)",
                  (cliente[0], descrizione, data_scadenza))
        conn.commit()
        st.success("Scadenza aggiunta!")

    # Elenco scadenze
    st.subheader("📋 Scadenze per cliente")
    scadenze = get_scadenze(cliente[0])
    for s in scadenze:
        st.markdown(f"- **{s[2]}** – {s[3]}")

    # Notifiche automatiche
    oggi = date.today()
    entro_3_giorni = oggi + timedelta(days=3)
    scadenze_imminenti = c.execute("""
        SELECT clienti.nome, clienti.email, clienti.telefono, scadenze.descrizione, scadenze.data
        FROM scadenze
        JOIN clienti ON scadenze.cliente_id = clienti.id
        WHERE scadenze.data <= ?
    """, (entro_3_giorni,)).fetchall()

    if scadenze_imminenti:
        st.subheader("🔔 Notifiche imminenti")
        for nome, email, telefono, descrizione, data_s in scadenze_imminenti:
            st.warning(f"{nome} ha una scadenza: {descrizione} il {data_s}")
            invia_email(email, descrizione, data_s)
            invia_whatsapp(telefono, descrizione, data_s)
else:
    st.info("ℹ️ Aggiungi un cliente per iniziare.")