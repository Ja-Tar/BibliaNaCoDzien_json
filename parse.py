import json
import re

def parse_html(html_content):
    clean_text = re.sub(r"<.*?>", "", html_content)
    return clean_text

with open("bncd.json", "r+", encoding="utf-8") as file:
    data = json.load(file)
    pierwsze = data[0]["pierwsze"]
    drugie = data[0]["drugie"]
    pierwszeT = parse_html(pierwsze["html"])
    pierwszeA = parse_html(pierwsze["zrodlo"])
    drugieT = parse_html(drugie["html"])
    drugieA = parse_html(drugie["zrodlo"])
    file.seek(0)
    json.dump({
        pierwszeT: pierwszeA,
        drugieT: drugieA
    }, file, ensure_ascii=False, indent=4)
    file.truncate()
