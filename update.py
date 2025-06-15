import json
import re
import requests
import datetime
import math

def parse_html(html_content):
    clean_text = re.sub(r"<.*?>", "", html_content)
    return clean_text

def get_validator():
    e = datetime.datetime.now(datetime.timezone.utc)
    n = [5, 13, 9, 22, 1517]
    r = e.minute + n[0]
    result = ''.join([
    f"{math.log(r) / math.log(65):.5f}".split('.')[1],
    f"{math.log(e.hour + n[1]) / math.log(r):.5f}".replace('.', ''),
    f"{math.log(e.day + n[2]) / math.log(r):.5f}".replace('.', ''),
    f"{math.log(e.month + n[3]) / math.log(r):.5f}".replace('.', ''),
    f"{math.log(e.year + n[4]) / math.log(r):.5f}".replace('.', ''),
    ])
    return result

def get_api():
    # https://biblianacodzien.pl/bncd/api/dzien/2025-06-15
    # Example date: 2025-06-15
    today = datetime.date.today()
    date = today.strftime("%Y-%m-%d")
    response = requests.get(f"https://biblianacodzien.pl/bncd/api/dzien/{date}", headers={"validator": get_validator(), "User-Agent": "Mozilla/5.0"}, timeout=500)
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
