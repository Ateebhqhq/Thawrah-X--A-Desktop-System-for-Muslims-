#!/bin/bash

ARABIC="أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ"
ENGLISH="We have entered the morning and at this very time the whole kingdom belongs to Allah."

# GTK_THEME forces dark mode so you don't get the white box
# --class="adhkaar" matches the Hyprland rule we made
GTK_THEME=Adwaita:dark yad --title="Morning Remembrance" \
    --class="adhkaar" \
    --width=600 \
    --height=250 \
    --center \
    --window-icon="emblem-default" \
    --text="<span font='Noto Naskh Arabic Bold 24' foreground='#ebcb8b'>$ARABIC</span>\n\n<span font='Arial 12' foreground='#cdd6f4'>$ENGLISH</span>" \
    --button="Close":0 \
    --undecorated \
    --text-align=center \
    --back="#1e1e2e" \
    --fore="#cdd6f4"