import json
import re
import requests

def parse_html(html_content):
    clean_text = re.sub(r"<.*?>", "", html_content)
    return clean_text

def get_api():
    # https://biblianacodzien.pl/bncd/api/dzien/2025-06-15
    response = requests.get("https://biblianacodzien.pl/bncd/api/dzien/2025-06-15/?format=json", headers={"validator": "91191088458083487087536214688", "User-Agent": "Mozilla/5.0"}, timeout=100)
    if response.status_code == 200:
        return response.json()
    response.raise_for_status()
    
def create_file(data):
    with open("bncd.json", "w", encoding="utf-8") as file:
        pierwsze = data[0]["pierwsze"]
        drugie = data[0]["drugie"]
        pierwszeT = parse_html(pierwsze["html"])
        pierwszeA = parse_html(pierwsze["zrodlo"])
        drugieT = parse_html(drugie["html"])
        drugieA = parse_html(drugie["zrodlo"])
        file.seek(0)
        json.dump([
            {
                "author": pierwszeA,
                "content": pierwszeT,
            },
            {
                "author": drugieA,
                "content": drugieT,
            }
        ], file, ensure_ascii=False, indent=4)
        file.truncate()

def main():
    create_file(get_api())

if __name__ == "__main__":
    main()
