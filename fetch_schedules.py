import json
import urllib.request
from datetime import datetime

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
        month_str = f"{m:02d}"
        
        url = f"https://storage.portale.unical.it/api/ricerca/cds-websites/{cal['cdscod']}/timetable/?lang=it&academic_year={ACADEMIC_YEAR}&year={cal['year']}&date_year={year_val}&date_month={month_str}&search_teacher=&search_location=&af_cod="
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                items = json.loads(response.read().decode('utf-8'))
                if not isinstance(items, list):
                    continue

                for item in items:
                    materia = item.get('insegnamento', 'Lezione')
                    
                    # Formattazione Docenti
                    docenti_list = item.get('docenti', [])
                    docente = ", ".join(docenti_list) if docenti_list else "Docente da definire"
                    
                    # Formattazione Aule
                    aule_raw = item.get('aule', [])
                    aule_formatted = []
                    for a in aule_raw:
                        nome_aula = a.get('nome', '')
                        edificio = a.get('edificio', '')
                        if nome_aula and edificio:
                            aule_formatted.append(f"{nome_aula} ({edificio})")
                        elif nome_aula:
                            aule_formatted.append(nome_aula)
                    aula = ", ".join(aule_formatted) if aule_formatted else "Aula TBD"
                    
                    # Date e Orari
                    data_str = item.get('dataInizio')
                    ora_inizio = item.get('orarioInizio', '')
                    ora_fine = item.get('orarioFine', '')
                    
                    if not data_str:
                        continue

                    try:
                        dt_obj = datetime.strptime(data_str[:10], '%Y-%m-%d')
                        giorno_str = giorni_map.get(dt_obj.weekday(), '')
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
                        "data": dt_obj.strftime('%Y-%m-%d'),
                        "giorno": giorno_str,
                        "orario": f"{ora_inizio} - {ora_fine}" if ora_inizio and ora_fine else "Orario TBD",
                        "materia": materia,
                        "docente": docente,
                        "aula": aula
                    }
                    eventi_cal.append(lesson_obj)
        except Exception as e:
            pass

    all_lessons.extend(eventi_cal)
    print(f"[{cal['sheet']}] Scaricate {len(eventi_cal)} lezioni.")

# Salvataggio nel file JSON per l'interfaccia web
with open('lessons_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_lessons, f, ensure_ascii=False, indent=4)

print(f"\n--- COMPLETATO --- Totale lezioni scaricate per A.A. 2026/2027: {len(all_lessons)}")
