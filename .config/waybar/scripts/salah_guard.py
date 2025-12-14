#!/usr/bin/env python3
import json
import time
import os
import subprocess
from datetime import datetime

# --- CONFIGURATION ---
CACHE_FILE = os.path.expanduser("~/.cache/thawrah_prayers.json")
LOCK_CMD = "hyprlock"  
NOTIFICATION_TIMEOUT_MS = 900000  # 15 Minutes in milliseconds

def load_prayer_times():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                data = json.load(f)
                today_str = datetime.now().strftime("%d-%m-%Y")
                if data.get('date', {}).get('gregorian', {}).get('date') == today_str:
                    return data['timings']
        except:
            return None
    return None

def send_notification(urgency, title, message):
    # Added "-t" flag to make it expire after 15 mins
    subprocess.run([
        "notify-send", 
        "-u", urgency, 
        "-t", str(NOTIFICATION_TIMEOUT_MS), 
        title, 
        message
    ])

def main():
    print("🛡️ Salah Guard Active (Locking BEFORE prayer)...")
    
    last_locked_prayer = None
    warning_sent_for = None

    while True:
        timings = load_prayer_times()
        
        if timings:
            now = datetime.now()
            target_prayers = {k: v for k, v in timings.items() if k in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']}

            for name, time_str in target_prayers.items():
                clean_time = time_str[:5]
                p_time = datetime.strptime(f"{now.strftime('%Y-%m-%d')} {clean_time}", "%Y-%m-%d %H:%M")
                
                # Calculate difference in minutes
                # Negative result = Before Prayer
                # Positive result = After Prayer
                diff = (now - p_time).total_seconds() / 60
                
                # --- NEW LOGIC: LOCK BEFORE PRAYER ---
                
                # TRIGGER 1: WARNING (6 minutes BEFORE prayer)
                # Gives you 1 minute to finish up before the lock at -5
                if -6.0 <= diff < -5.0:
                    if warning_sent_for != name:
                        send_notification("critical", "⚠️ Salah Guard", f"System will lock in 1 minute for {name}.")
                        warning_sent_for = name
                
                # TRIGGER 2: THE LOCK (5 minutes BEFORE prayer)
                elif -5.0 <= diff < -4.0:
                    if last_locked_prayer != name:
                        print(f"🔒 Locking for {name}")
                        send_notification("critical", "🔒 Salah Guard", f"Time to prepare for {name}. Locking system.")
                        time.sleep(3) 
                        subprocess.run([LOCK_CMD]) 
                        last_locked_prayer = name
                        warning_sent_for = None 
        
        time.sleep(10)

if __name__ == "__main__":
    main()