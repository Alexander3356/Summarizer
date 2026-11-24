
## Requisiti

- Python 3.10 o superiore
- MySQL
- Connessione Internet per utilizzare il modello SBERT

## Installazione

Crea e attiva un ambiente virtuale:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Installa le dipendenze:

```powershell
pip install -r requirements.txt
```

Copia `.env.example` in un nuovo file chiamato `.env` e inserisci i tuoi dati. 

Crea il database MySQL:

```sql
CREATE DATABASE smart_summarizer
```

## Database

Per usare le migration:

```powershell
flask --app app.py db upgrade
```


## Avvio

```powershell
python app.py
```

Apri `http://127.0.0.1:5000` nel browser.



## Test

```powershell
pip install -r requirements-dev.txt
pytest
```

I test sostituiscono temporaneamente la funzione SBERT con una funzione di prova.

## Variabili di ambiente

- `SECRET_KEY`: chiave utilizzata da Flask per sessioni e protezione dei form. La scegli tu.
- `DATABASE_URL`: indirizzo completo di connessione al database.
- `SBERT_MODEL`: identificativo del modello Sentence Transformers.
