# 📊 Gemini Data Viewer Chatbot

Una sandbox per una web application interattiva che permette di caricare dataset CSV, analizzarli tramite linguaggio naturale e generare grafici automatici.

Costruita utilizzando **Python (Flask)** per il backend e **Google Gemini 2.5 Flash** come motore di intelligenza artificiale.

# 🤖 AI Disclaimer
Questo progetto è stato sviluppato a scopo educativo e dimostrativo. Il codice è stato generato e rifinito con la collaborazione di un assistente AI (Google Gemini), seguendo un approccio di "Coding Partnership" per l'implementazione dell'architettura Backend/Frontend e l'integrazione delle API.

## ✨ Funzionalità

* **Chat Intelligente:** Interfaccia conversazionale basata su Google Gemini.
* **Analisi Dati Dinamica:** Upload di file CSV direttamente dall'interfaccia.
* **Visualizzazione Automatica:** Generazione di grafici interattivi (Plotly.js) basati sulle richieste dell'utente (es. "Fammi un grafico a barre delle vendite").
* **Context Aware:** Il bot "ricorda" la conversazione precedente per un'analisi continua.

## 🛠️ Tecnologie Utilizzate

* **Backend:** Python, Flask
* **AI Model:** Google Gemini 2.5 Flash (via `google-generative-ai`)
* **Data Processing:** Pandas
* **Frontend:** HTML, CSS, JavaScript
* **Charting:** Plotly.js

## 🚀 Installazione e Utilizzo

### 1. Clona il repository
```bash
git clone [https://github.com/IL_TUO_USERNAME/gemini-data-analyst.git](https://github.com/IL_TUO_USERNAME/gemini-data-analyst.git)
cd gemini-data-analyst
```

### 2. Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 3. Configurazione API Key
Per motivi di sicurezza, la API Key non è inclusa nel codice. Crea un file chiamato config.py nella root del progetto e inserisci la tua chiave:

```Python
# config.py
API_KEY = "INSERISCI_QUI_LA_TUA_CHIAVE_GOOGLE_AI_STUDIO"
```
Puoi ottenere una chiave gratuitamente su Google AI Studio.

### 4. Avvia l'applicazione
```Bash
python app.py
```
Apri il browser all'indirizzo: http://127.0.0.1:5000