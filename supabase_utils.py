from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_scadenze_prossime():
    from datetime import date, timedelta
    oggi = date.today()
    limite = oggi + timedelta(days=7)
    response = supabase.table("scadenze_clienti").select("*").lte("data_scadenza", limite).eq("notificato", False).execute()
    return response.data

def segna_notificato(id):
    supabase.table("scadenze_clienti").update({"notificato": True}).eq("id", id).execute()