import json
import os

# The correct data with proper Arabic and no missing fields
data = {
    "morning": [
        {
            "arabic": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ",
            "translation": "We have entered the morning and at this very time the whole kingdom belongs to Allah."
        },
        {
            "arabic": "اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا",
            "translation": "O Allah, by You we enter the morning and by You we enter the evening."
        },
        {
            "arabic": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لاَ إِلَهَ إلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ",
            "translation": "We have entered the morning and at this very time the whole kingdom belongs to Allah, and all praise is due to Allah. There is none worthy of worship but Allah, the One who has no partner."
        }
    ],
    "evening": [
        {
            "arabic": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ",
            "translation": "We have entered the evening and at this very time the whole kingdom belongs to Allah."
        },
        {
            "arabic": "اللَّهُمَّ بِكَ أَمْسَيْنَا وَبِكَ أَصْبَحْنَا",
            "translation": "O Allah, by You we enter the evening and by You we enter the morning."
        }
    ]
}

# Path to your file
db_path = os.path.expanduser("~/.config/waybar/scripts/adhkaar_db.json")

# Write it with ensure_ascii=False to force real Arabic characters
with open(db_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("✅ Database successfully reset with readable Arabic!")