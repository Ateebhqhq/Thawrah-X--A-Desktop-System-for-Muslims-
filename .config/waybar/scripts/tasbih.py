#!/usr/bin/env python3
import sys
import os
import json

# Configuration
CACHE_FILE = os.path.expanduser("~/.cache/thawrah_tasbih")
START_COUNT = 33
DHIKR_NAME = "SubhanAllah" # You can change this to Alhamdulillah/AllahuAkbar

def load_count():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return int(f.read().strip())
        except:
            return START_COUNT
    return START_COUNT

def save_count(n):
    with open(CACHE_FILE, 'w') as f:
        f.write(str(n))

def main():
    # Handle Arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "dec":
            count = load_count()
            count -= 1
            if count < 0: count = START_COUNT # Reset loop
            save_count(count)
            
        elif command == "reset":
            save_count(START_COUNT)

    # Output for Waybar
    count = load_count()
    
    # Change color based on progress
    if count == 0:
        text_color = "#a6e3a1" # Green when done
        icon = "✅"
    else:
        text_color = "#cdd6f4" # White normal
        icon = "📿"

    output = {
        "text": f"{icon} {DHIKR_NAME}: {count}",
        "tooltip": "Press Super + . to count",
        "class": "tasbih-done" if count == 0 else "tasbih-active",
        "percentage": count
    }
    
    print(json.dumps(output))

if __name__ == "__main__":
    main()
