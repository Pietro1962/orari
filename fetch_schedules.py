import json
import urllib.request
import urllib.parse
from datetime import datetime

# Elenco dei 12 calendari UP Cineca A.A. 2026/2027
CALENDARI = [
    {"sheet": "Economia I", "cdl_code": "ECONOMIA", "cdl_name": "CdL Triennale in Economia", "cdl_type": "Triennale", "year_order": 1, "anno": "1° anno", "color": "#1e3a8a", "id": "6a63231e7e6b9600bbc5fd93"},
    {"sheet": "Economia II", "cdl_code": "ECONOMIA", "cdl_name": "CdL Triennale in Economia", "cdl_type": "Triennale", "year_order": 2, "anno": "2° anno", "color": "#1e40af", "id": "6a632535aae8aa00b5594f76"},
    {"sheet": "Economia III", "cdl_code": "ECONOMIA", "cdl_name": "CdL Triennale in Economia", "cdl_type": "Triennale", "year_order": 3, "anno": "3° anno", "color": "#1d4ed8", "id": "6a632799de54e8007a24a1a0"},
    {"sheet": "SDS I", "cdl_code": "SDS", "cdl_name": "CdL Triennale in Statistica per Data Science", "cdl_type": "Triennale", "year_order": 1, "anno": "1° anno", "color": "#065f46", "id": "6a63238b7e6b9600bbc5fdc1"},
    {"sheet": "SDS II", "cdl_code": "SDS", "cdl_name": "CdL Triennale in Statistica per Data Science", "cdl_type": "Triennale", "year_order": 2, "anno": "2° anno", "color": "#047857", "id": "6a63257e9e36710014cd0620"},
    {"sheet": "SDS III", "cdl_code": "SDS", "cdl_name": "CdL Triennale in Statistica per Data Science", "cdl_type": "Triennale", "year_order": 3, "anno": "3° anno", "color": "#059669", "id": "6a6327d4de54e8007a24a1d0"},
    {"sheet": "EIS I", "cdl_code": "EIS", "cdl_name": "CdL Magistrale in Economia, Imprese e Sostenibilità", "cdl_type": "Magistrale", "year_order": 1, "anno": "1° anno", "color": "#9a3412", "id": "6a632453de54e8007a24a06c"},
    {"sheet": "EIS II", "cdl_code": "EIS", "cdl_name": "CdL Magistrale in Economia, Imprese e Sostenibilità", "cdl_type": "Magistrale", "year_order": 2, "anno": "2° anno", "color": "#c2410c", "id": "6a632663acb9d70071d051e4"},
    {"sheet": "DSSA I", "cdl_code": "DSSA", "cdl_name": "CdL Magistrale in Data Science per le Strategie Aziendali", "cdl_type": "Magistrale", "year_order": 1, "anno": "1° anno", "color": "#6b21a8", "id": "6a6323ea7bf6a400143cf32a"},
    {"sheet": "DSSA II", "cdl_code": "DSSA", "cdl_name": "CdL Magistrale in Data Science per le Strategie Aziendali", "cdl_type": "Magistrale", "year_order": 2, "anno": "2° anno", "color": "#7e22ce", "id": "6a6325d84a2373001968598c"},
    {"sheet": "Finance I", "cdl_code": "FINANCE", "cdl_name": "CdL Magistrale in Finance and Insurance", "cdl_type": "Magistrale", "year_order": 1, "anno": "1° anno", "color": "#831843", "id": "6a6324b3b0e7470014a6276b"},
    {"sheet": "Finance II", "cdl_code": "FINANCE", "cdl_name": "CdL Magistrale in Finance and Insurance", "cdl_type": "Magistrale", "year_order": 2, "anno": "2° anno", "color": "#9f1239", "id": "6a6326b34a237300196859e1"}
]

# Definizione intervallo accademico
PRIMA_DATA = "2026-09-01T00:00:00.000Z"
ULTIMA_DATA = "2027-07-31T23:59:59.000Z"

all_lessons = []
giorni_map = {0: 'Lunedì', 1: 'Martedì', 2: 'Mercoledì', 3: 'Giovedì', 4: 'Venerdì', 5: 'Sabato', 6: 'Domenica'}

for cal in CALENDARI:
    params = urllib.parse.urlencode({
        'linkCalendarioId': cal['id'],
        'primaData': PRIMA_DATA,
        'ultimaData': ULTIMA_DATA
    })
    url = f"https://unical.prod.up.cineca.it/api/CalendarioPubblico/getEventiCalendarioPubblico?{params}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            # Gestione sia di lista diretta che di dizionario con chiave 'eventi' o 'eventiCalendario'
            eventi = []
            if isinstance(data, list):
                eventi = data
            elif isinstance(data, dict):
                eventi = data.get('eventi', data.get('eventiCalendario', []))

            for ev in eventi:
                # Estrazione dati materia
                materia = ev.get('title', ev.get('insegnamento', ev.get('nomeEvent', 'Lezione')))
                
                # Estrazione docenti ed aule dalle risorse annidate se presenti
                docenti_list = []
                aule_list = []
                for res in ev.get('risorse', []):
                    if res.get('type') == 'DOCENTE' or 'docente' in res.get('tipo', '').lower():
                        docenti_list.append(res.get('nome', ''))
                    elif res.get('type') == 'AULA' or 'aula' in res.get('tipo', '').lower():
                        aule_list.append(res.get('nome', ''))
                
                docente = ", ".join(docenti_list) if docenti_list else ev.get('docente', 'Docente da definire')
                aula = ", ".join(aule_list) if aule_list else ev.get('aula', 'Aula TBD')
                
                # Parsing orari
                start_raw = ev.get('start', ev.get('oraInizio'))
                end_raw = ev.get('end', ev.get('oraFine'))
                
                if not start_raw or not end_raw:
                    continue

                start_dt = datetime.fromisoformat(start_raw.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end_raw.replace('Z', '+00:00'))
                
                giorno_ita = giorni_map.get(start_dt.weekday(), '')
                orario_str = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
                data_str = start_dt.strftime('%Y-%m-%d')
                
                lesson_obj = {
                    "sheet": cal["sheet"],
                    "cdl_code": cal["cdl_code"],
                    "cdl_name": cal["cdl_name"],
                    "cdl_type": cal["cdl_type"],
                    "year_order": cal["year_order"],
                    "anno": cal["anno"],
                    "color": cal["color"],
                    "data": data_str,
                    "giorno": giorno_ita,
                    "orario": orario_str,
                    "materia": materia,
                    "docente": docente,
                    "aula": aula
                }
                all_lessons.append(lesson_obj)
                
        print(f"[{cal['sheet']}] Scaricati {len(eventi)} eventi.")
    except Exception as e:
        print(f"Errore recupero {cal['sheet']}: {e}")

# Salva i dati scaricati nel file JSON
with open('lessons_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_lessons, f, ensure_ascii=False, indent=4)

print(f"\nOperazione completata! Recuperati in totale {len(all_lessons)} eventi da CINECA.")
