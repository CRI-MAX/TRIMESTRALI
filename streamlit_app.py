import streamlit as st
from datetime import date, timedelta
from db_utils import session, Cliente, TipoScadenza, Scadenza

st.set_page_config(page_title="Gestione Scadenze", layout="centered")
st.title("📅 Gestione Scadenze")

# -------------------------------
# 🔔 Notifiche scadenze imminenti
# -------------------------------
oggi = date.today()
limite = oggi + timedelta(days=7)

scadenze_imminenti = (
    session.query(Scadenza)
    .filter(Scadenza.data_scadenza >= oggi, Scadenza.data_scadenza <= limite)
    .order_by(Scadenza.data_scadenza)
    .all()
)

if scadenze_imminenti:
    st.warning("⚠️ Hai scadenze imminenti nei prossimi 7 giorni!")
    for s in scadenze_imminenti:
        cliente = session.query(Cliente).get(s.cliente_id)
        tipo = session.query(TipoScadenza).get(s.tipo_id)
        st.markdown(f"""
        - **{s.titolo}**  
          📅 {s.data_scadenza.strftime('%d/%m/%Y')}  
          👤 {cliente.nome}  
          🗂️ {tipo.nome}
        """)
else:
    st.success("✅ Nessuna scadenza imminente.")

# -------------------------------
# 👤 Aggiungi nuovo cliente
# -------------------------------
st.subheader("➕ Aggiungi nuovo cliente")

nome_cliente = st.text_input("Nome cliente")
email_cliente = st.text_input("Email cliente")

if st.button("Salva cliente"):
    if nome_cliente and email_cliente:
        nuovo_cliente = Cliente(nome=nome_cliente, email=email_cliente)
        session.add(nuovo_cliente)
        session.commit()
        st.success("✅ Cliente aggiunto con successo!")
    else:
        st.warning("⚠️ Inserisci sia il nome che l'email.")

# -------------------------------
# 🗂️ Aggiungi nuovo tipo di scadenza
# -------------------------------
st.subheader("➕ Aggiungi nuovo tipo di scadenza")

nome_tipo = st.text_input("Nome tipo di scadenza")

if st.button("Salva tipo di scadenza"):
    if nome_tipo:
        nuovo_tipo = TipoScadenza(nome=nome_tipo)
        session.add(nuovo_tipo)
        session.commit()
        st.success("✅ Tipo di scadenza aggiunto con successo!")
    else:
        st.warning("⚠️ Inserisci il nome del tipo di scadenza.")

# -------------------------------
# 📝 Aggiungi nuova scadenza
# -------------------------------
st.subheader("➕ Aggiungi nuova scadenza")

clienti = session.query(Cliente).order_by(Cliente.nome).all()
tipi = session.query(TipoScadenza).order_by(TipoScadenza.nome).all()

cliente_opzioni = {f"{c.nome} ({c.email})": c.id for c in clienti}
tipo_opzioni = {t.nome: t.id for t in tipi}

cliente_nome = st.selectbox("Cliente", list(cliente_opzioni.keys()))
cliente_id = cliente_opzioni[cliente_nome]

tipo_nome = st.selectbox("Tipo di scadenza", list(tipo_opzioni.keys()))
tipo_id = tipo_opzioni[tipo_nome]

titolo = st.text_input("Titolo scadenza")
descrizione = st.text_area("Descrizione")
data_scadenza = st.date_input("Data di scadenza", min_value=date.today())

if st.button("Salva scadenza"):
    nuova = Scadenza(
        titolo=titolo,
        descrizione=descrizione,
        data_scadenza=data_scadenza,
        cliente_id=cliente_id,
        tipo_id=tipo_id
    )
    session.add(nuova)
    session.commit()
    st.success("✅ Scadenza salvata con successo!")

# -------------------------------
# 📋 Tabella riepilogativa
# -------------------------------
st.subheader("📋 Scadenze registrate")

filtro_cliente = st.selectbox("Filtra per cliente", ["Tutti"] + list(cliente_opzioni.keys()))
filtro_tipo = st.selectbox("Filtra per tipo", ["Tutti"] + list(tipo_opzioni.keys()))

query = session.query(Scadenza)

if filtro_cliente != "Tutti":
    query = query.filter(Scadenza.cliente_id == cliente_opzioni[filtro_cliente])
if filtro_tipo != "Tutti":
    query = query.filter(Scadenza.tipo_id == tipo_opzioni[filtro_tipo])

scadenze = query.order_by(Scadenza.data_scadenza).all()

if scadenze:
    dati = []
    for s in scadenze:
        cliente = session.query(Cliente).get(s.cliente_id)
        tipo = session.query(TipoScadenza).get(s.tipo_id)
        dati.append({
            "Titolo": s.titolo,
            "Descrizione": s.descrizione,
            "Data": s.data_scadenza.strftime("%d/%m/%Y"),
            "Cliente": cliente.nome,
            "Tipo": tipo.nome
        })
    st.dataframe(dati, use_container_width=True)
else:
    st.info("ℹ️ Nessuna scadenza trovata con i filtri selezionati.")

# -------------------------------
# ✏️ Modifica o elimina scadenza
# -------------------------------
st.subheader("✏️ Modifica o elimina scadenza")

scadenze_tutte = session.query(Scadenza).order_by(Scadenza.data_scadenza).all()

if scadenze_tutte:
    scadenza_opzioni = {
        f"{s.titolo} - {s.data_scadenza.strftime('%d/%m/%Y')}": s.id for s in scadenze_tutte
    }
    scelta = st.selectbox("Seleziona una scadenza", list(scadenza_opzioni.keys()))
    scadenza_id = scadenza_opzioni[scelta]
    scadenza = session.query(Scadenza).get(scadenza_id)

    nuovo_titolo = st.text_input("Titolo", value=scadenza.titolo)
    nuova_descrizione = st.text_area("Descrizione", value=scadenza.descrizione)
    nuova_data = st.date_input("Data di scadenza", value=scadenza.data_scadenza)

    nuovo_cliente = st.selectbox("Cliente", list(cliente_opzioni.keys()), index=list(cliente_opzioni.values()).index(scadenza.cliente_id))
    nuovo_tipo = st.selectbox("Tipo di scadenza", list(tipo_opzioni.keys()), index=list(tipo_opzioni.values()).index(scadenza.tipo_id))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Salva modifiche"):
            scadenza.titolo = nuovo_titolo
            scadenza.descrizione = nuova_descrizione
            scadenza.data_scadenza = nuova_data
            scadenza.cliente_id = cliente_opzioni[nuovo_cliente]
            scadenza.tipo_id = tipo_opzioni[nuovo_tipo]
            session.commit()
            st.success("✅ Scadenza modificata con successo!")

    with col2:
        if st.button("🗑️ Elimina scadenza"):
            session.delete(scadenza)
            session.commit()
            st.warning("⚠️ Scadenza eliminata.")
else:
    st.info("ℹ️ Nessuna scadenza disponibile per modifica o eliminazione.")