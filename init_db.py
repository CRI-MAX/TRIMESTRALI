# init_db.py

import os
from sqlalchemy import create_engine
from models import Base

DB_PATH = "database.db"

# 🧹 Elimina il database esistente (se presente)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"🗑️ Database esistente '{DB_PATH}' eliminato.")

# 🔨 Crea nuovo database
engine = create_engine(f"sqlite:///{DB_PATH}")
Base.metadata.create_all(engine)

print(f"✅ Nuovo database '{DB_PATH}' creato con successo.")