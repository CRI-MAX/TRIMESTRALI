from db_utils import (
    get_session,
    mostra_alert,
    aggiungi_scadenza,
    modifica_scadenza,
    elimina_scadenza,
    mostra_tutte_scadenze,
    cerca_scadenze,
    esporta_tutte_scadenze,
    filtra_scadenze
)

def main():
    session = get_session()
    print("📆 Benvenuto nel gestore di scadenze!")

    while True:
        print("\n📜 Menu:")
        print("1. Mostra scadenze urgenti")
        print("2. Aggiungi scadenza")
        print("3. Modifica scadenza")
        print("4. Elimina scadenza")
        print("5. Mostra tutte le scadenze")
        print("6. Cerca scadenze")
        print("7. Esporta tutte le scadenze in file")
        print("8. Filtra scadenze per cliente o tipo")
        print("0. Esci")

        scelta = input("➡️ Scegli un'opzione: ")

        if scelta == "1":
            mostra_alert(session)
        elif scelta == "2":
            aggiungi_scadenza(session)
        elif scelta == "3":
            modifica_scadenza(session)
        elif scelta == "4":
            elimina_scadenza(session)
        elif scelta == "5":
            mostra_tutte_scadenze(session)
        elif scelta == "6":
            cerca_scadenze(session)
        elif scelta == "7":
            esporta_tutte_scadenze(session)
        elif scelta == "8":
            filtra_scadenze(session)
        elif scelta == "0":
            print("👋 Uscita dal programma.")
            break
        else:
            print("❌ Scelta non valida.")

if __name__ == "__main__":
    main()