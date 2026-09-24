import json
import urllib.request

url = "https://storage.portale.unical.it/api/ricerca/cds-websites/0847/timetable/?lang=it&academic_year=2026&year=2&date_year=2026&date_month=09&search_teacher=&search_location=&af_cod="

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        
        print("--- DEBUG RISPOSTA UNICAL ---")
        print("Tipo dato:", type(data))
        if isinstance(data, dict):
            print("Chiavi JSON:", list(data.keys()))
            print("Anteprima JSON:", json.dumps(data, indent=2)[:500])
        elif isinstance(data, list):
            print("Lunghezza lista:", len(data))
            if data:
                print("Primo elemento:", json.dumps(data[0], indent=2))
        print("----------------------------")
except Exception as e:
    print(f"Errore chiamata debug: {e}")

# Mantiene un file vuoto valido per evitare blocchi al workflow
with open('lessons_data.json', 'w', encoding='utf-8') as f:
    json.dump([], f)
