#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import subprocess
import time
import sys
import arabic_reshaper
from bidi.algorithm import get_display

# --- CONFIGURATION ---
BG_COLOR = "#000000"     
GOLD_COLOR = "#ebcb8b"   
TEXT_COLOR = "#cdd6f4"   
DURATION_SECONDS = 4     

# The Dua Text
ARABIC_RAW = "سُبْحَانَكَ اللَّهُمَّ وَبِحَمْدِكَ، أَشْهَدُ أَنْ لاَ إِلَهَ إِلاَّ أَنْتَ، أَسْتَغْفِرُكَ وَأَتُوبُ إِلَيْكَ"
TRANS_TEXT = "Glory is to You, O Allah, and praise is to You.\nI bear witness that there is none worthy of worship but You.\nI seek Your forgiveness and repent to You."

def fix_text(text):
    # This fixes "disconnected" or "backward" Arabic text
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

class KaffaratScreen:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=BG_COLOR)
        self.root.config(cursor="none") 

        # Center Frame
        frame = tk.Frame(root, bg=BG_COLOR)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # ARABIC TEXT (Reshaped)
        self.lbl_arabic = tk.Label(
            frame, 
            text=fix_text(ARABIC_RAW), 
            font=("Noto Sans Arabic", 30, "bold"), 
            fg=GOLD_COLOR, 
            bg=BG_COLOR, 
            wraplength=1200, 
            justify="center"
        )
        self.lbl_arabic.pack(pady=30)

        # ENGLISH TEXT
        self.lbl_trans = tk.Label(
            frame, 
            text=TRANS_TEXT, 
            font=("Arial", 14), 
            fg=TEXT_COLOR, 
            bg=BG_COLOR, 
            wraplength=900, 
            justify="center"
        )
        self.lbl_trans.pack(pady=20)

        # STATUS
        self.lbl_status = tk.Label(
            frame, 
            text=f"System shutting down in {DURATION_SECONDS} seconds...", 
            font=("Arial", 10, "italic"), 
            fg="#555555", 
            bg=BG_COLOR
        )
        self.lbl_status.pack(pady=40)

        # Start the countdown
        self.root.after(DURATION_SECONDS * 1000, self.shutdown_now)

    def shutdown_now(self):
        # ---------------------------------------------------------
        # SAFE MODE: The shutdown line below is commented out (#)
        # ---------------------------------------------------------
        # subprocess.run(["systemctl", "poweroff"]) 
        
        print("✅ Test Passed: Dua displayed, shutdown skipped.")
        
        # Close App
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = KaffaratScreen(root)
    root.mainloop()