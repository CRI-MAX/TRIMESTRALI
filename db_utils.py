from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# 🔗 Connessione al database SQLite
engine = create_engine("sqlite:///scadenze.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# 👤 Tabella Cliente
class Cliente(Base):
    __tablename__ = "clienti"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)

    scadenze = relationship("Scadenza", back_populates="cliente")

# 🗂️ Tabella TipoScadenza
class TipoScadenza(Base):
    __tablename__ = "tipi_scadenza"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)

    scadenze = relationship("Scadenza", back_populates="tipo")

# 📅 Tabella Scadenza
class Scadenza(Base):
    __tablename__ = "scadenze"
    id = Column(Integer, primary_key=True)
    titolo = Column(String, nullable=False)
    descrizione = Column(String)
    data_scadenza = Column(Date, nullable=False)

    cliente_id = Column(Integer, ForeignKey("clienti.id"))
    tipo_id = Column(Integer, ForeignKey("tipi_scadenza.id"))

    cliente = relationship("Cliente", back_populates="scadenze")
    tipo = relationship("TipoScadenza", back_populates="scadenze")

# 🛠️ Crea le tabelle se non esistono
Base.metadata.create_all(engine)