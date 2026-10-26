import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)
    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)

    input_tipo=ft.TextField(label='Tipo')
    input_marca=ft.TextField(label='Marca')
    input_annoacquisto=ft.TextField(label='Anno acquisto')


    valore_corrente=[0]
    valore=ft.TextField(value=str(valore_corrente[0]),width=50, text_align=ft.TextAlign.CENTER) # text_align=ft.TextAlign.CENTER centra il testo
                                                                                                # width imposta la larghezza del campo


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def incrementa_valore(e):

        valore_corrente[0]+=1
        valore.value = str(valore_corrente[0])
        page.update()

    def decrementa_valore(e):

        if valore_corrente[0] > 0:
            valore_corrente[0]-=1
            valore.value = str(valore_corrente[0])
            page.update()

    # funzione aggiungi_strumento
    def aggiungi_strumento(e):

        tipo=input_tipo.value.strip() # recupera cio che l'utente ha scritto nel campo Tipo
        marca=input_marca.value.strip() # recupera la marca
        anno=input_annoacquisto.value.strip() # recupera l'anno

        if tipo=='' or marca=='':
            alert.show_alert('❌ ERRORE:inserisci il tipo e la marca dello strumento') #alert.show_alert(...) mostra una finestra di dialogo attraverso la classe AlertManager
            return

        #controllo che l'anno sia un numero intero
        try:
            anno=int(anno)
        except ValueError:
            alert.show_alert("❌ ERRORE:inserisci valori numerici validi per l'anno di acquisto")
            return

        #aggiunta dello strumento al deposito
        deposito.aggiungi_strumento(tipo,marca,anno,valore_corrente[0])

        #svuota i campi dopo l'aggiunta per consentire un nuovo inserimento
        input_tipo.value=''
        input_marca.value=''
        input_annoacquisto.value=''

        # azzero contatore dopo l'aggiunta e aggiorno il campo grafico
        valore_corrente[0]=0
        valore.value=str(valore_corrente[0])

        #aggiorna la lista degli strumenti
        aggiorna_lista_strumenti()

        # aggiorna interfaccia
        page.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento

    pulsante_aggiungi_strumento=ft.Button('Aggiungi strumento', on_click=aggiungi_strumento)
    pulsante_decrementa=ft.IconButton(icon=ft.Icons.REMOVE, on_click=decrementa_valore,icon_color='Red') #icon=ft.Icons.REMOVE(mostra il simbolo meno)
    pulsante_incrementa=ft.IconButton(icon=ft.Icons.ADD,on_click=incrementa_valore,icon_color='Green')   #icon=ft.Icons.ADD (mostra il simbolo più)
    # on_click collega ciascun pulsante alla propria funzione

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(), # crea una linea divisoria nell'interfaccia grafica , per separare visivamente due elementi o sezioni
        ft.Text('Aggiungi Nuovo Strumento', size=20),
        ft.Row(spacing=20,
            controls=[input_tipo,input_marca,input_annoacquisto,pulsante_decrementa,valore,pulsante_incrementa],
               alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(spacing=200,
               controls=[pulsante_aggiungi_strumento],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
