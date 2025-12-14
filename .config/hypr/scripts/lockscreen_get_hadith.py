#!/usr/bin/env python3
import json
import textwrap
import random
import urllib.request
import urllib.error

# Configuration
MAX_LENGTH = 300  # Skip verses longer than this characters (too big for screen)
WRAP_WIDTH = 60   # Wrap text after 60 chars

def get_quran_ayah():
    try:
        # Fetch a random Ayah (using Saheeh International translation)
        url = "http://api.alquran.cloud/v1/ayah/random/en.sahih"
        with urllib.request.urlopen(url, timeout=2) as response:
            data = json.loads(response.read().decode())
            
            ayah = data['data']
            text = ayah['text']
            surah = ayah['surah']['englishName']
            number = ayah['numberInSurah']
            
            # Formatting
            if len(text) > MAX_LENGTH:
                return get_quran_ayah() # Retry if too long
                
            formatted_text = textwrap.fill(text, WRAP_WIDTH)
            return f'"{formatted_text}"\n\n— Surah {surah} [{number}]'
    except (urllib.error.URLError, Exception):
        # Fallback if offline
        return '"Verily, with hardship comes ease."\n\n— Surah Ash-Sharh [94:6]'

# You can expand this to fetch Hadith if you find a stable API, 
# but currently most Hadith APIs are slow or require keys. 
# For now, this script defaults to Quran.

if __name__ == "__main__":
    print(get_quran_ayah())
