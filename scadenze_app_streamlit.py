import streamlit as st
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Scadenza(Base):
    __tablename__ = 'scadenze'
    id = Column(Integer, primary_key=True)
    titolo = Column(String)
    data_scadenza = Column(Date)

engine = create_engine('sqlite:///scadenze.db')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

st.title("📋 Scadenze Minimali")

# Inserimento
with st.form("form_scadenza"):
    titolo = st.text_input("Titolo")
    data = st.date_input("Data Scadenza", value=date.today())
    invia = st.form_submit_button("Salva")
    if invia and titolo:
        nuova = Scadenza(titolo=titolo, data_scadenza=data)
        session.add(nuova)
        session.commit()
        st.success(f"✅ Scadenza '{titolo}' salvata!")

# Visualizzazione
scadenze = session.query(Scadenza).order_by(Scadenza.data_scadenza).all()
if scadenze:
    st.subheader("📅 Scadenze registrate")
    for s in scadenze:
        st.write(f"📌 {s.titolo} – {s.data_scadenza.strftime('%d/%m/%Y')}")
else:
    st.info("🔕 Nessuna scadenza registrata.")