from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import pandas as pd
import json
import config
import os

app = Flask(__name__)

# --- CONFIGURAZIONE ---
genai.configure(api_key=config.API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- VARIABILI GLOBALI (Stato dell'applicazione) ---
# Usiamo queste variabili globali per poterle cambiare quando carichi un nuovo file
df = None
csv_info = ""
chat_history = []
CURRENT_FILE = 'dati.csv' # File di default

def load_dataset(filename):
    """Questa funzione legge il CSV e aggiorna le istruzioni per Gemini."""
    global df, csv_info
    
    try:
        df = pd.read_csv(filename)
        # Aggiorniamo la descrizione che daremo a Gemini
        csv_info = f"""
        Le colonne del dataset sono: {list(df.columns)}
        Ecco un'anteprima dei dati (prime righe):
        {df.head(3).to_string()}
        """
        print(f"Dataset caricato: {filename}")
        return True
    except Exception as e:
        print(f"Errore caricamento CSV: {e}")
        csv_info = "Nessun dataset caricato correttamente."
        return False

# Carichiamo il file di default all'avvio
if os.path.exists(CURRENT_FILE):
    load_dataset(CURRENT_FILE)

# --- ROTTE ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Riceve un file dal frontend e aggiorna il sistema."""
    global chat_history
    
    if 'file' not in request.files:
        return jsonify({"error": "Nessun file inviato"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Nome file vuoto"}), 400

    if file:
        # Salviamo il file sovrascrivendo quello attuale (o usandone uno temporaneo)
        # Per semplicità lo chiamiamo sempre 'dataset_corrente.csv'
        filepath = 'dataset_corrente.csv'
        file.save(filepath)
        
        # Ricarichiamo i dati
        success = load_dataset(filepath)
        
        if success:
            # IMPORTANTE: Resettiamo la memoria quando cambiamo i dati!
            chat_history = [] 
            return jsonify({"status": "success", "columns": list(df.columns)})
        else:
            return jsonify({"error": "Il file non sembra un CSV valido"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    user_message = request.json.get('message')

    # Aggiungi messaggio utente
    chat_history.append({"role": "user", "parts": [user_message]})

    # --- PROMPT DINAMICO ---
    # Usiamo 'csv_info' che contiene i dati del file ATTUALMENTE caricato
    system_instruction = f"""
    Sei un analista dati esperto. Hai accesso a un dataset.
    {csv_info}

    IMPORTANTE: Devi rispondere SEMPRE e SOLO usando un oggetto JSON valido. 
    Il formato deve essere:
    {{
        "text": "Risposta testuale breve",
        "plot": {{ ...oggetto JSON Plotly... }} o null
    }}

    Esempio plot: {{ "data": [ {{ "x": [...], "y": [...], "type": "bar" }} ], "layout": {{ "title": "..." }} }}
    """
    
    full_prompt = [{"role": "user", "parts": [system_instruction]}] + chat_history

    try:
        response = model.generate_content(full_prompt)
        text_response = response.text
        
        # Pulizia JSON
        clean_json = text_response.replace('```json', '').replace('```', '').strip()
        response_data = json.loads(clean_json)

        chat_history.append({"role": "model", "parts": [response_data['text']]})
        return jsonify(response_data)

    except Exception as e:
        print(f"Errore: {e}")
        return jsonify({"text": "Errore nell'elaborazione. Forse il dataset è troppo complesso o vuoto.", "plot": None})

if __name__ == '__main__':
    app.run(debug=True)