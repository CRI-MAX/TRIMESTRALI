import os
import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Cliente, TipoScadenza, Scadenza
from db_utils import (
    aggiungi_scadenza_test,
    esporta_tutte_scadenze
)

TEST_DB_PATH = "test_scadenze.db"
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"

@pytest.fixture(scope="module")
def session():
    engine = create_engine(TEST_DB_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()
    engine.dispose()

def teardown_module(module):
    try:
        os.remove(TEST_DB_PATH)
    except PermissionError:
        print("⚠️ Il file test_scadenze.db è ancora in uso e non può essere eliminato.")

def test_aggiunta_cliente_e_tipo(session):
    cliente = Cliente(nome="Cliente Test")
    tipo = TipoScadenza(nome="Tipo Test")
    session.add_all([cliente, tipo])
    session.commit()
    assert cliente.id is not None
    assert tipo.id is not None

def test_aggiunta_scadenza(session):
    cliente = session.query(Cliente).first()
    tipo = session.query(TipoScadenza).first()
    scadenza = aggiungi_scadenza_test(
        session,
        "Scadenza Test",
        date(2025, 7, 25),
        cliente_id=cliente.id,
        tipo_id=tipo.id
    )
    assert scadenza.id is not None

def test_modifica_scadenza(session):
    scadenza = session.query(Scadenza).first()
    scadenza.descrizione = "Scadenza Modificata"
    session.commit()
    updated = session.get(Scadenza, scadenza.id)
    assert updated.descrizione == "Scadenza Modificata"

def test_eliminazione_scadenza(session):
    scadenza = session.query(Scadenza).first()
    session.delete(scadenza)
    session.commit()
    deleted = session.get(Scadenza, scadenza.id)
    assert deleted is None

def test_filtra_per_cliente(session):
    cliente = Cliente(nome="Cliente Filtro")
    session.add(cliente)
    session.commit()
    scadenza = aggiungi_scadenza_test(session, "Filtro Cliente", date.today(), cliente_id=cliente.id)
    results = session.query(Scadenza).filter(Scadenza.cliente_id == cliente.id).all()
    assert len(results) == 1

def test_filtra_per_tipo(session):
    tipo = TipoScadenza(nome="Tipo Filtro")
    session.add(tipo)
    session.commit()
    scadenza = aggiungi_scadenza_test(session, "Filtro Tipo", date.today(), tipo_id=tipo.id)
    results = session.query(Scadenza).filter(Scadenza.tipo_id == tipo.id).all()
    assert len(results) == 1

def test_esportazione(session):
    export_path = "test_export.txt"
    aggiungi_scadenza_test(session, "Export Test", date.today())
    esporta_tutte_scadenze(session, export_path)
    assert os.path.exists(export_path)
    with open(export_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Export Test" in content
    os.remove(export_path)