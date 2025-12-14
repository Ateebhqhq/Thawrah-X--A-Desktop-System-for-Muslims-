#!/usr/bin/env python3
import sys
import os
import json
import math
from datetime import datetime

# --- CONFIGURATION ---
CACHE_FILE = os.path.expanduser("~/.cache/thawrah_khatmah.json")
TOTAL_PAGES = 604 

def load_data():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"current_page": 0, "last_read_date": datetime.now().strftime("%Y-%m-%d"), "pages_today": 0}

def save_data(data):
    with open(CACHE_FILE, 'w') as f:
        json.dump(data, f)

def get_juz(page):
    if page <= 0: return 0
    return math.ceil(page / 20)

def main():
    data = load_data()
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Reset daily counter
    if data.get("last_read_date") != today_str:
        data["pages_today"] = 0
        data["last_read_date"] = today_str

    # Handle direct commands (Right click decrement)
    if len(sys.argv) > 1 and sys.argv[1] == "dec":
        if data["current_page"] > 0:
            data["current_page"] -= 1
            if data["pages_today"] > 0: data["pages_today"] -= 1
        save_data(data)

    # --- OUTPUT TO WAYBAR ---
    page = data["current_page"]
    juz = get_juz(page)
    percentage = int((page / TOTAL_PAGES) * 100)
    
    icon = "📖"
    if page >= TOTAL_PAGES: icon = "🎉"
    
    text = f"{icon} Page {page}"
    if page == 0: text = f"{icon} Start Reading"

    tooltip = (f"<b>Quran Progress</b>\n"
               f"----------------\n"
               f"Juz: {juz}\n"
               f"Pages Today: {data['pages_today']}\n"
               f"Progress: {percentage}%")

    print(json.dumps({
        "text": text,
        "tooltip": tooltip,
        "class": "khatmah-active",
        "percentage": percentage
    }))

if __name__ == "__main__":
    main()