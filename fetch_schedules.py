import json
import urllib.request
import urllib.parse
from datetime import datetime

# Mappa dei 12 calendari per l'A.A. 2026/2027
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

# Mesi del primo semestre A.A. 2026/2027
mesi = [9, 10, 11, 12, 1, 2]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

for cal in CALENDARI:
    eventi_cal = []
    
    for m in mesi:
        year_val = ACADEMIC_YEAR if m >= 9 else ACADEMIC_YEAR + 1
        month_str = f"{m:02d}"
        
        url = f"https://storage.portale.unical.it/api/ricerca/cds-websites/{cal['cdscod']}/timetable/?lang=it&academic_year={ACADEMIC_YEAR}&year={cal['year']}&date_year={year_val}&date_month={month_str}&search_teacher=&search_location=&af_cod="
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                # Estrazione flessibile della lista eventi da qualunque struttura ritorni la risposta
                raw_items = []
                if isinstance(data, list):
                    raw_items = data
                elif isinstance(data, dict):
                    if 'results' in data:
                        res = data['results']
                        if isinstance(res, list):
                            raw_items = res
                        elif isinstance(res, dict):
                            for v in res.values():
                                if isinstance(v, list): raw_items.extend(v)
                    elif 'timetable' in data:
                        tt = data['timetable']
                        if isinstance(tt, list):
                            raw_items = tt
                        elif isinstance(tt, dict):
                            for v in tt.values():
                                if isinstance(v, list): raw_items.extend(v)
                    else:
                        for v in data.values():
                            if isinstance(v, list): raw_items.extend(v)

                for item in raw_items:
                    if not isinstance(item, dict):
                        continue
                        
                    materia = item.get('activity_name') or item.get('af_name') or item.get('title') or item.get('description') or 'Lezione'
                    docente = item.get('teacher_name') or item.get('teacher') or item.get('docente') or 'Docente da definire'
                    aula = item.get('location') or item.get('building') or item.get('aula') or 'Aula TBD'
                    
                    # Recupero date e orari
                    date_str = item.get('date') or item.get('day')
                    start_time = item.get('time_start') or item.get('start_time') or item.get('start')
                    end_time = item.get('time_end') or item.get('end_time') or item.get('end')
                    
                    # Parsing della data
                    if date_str:
                        try:
                            dt_obj = datetime.strptime(date_str[:10], '%Y-%m-%d')
                            data_formatted = dt_obj.strftime('%Y-%m-%d')
                            giorno_str = giorni_map.get(dt_obj.weekday(), '')
                        except Exception:
                            continue
                    elif start_time and 'T' in str(start_time):
                        try:
                            dt_obj = datetime.fromisoformat(str(start_time).replace('Z', '+00:00'))
                            data_formatted = dt_obj.strftime('%Y-%m-%d')
                            giorno_str = giorni_map.get(dt_obj.weekday(), '')
                            start_time = dt_obj.strftime('%H:%M')
                            if end_time and 'T' in str(end_time):
                                end_dt = datetime.fromisoformat(str(end_time).replace('Z', '+00:00'))
                                end_time = end_dt.strftime('%H:%M')
                        except Exception:
                            continue
                    else:
                        continue

                    orario_str = f"{start_time} - {end_time}" if start_time and end_time else "Orario non specificato"

                    lesson_obj = {
                        "sheet": cal["sheet"],
                        "cdl_code": cal["cdl_code"],
                        "cdl_name": cal["cdl_name"],
                        "cdl_type": cal["cdl_type"],
                        "year_order": cal["year_order"],
                        "anno": cal["anno"],
                        "color": cal["color"],
                        "data": data_formatted,
                        "giorno": giorno_str,
                        "orario": orario_str,
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
