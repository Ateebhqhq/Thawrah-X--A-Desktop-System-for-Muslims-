#!/usr/bin/env python3
import json
import time
import math
import os
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# --- CONFIGURATION ---
CACHE_FILE = os.path.expanduser("~/.cache/thawrah_prayers.json")
STATE_FILE = "/tmp/thawrah_prayer_state"
ADHAN_FILE = os.path.expanduser("~/.config/waybar/scripts/adhan.mp3")

# --- UTILS ---
def send_notification(title, message):
    # Added -t 900000 (15 mins)
    subprocess.run(["notify-send", "-u", "critical", "-t", "900000", title, message])

def play_adhan():
    if os.path.exists(ADHAN_FILE):
        subprocess.Popen(["mpv", "--no-terminal", "--volume=15", ADHAN_FILE])

def get_location():
    """Detects location via IP address."""
    try:
        with urllib.request.urlopen("https://ipapi.co/json/", timeout=5) as url:
            data = json.loads(url.read().decode())
            return data['latitude'], data['longitude'], data['city']
    except:
        return None, None, None

def get_qibla(lat, lon):
    # KAABA Coordinates (Fixed)
    kaaba_lat = 21.4225
    kaaba_lon = 39.8262

    # Convert all to radians
    lat_rad = math.radians(float(lat))
    lon_rad = math.radians(float(lon))
    k_lat_rad = math.radians(kaaba_lat)
    k_lon_rad = math.radians(kaaba_lon)

    # The "Great Circle" Formula
    lon_delta = k_lon_rad - lon_rad
    y = math.sin(lon_delta) * math.cos(k_lat_rad)
    x = math.cos(lat_rad) * math.sin(k_lat_rad) - math.sin(lat_rad) * math.cos(k_lat_rad) * math.cos(lon_delta)
    
    # Calculate Angle and convert to Degrees
    angle = math.degrees(math.atan2(y, x))
    
    # Normalize to 0-360 degrees
    qibla_deg = (angle + 360) % 360
    
    # Convert degrees to text (e.g., "South-East")
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    index = int(round(qibla_deg / 45))
    direction_text = directions[index]

    return int(qibla_deg), direction_text

def fetch_times_online(lat, lon):
    """Fetches prayer times from Aladhan API."""
    try:
        # Method 3 = Muslim World League. Change 'method' param if needed.
        api_url = f"http://api.aladhan.com/v1/timings/{int(time.time())}?latitude={lat}&longitude={lon}&method=3"
        with urllib.request.urlopen(api_url, timeout=5) as url:
            data = json.loads(url.read().decode())
            return data['data'] # Contains 'timings' and 'date'
    except:
        return None

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def save_cache(data):
    # Create dir if not exists
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, 'w') as f:
        json.dump(data, f)

# --- MAIN LOGIC ---
def main():
    # 1. Try to load today's cache first
    cached_data = load_cache()
    today_str = datetime.now().strftime("%d-%m-%Y")
    
    current_times = None
    location_name = "Unknown"
    
    # Variables to hold coordinates for Qibla
    lat = None
    lon = None

    # Check if cache is valid for TODAY
    if cached_data and cached_data.get('date', {}).get('gregorian', {}).get('date') == today_str:
        current_times = cached_data['timings']
        location_name = cached_data.get('meta', {}).get('timezone', 'Cached')
        # Extract lat/lon from cache so we can still calc Qibla offline
        lat = cached_data.get('meta', {}).get('latitude')
        lon = cached_data.get('meta', {}).get('longitude')
    else:
        # Cache is old or missing -> Fetch from Internet
        lat, lon, city = get_location()
        if lat and lon:
            fetched_data = fetch_times_online(lat, lon)
            if fetched_data:
                current_times = fetched_data['timings']
                # Inject date into data structure for cache validation
                fetched_data['date']['gregorian']['date'] = today_str 
                save_cache(fetched_data)
                location_name = city
        
        # If internet failed and we have NO cache, use old cache as fallback
        if not current_times and cached_data:
            current_times = cached_data['timings']
            location_name = "Offline"
            lat = cached_data.get('meta', {}).get('latitude')
            lon = cached_data.get('meta', {}).get('longitude')

    # If everything failed (No net, no cache)
    if not current_times:
        print(json.dumps({"text": "🚫 No Net", "tooltip": "Connect to internet to fetch prayer times", "class": "error"}))
        return

    # 2. Calculate Next Prayer
    # API returns strings like "18:45". We need to compare them.
    timings = {k: v for k, v in current_times.items() if k in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']}
    
    now = datetime.now()
    min_diff_minutes = 9999
    next_prayer_name = None
    
    # Sort prayers by time
    sorted_prayers = []
    for name, time_str in timings.items():
        # Handle formats like "18:45 (CET)" by taking first 5 chars
        clean_time = time_str[:5]
        p_time = datetime.strptime(f"{now.strftime('%Y-%m-%d')} {clean_time}", "%Y-%m-%d %H:%M")
        sorted_prayers.append((name, p_time))

    # Find the next one
    found_next = False
    for name, p_time in sorted(sorted_prayers, key=lambda x: x[1]):
        diff = (p_time - now).total_seconds() / 60
        if diff > 0:
            min_diff_minutes = int(diff)
            next_prayer_name = name
            found_next = True
            break
    
    # If no prayer left today, point to Fajr tomorrow
    if not found_next:
        next_prayer_name = "Fajr (Tom)"
        # Get Fajr time and add 24 hours to difference
        fajr_time = [p[1] for p in sorted_prayers if p[0] == 'Fajr'][0]
        diff_seconds = ((fajr_time + timedelta(days=1)) - now).total_seconds()
        min_diff_minutes = int(diff_seconds / 60)

    # 3. Format Output text (e.g. "-2h 10m")
    if min_diff_minutes >= 60:
        h = min_diff_minutes // 60
        m = min_diff_minutes % 60
        output_text = f"{next_prayer_name} -{h}h {m}m"
    else:
        output_text = f"{next_prayer_name} -{min_diff_minutes}m"

    # 4. Handle Notifications & Audio
    current_state = ""
    if min_diff_minutes <= 15 and min_diff_minutes > 0:
        current_state = "soon"
    elif min_diff_minutes == 0:
        current_state = "now"

    last_state = ""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f: last_state = f.read().strip()

    if current_state == "soon" and last_state != "soon":
        send_notification("⏳ Prepare for Salah", f"{next_prayer_name} is in {min_diff_minutes} min.")
        with open(STATE_FILE, "w") as f: f.write("soon")
        
    if current_state == "now" and last_state != "now":
        send_notification("🕌 It is time for Salah", f"Time for {next_prayer_name}.")
        play_adhan()
        with open(STATE_FILE, "w") as f: f.write("now")

    if current_state == "" and last_state != "":
         with open(STATE_FILE, "w") as f: f.write("")

    # 5. Output JSON for Waybar
    
    # Qibla Calculation Logic
    qibla_text = ""
    if lat and lon:
        q_deg, q_dir = get_qibla(lat, lon)
        qibla_text = f"📍 Qibla: {q_deg}° {q_dir}\n"
    
    tooltip = f"Location: {location_name}\n{qibla_text}\n" + "\n".join([f"{name}: {time}" for name, time in timings.items()])
    
    json_data = {
        "text": f"🕌 {output_text}",
        "tooltip": tooltip,
        "class": "prayer-soon" if min_diff_minutes < 15 else "prayer-far"
    }
    print(json.dumps(json_data))

if __name__ == "__main__":
    main()