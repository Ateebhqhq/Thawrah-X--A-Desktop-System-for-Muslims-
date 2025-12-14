#!/usr/bin/env python3
import sys
import tkinter as tk
from datetime import datetime

# --- COLORS (Catppuccin/Dracula Style) ---
BG_COLOR = "#1e1e2e"
TEXT_COLOR = "#cdd6f4"
GOLD_COLOR = "#ebcb8b"
BTN_COLOR = "#89b4fa"
BTN_TXT = "#1e1e2e"

# --- HARDCODED DATA ---
# This dictionary contains the direct Arabic characters.
DATA = {
    "morning": [
        {
            "arabic": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لاَ إِلَهَ إلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ",
            "translation": "We have entered the morning and at this very time the whole kingdom belongs to Allah, and all praise is due to Allah."
        },
        {
            "arabic": "اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ",
            "translation": "O Allah, by You we enter the morning and by You we enter the evening, by You we live and by You we die, and to You is the Final Return."
        },
        {
            "arabic": "سُبْحَانَ اللهِ وَبِحَمْدِهِ",
            "translation": "Glory is to Allah and all praise is to Him."
        }
    ],
    "evening": [
        {
            "arabic": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ",
            "translation": "We have entered the evening and at this very time the whole kingdom belongs to Allah, and all praise is due to Allah."
        },
        {
            "arabic": "اللَّهُمَّ بِكَ أَمْسَيْنَا وَبِكَ أَصْبَحْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ الْمَصِيرُ",
            "translation": "O Allah, by You we enter the evening and by You we enter the morning, by You we live and by You we die, and to You is the final return."
        },
        {
            "arabic": "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ",
            "translation": "I seek Allah's forgiveness and turn to Him in repentance."
        }
    ]
}

class AdhkaarApp:
    def __init__(self, root, mode):
        self.root = root
        self.adhkaar_list = DATA.get(mode, [])
        self.index = 0
        self.mode = mode.capitalize()

        self.root.title(f"📿 {self.mode} Adhkaar")
        self.root.geometry("750x550")
        self.root.configure(bg=BG_COLOR)

        if not self.adhkaar_list:
            # Fallback if empty (won't crash)
            label = tk.Label(root, text=f"No adhkaar found for {mode}.", bg=BG_COLOR, fg=TEXT_COLOR)
            label.pack(pady=20)
            return

        # Header
        self.header_frame = tk.Frame(root, bg=BG_COLOR)
        self.header_frame.pack(fill="x", pady=20)
        
        self.title_label = tk.Label(
            self.header_frame, 
            text=f"{self.mode} Remembrance", 
            font=("Arial", 16, "bold"), 
            fg=BTN_COLOR, 
            bg=BG_COLOR
        )
        self.title_label.pack()
        
        self.counter_label = tk.Label(
            self.header_frame, 
            text=f"1 / {len(self.adhkaar_list)}", 
            font=("Arial", 10), 
            fg=TEXT_COLOR, 
            bg=BG_COLOR
        )
        self.counter_label.pack()

        # Content Frame
        self.content_frame = tk.Frame(root, bg=BG_COLOR, padx=20)
        self.content_frame.pack(expand=True, fill="both")

        # ARABIC TEXT LABEL
        self.arabic_label = tk.Label(
            self.content_frame, 
            text="", 
            font=("Noto Naskh Arabic", 26, "bold"), 
            fg=GOLD_COLOR, 
            bg=BG_COLOR, 
            wraplength=700, 
            justify="center"
        )
        self.arabic_label.pack(pady=(10, 20))

        # TRANSLATION TEXT LABEL
        self.trans_label = tk.Label(
            self.content_frame, 
            text="", 
            font=("Arial", 12), 
            fg=TEXT_COLOR, 
            bg=BG_COLOR, 
            wraplength=650, 
            justify="center"
        )
        self.trans_label.pack(pady=10)

        # Buttons Frame
        self.btn_frame = tk.Frame(root, bg=BG_COLOR, pady=30)
        self.btn_frame.pack(fill="x")

        self.prev_btn = tk.Button(
            self.btn_frame, 
            text="< Previous", 
            command=self.prev_card, 
            bg=BTN_COLOR, 
            fg=BTN_TXT, 
            font=("Arial", 11, "bold"), 
            bd=0, 
            padx=20, 
            pady=8
        )
        self.prev_btn.pack(side="left", padx=60)

        self.next_btn = tk.Button(
            self.btn_frame, 
            text="Next >", 
            command=self.next_card, 
            bg=BTN_COLOR, 
            fg=BTN_TXT, 
            font=("Arial", 11, "bold"), 
            bd=0, 
            padx=20, 
            pady=8
        )
        self.next_btn.pack(side="right", padx=60)

        self.update_card()

    def update_card(self):
        item = self.adhkaar_list[self.index]
        self.arabic_label.config(text=item['arabic'])
        self.trans_label.config(text=item['translation'])
        self.counter_label.config(text=f"{self.index + 1} / {len(self.adhkaar_list)}")

    def next_card(self):
        if self.index < len(self.adhkaar_list) - 1:
            self.index += 1
            self.update_card()

    def prev_card(self):
        if self.index > 0:
            self.index -= 1
            self.update_card()

def main():
    now = datetime.now()
    hour = now.hour
    mode = None

    # Logic:
    # 1. "test" argument forces Morning mode for debugging
    # 2. Morning: 05:00 - 11:00
    # 3. Evening: 16:00 - 23:00
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        mode = "morning"
    elif 5 <= hour < 11:
        mode = "morning"
    elif 16 <= hour < 23:
        mode = "evening"

    if mode:
        root = tk.Tk()
        app = AdhkaarApp(root, mode)
        root.mainloop()

if __name__ == "__main__":
    main()