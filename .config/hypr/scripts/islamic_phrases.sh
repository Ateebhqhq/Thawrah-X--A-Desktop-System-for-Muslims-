#!/bin/bash

# Define phrases
declare -A phrases
phrases["Salam"]="ٱلسَّلَامُ عَلَيْكُمْ"
phrases["Wa Alaykum"]="وَعَلَيْكُمُ ٱلسَّلَامُ"
phrases["Bismillah"]="بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
phrases["InshaAllah"]="إِنْ شَاءَ ٱللَّٰهُ"
phrases["MashaAllah"]="مَا شَاءَ ٱللَّٰهُ"
phrases["JazakAllah"]="جَزَاكَ ٱللَّٰهُ خَيْرًا"
phrases["Alhamdulillah"]="ٱلْحَمْدُ لِلَّٰهِ"
phrases["Astaghfirullah"]="أَسْتَغْفِرُ ٱللَّٰهَ"

# Show Rofi Menu
# We pipe the keys (names) to Rofi
choice=$(printf "%s\n" "${!phrases[@]}" | rofi -dmenu -i -p "📿 Phrasebook")

# If user picked something, type it
if [ -n "$choice" ]; then
    text="${phrases[$choice]}"
    
    # Method 1: Type it out (Cleanest)
    wtype "$text"
    
    # Method 2: Copy & Paste (Faster for long text)
    # echo -n "$text" | wl-copy
    # wtype -M ctrl -k v -m ctrl
fi
