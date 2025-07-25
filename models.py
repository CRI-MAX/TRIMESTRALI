from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clienti"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    whatsapp = Column(String)

    scadenze = relationship("Scadenza", back_populates="cliente")

class TipoScadenza(Base):
    __tablename__ = "tipi_scadenza"
    id = Column(Integer, primary_key=True)
    nome = Column(String)

    scadenze = relationship("Scadenza", back_populates="tipo")

class Scadenza(Base):
    __tablename__ = "scadenze"
    id = Column(Integer, primary_key=True)
    titolo = Column(String)
    descrizione = Column(String)
    data_scadenza = Column(Date)

    cliente_id = Column(Integer, ForeignKey("clienti.id"))
    tipo_id = Column(Integer, ForeignKey("tipi_scadenza.id"))

    cliente = relationship("Cliente", back_populates="scadenze")
    tipo = relationship("TipoScadenza", back_populates="scadenze")