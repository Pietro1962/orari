import json
import urllib.request
import urllib.parse
from datetime import datetime

# Mappa dei 12 calendari basata sulle API ufficiali UniCal Storage
CALENDARI = [
    # Triennali
    {"sheet": "Economia I", "cdl_code": "ECONOMIA", "cdl_name": "CdL Triennale in Economia", "cdl_type": "Triennale", "year_order": 1, "anno": "1° anno", "color": "#1e3a8a", "cdscod": "0733", "year": 1},
    {"sheet": "Economia II", "cdl_code": "ECONOMIA", "cdl_name": "CdL Triennale in Economia", "cdl_type": "Triennale", "year_order": 2, "anno": "2° anno", "color": "#1e40af", "cdscod": "0733", "year": 2},
    {"sheet": "Economia III", "cdl_code": "ECONOMIA", "cdl_name": "CdL Triennale in Economia", "cdl_type": "Triennale", "year_order": 3, "anno": "3° anno", "color": "#1d4ed8", "cdscod": "0733", "year": 3},
    
    {"sheet": "SDS I", "cdl_code": "SDS", "cdl_name": "CdL Triennale in Statistica per Data Science", "cdl_type": "Triennale", "year_order": 1, "anno": "1° anno", "color": "#065f46", "cdscod": "0847", "year": 1},
    {"sheet": "SDS II", "cdl_code": "SDS", "cdl_name": "CdL Triennale in Statistica per Data Science", "cdl_type": "Triennale", "year_order": 2, "anno": "2° anno", "color": "#047857", "cdscod": "0847", "year": 2},
    {"sheet": "SDS III", "cdl_code": "SDS", "cdl_name": "CdL Triennale in Statistica per Data Science", "cdl_type": "Triennale", "year_order": 3, "anno": "3° anno", "color": "#059669", "cdscod": "0847", "year": 3},
    
    # Magistrali
    {"sheet": "EIS I", "cdl_code": "EIS", "cdl_name": "CdL Magistrale in Economia, Imprese e Sostenibilità", "cdl_type": "Magistrale", "year_order": 1, "anno": "1° anno", "color": "#9a3412", "cdscod": "0820", "year": 1},
    {"sheet": "EIS II", "cdl_code": "EIS", "cdl_name": "CdL Magistrale in Economia, Imprese e Sostenibilità", "cdl_type": "Magistrale", "year_order": 2, "anno": "2° anno", "color": "#c2410c", "cdscod": "0820", "year": 2},
    
    {"sheet": "DSSA I", "cdl_code": "DSSA", "cdl_name": "CdL Magistrale in Data Science per le Strategie Aziendali", "cdl_type": "Magistrale", "year_order": 1, "anno": "1° anno", "color": "#6b21a8", "cdscod": "0848", "year": 1},
    {"sheet": "DSSA II", "cdl_code": "DSSA", "cdl_name": "CdL Magistrale in Data Science per le Strategie Aziendali", "cdl_type": "Magistrale", "year_order": 2, "anno": "2° anno", "color": "#7e22ce", "cdscod": "0848", "year": 2},
    
    {"sheet": "Finance I", "cdl_code": "FINANCE", "cdl_name": "CdL Magistrale in Finance and Insurance", "cdl_type": "Magistrale", "year_order": 1, "anno": "1° anno", "color": "#831843", "cdscod": "0766", "year": 1},
    {"sheet": "Finance II", "cdl_code": "FINANCE", "cdl_name": "CdL Magistrale in Finance and Insurance", "cdl_type": "Magistrale", "year_order": 2, "anno": "2° anno", "color": "#9f1239", "cdscod": "0766", "year": 2}
]

ACADEMIC_YEAR = 2026
all_lessons = []
giorni_map = {0: 'Lunedì', 1: 'Martedì', 2: 'Mercoledì', 3: 'Giovedì', 4: 'Venerdì', 5: 'Sabato', 6: 'Domenica'}

# Mesi del semestre (Settembre - Febbraio)
mesi = [9, 10, 11, 12, 1, 2]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

for cal in CALENDARI:
    eventi_cal = []
    
    for m in mesi:
        year_val = ACADEMIC_YEAR if m >= 9 else ACADEMIC_YEAR + 1
        url = f"https://storage.portale.unical.it/api/ricerca/cds-websites/{cal['cdscod']}/timetable/?lang=it&academic_year={ACADEMIC_YEAR}&year={cal['year']}&date_year={year_val}&date_month={m}&search_teacher=&search_location=&af_cod="
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                # La risposta può essere una lista o un dizionario contenente la chiave 'results' / 'timetable'
                items = []
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict):
                    items = data.get('results', data.get('timetable', data.get('events', [])))
                
                for item in items:
                    materia = item.get('title', item.get('af_name', item.get('description', 'Lezione')))
                    docente = item.get('teacher', item.get('teacher_name', 'Docente da definire'))
                    aula = item.get('location', item.get('building', 'Aula TBD'))
                    
                    start_str = item.get('start', item.get('start_time'))
                    end_str = item.get('end', item.get('end_time'))
                    
                    if not start_str or not end_str:
                        continue

                    # Parsing della data/ora
                    try:
                        start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                        end_dt = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                    except Exception:
                        continue

                    lesson_obj = {
                        "sheet": cal["sheet"],
                        "cdl_code": cal["cdl_code"],
                        "cdl_name": cal["cdl_name"],
                        "cdl_type": cal["cdl_type"],
                        "year_order": cal["year_order"],
                        "anno": cal["anno"],
                        "color": cal["color"],
                        "data": start_dt.strftime('%Y-%m-%d'),
                        "giorno": giorni_map.get(start_dt.weekday(), ''),
                        "orario": f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}",
                        "materia": materia,
                        "docente": docente,
                        "aula": aula
                    }
                    eventi_cal.append(lesson_obj)
        except Exception as e:
            pass

    all_lessons.extend(eventi_cal)
    print(f"[{cal['sheet']}] Scaricati {len(eventi_cal)} eventi da UniCal Storage.")

# Salvataggio dati scaricati nel file JSON
with open('lessons_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_lessons, f, ensure_ascii=False, indent=4)

print(f"\n--- COMPLETATO --- Totale lezioni scaricate per A.A. 2026/2027: {len(all_lessons)}")
