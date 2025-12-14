#!/usr/bin/env python3
import tkinter as tk
import json
import os
import subprocess

# --- CONFIGURATION ---
BG_COLOR = "#11111b"       # Darkest background (Crust)
WHEEL_BG = "#1e1e2e"       # Main Drawer Color (Base)
TEXT_COLOR = "#cdd6f4"     
ACTIVE_COLOR = "#ebcb8b"   # Gold
ACCENT_COLOR = "#89b4fa"   # Blue
HIGHLIGHT_BG = "#313244"   

CACHE_FILE = os.path.expanduser("~/.cache/thawrah_khatmah.json")

# --- DATA ---
JUZ_STARTS = {
    1: 1, 2: 22, 3: 42, 4: 62, 5: 82, 6: 102, 7: 122, 8: 142, 9: 162, 10: 182,
    11: 202, 12: 222, 13: 242, 14: 262, 15: 282, 16: 302, 17: 322, 18: 342, 19: 362, 20: 382,
    21: 402, 22: 422, 23: 442, 24: 462, 25: 482, 26: 502, 27: 522, 28: 542, 29: 562, 30: 582,
    31: 605
}

SURAHS = [
    ("1. Al-Fatiha", 1), ("2. Al-Baqarah", 2), ("3. Al-Imran", 50), ("4. An-Nisa", 77),
    ("5. Al-Ma'idah", 106), ("6. Al-An'am", 128), ("7. Al-A'raf", 151), ("8. Al-Anfal", 177),
    ("9. At-Tawbah", 187), ("10. Yunus", 208), ("11. Hud", 221), ("12. Yusuf", 235),
    ("13. Ar-Ra'd", 249), ("14. Ibrahim", 255), ("15. Al-Hijr", 262), ("16. An-Nahl", 267),
    ("17. Al-Isra", 282), ("18. Al-Kahf", 293), ("19. Maryam", 305), ("20. Ta-Ha", 312),
    ("21. Al-Anbiya", 322), ("22. Al-Hajj", 332), ("23. Al-Mu'minun", 342), ("24. An-Nur", 350),
    ("25. Al-Furqan", 359), ("26. Ash-Shu'ara", 367), ("27. An-Naml", 377), ("28. Al-Qasas", 385),
    ("29. Al-Ankabut", 396), ("30. Ar-Rum", 404), ("31. Luqman", 411), ("32. As-Sajdah", 415),
    ("33. Al-Ahzab", 418), ("34. Saba", 428), ("35. Fatir", 434), ("36. Ya-Sin", 440),
    ("37. As-Saffat", 446), ("38. Sad", 453), ("39. Az-Zumar", 458), ("40. Ghafir", 467),
    ("41. Fussilat", 477), ("42. Ash-Shura", 483), ("43. Az-Zukhruf", 489), ("44. Ad-Dukhan", 496),
    ("45. Al-Jathiyah", 499), ("46. Al-Ahqaf", 502), ("47. Muhammad", 507), ("48. Al-Fath", 511),
    ("49. Al-Hujurat", 515), ("50. Qaf", 518), ("51. Adh-Dhariyat", 520), ("52. At-Tur", 523),
    ("53. An-Najm", 526), ("54. Al-Qamar", 528), ("55. Ar-Rahman", 531), ("56. Al-Waqi'ah", 534),
    ("57. Al-Hadid", 537), ("58. Al-Mujadila", 542), ("59. Al-Hashr", 545), ("60. Al-Mumtahanah", 549),
    ("61. As-Saff", 551), ("62. Al-Jumu'ah", 553), ("63. Al-Munafiqun", 554), ("64. At-Taghabun", 556),
    ("65. At-Talaq", 558), ("66. At-Tahrim", 560), ("67. Al-Mulk", 562), ("68. Al-Qalam", 564),
    ("69. Al-Haqqah", 566), ("70. Al-Ma'arij", 568), ("71. Nuh", 570), ("72. Al-Jinn", 572),
    ("73. Al-Muzzammil", 574), ("74. Al-Muddaththir", 575), ("75. Al-Qiyamah", 577), ("76. Al-Insan", 578),
    ("77. Al-Mursalat", 580), ("78. An-Naba", 582), ("79. An-Nazi'at", 583), ("80. Abasa", 585),
    ("81. At-Takwir", 586), ("82. Al-Infitar", 587), ("83. Al-Mutaffifin", 587), ("84. Al-Inshiqaq", 589),
    ("85. Al-Buruj", 590), ("86. At-Tariq", 591), ("87. Al-A'la", 591), ("88. Al-Ghashiyah", 592),
    ("89. Al-Fajr", 593), ("90. Al-Balad", 594), ("91. Ash-Shams", 595), ("92. Al-Lail", 595),
    ("93. Ad-Duha", 596), ("94. Ash-Sharh", 596), ("95. At-Tin", 597), ("96. Al-Alaq", 597),
    ("97. Al-Qadr", 598), ("98. Al-Bayyinah", 598), ("99. Az-Zalzalah", 599), ("100. Al-Adiyat", 599),
    ("101. Al-Qari'ah", 600), ("102. At-Takathur", 600), ("103. Al-Asr", 601), ("104. Al-Humazah", 601),
    ("105. Al-Fil", 601), ("106. Quraysh", 602), ("107. Al-Ma'un", 602), ("108. Al-Kawthar", 602),
    ("109. Al-Kafirun", 603), ("110. An-Nasr", 603), ("111. Al-Masad", 603), ("112. Al-Ikhlas", 604),
    ("113. Al-Falaq", 604), ("114. An-Nas", 604)
]

class CurvedScroller(tk.Canvas):
    def __init__(self, master, items, width=150, height=280, on_select=None, on_click=None):
        # Using WHEEL_BG to match the parent
        super().__init__(master, width=width, height=height, bg=WHEEL_BG, highlightthickness=0)
        self.items = items
        self.selected_index = 0
        self.on_select = on_select
        self.on_click = on_click
        self.height = height
        self.width = width
        self.offset_y = 0
        self.target_offset = 0
        self.item_height = 40
        self.scroll_speed = 0
        
        self.bind("<Motion>", self.handle_hover)
        self.bind("<Button-1>", self.handle_click)
        self.bind("<Button-4>", lambda e: self.scroll_fixed(-1))
        self.bind("<Button-5>", lambda e: self.scroll_fixed(1))
        
        self.animate()

    def update_items(self, new_items):
        self.items = new_items
        self.target_offset = 0
        self.offset_y = 0
        self.selected_index = 0

    def scroll_fixed(self, direction):
        self.target_offset -= direction * self.item_height
        self.limit_scroll()

    def handle_hover(self, event):
        y = event.y
        threshold = self.height * 0.15
        if y < threshold: self.scroll_speed = 6
        elif y > self.height - threshold: self.scroll_speed = -6
        else:
            self.scroll_speed = 0
            if abs(self.target_offset - self.offset_y) < 1:
                idx = round(-self.target_offset / self.item_height)
                self.target_offset = -idx * self.item_height

    def limit_scroll(self):
        max_scroll = -(len(self.items) - 1) * self.item_height
        if self.target_offset > 0: self.target_offset = 0
        if self.target_offset < max_scroll: self.target_offset = max_scroll

    def handle_click(self, event):
        cy = self.height / 2
        click_offset_from_center = event.y - cy
        index_offset = round(click_offset_from_center / self.item_height)
        target_idx = self.selected_index + index_offset
        if 0 <= target_idx < len(self.items):
            self.jump_to_index(target_idx)
            if self.on_click: self.on_click(self.items[target_idx])

    def jump_to_index(self, index):
        self.target_offset = -index * self.item_height
        self.offset_y = self.target_offset

    def animate(self):
        if self.scroll_speed != 0:
            self.target_offset += self.scroll_speed
            self.limit_scroll()

        self.offset_y += (self.target_offset - self.offset_y) * 0.2
        center_idx = round(-self.offset_y / self.item_height)
        center_idx = max(0, min(center_idx, len(self.items)-1))
        
        if center_idx != self.selected_index:
            self.selected_index = center_idx
            if self.on_select:
                self.on_select(self.items[self.selected_index], center_idx)

        self.delete("all")
        cy = self.height / 2
        
        # Draw "Lens" - A clean curve highlighting the center
        # We draw a small filled rectangle that is nicely rounded
        self.create_rectangle(5, cy-20, self.width-5, cy+20, fill=HIGHLIGHT_BG, outline="", tags="lens")
        self.tag_lower("lens") # Put behind text

        visible_range = int(self.height / self.item_height / 2) + 2
        
        for i in range(center_idx - visible_range, center_idx + visible_range + 1):
            if 0 <= i < len(self.items):
                item_y_pos = cy + (i * self.item_height) + self.offset_y
                dist = abs(cy - item_y_pos)
                scale = max(0.8, 1 - (dist / (self.height * 0.9)))
                font_size = int(12 * scale)
                
                # Simple X-Indent (No crazy curve that cuts off text)
                x_pos = self.width / 2 

                if i == center_idx:
                    color = ACTIVE_COLOR
                    font = ("Arial", 14, "bold")
                else:
                    color = TEXT_COLOR
                    font = ("Arial", font_size, "normal")

                self.create_text(x_pos, item_y_pos, text=str(self.items[i]), font=font, fill=color, anchor="center")

        self.after(20, self.animate)

class QuranLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Quran Nav")
        
        # --- COMPACT GEOMETRY ---
        win_w, win_h = 280, 420 
        pointer_y = root.winfo_pointery()
        screen_h = root.winfo_screenheight()
        screen_w = root.winfo_screenwidth()
        
        y_pos = pointer_y - (win_h // 2)
        if y_pos < 10: y_pos = 10
        if y_pos + win_h > screen_h: y_pos = screen_h - win_h - 10
        x_pos = screen_w - win_w - 60 
        
        self.root.geometry(f"{win_w}x{win_h}+{x_pos}+{y_pos}")
        self.root.overrideredirect(True)
        self.root.configure(bg=BG_COLOR)
        
        # --- BACKGROUND ---
        # A single canvas for the whole window
        self.bg_canvas = tk.Canvas(root, width=win_w, height=win_h, bg=BG_COLOR, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        
        # DRAW THE DRAWER SHAPE (Flat Right, Rounded Left)
        # This creates the "D" shape
        self.bg_canvas.create_rectangle(40, 0, win_w, win_h, fill=WHEEL_BG, outline="")
        self.bg_canvas.create_oval(0, 0, 80, win_h, fill=WHEEL_BG, outline="")
        
        # Subtle Border Line for definition
        self.bg_canvas.create_arc(0, 0, 80, win_h, start=90, extent=180, style=tk.ARC, outline=ACCENT_COLOR, width=2)
        self.bg_canvas.create_line(40, 0, win_w, 0, fill=ACCENT_COLOR, width=2)
        self.bg_canvas.create_line(40, win_h, win_w, win_h, fill=ACCENT_COLOR, width=2)

        # --- UI ELEMENTS ---
        # Position manually over the canvas
        
        # Header
        self.lbl_title = tk.Label(root, text="Juz Index", bg=WHEEL_BG, fg=ACCENT_COLOR, font=("Arial", 12, "bold"))
        self.lbl_title.place(x=60, y=25)
        
        # Use simple text for button to avoid gibberish boxes
        self.btn_mode = tk.Button(root, text="[SWAP]", bg=HIGHLIGHT_BG, fg=TEXT_COLOR, 
                                  bd=0, font=("Arial", 8, "bold"), command=self.toggle_mode, cursor="hand2")
        self.btn_mode.place(x=210, y=25, width=50, height=25)

        # Scrollers
        self.mode = "juz"
        
        self.left_items = [f"Juz {i}" for i in range(1, 31)]
        self.left_scroll = CurvedScroller(root, self.left_items, width=110, height=250, on_select=self.on_left_change)
        self.left_scroll.place(x=30, y=70) 

        self.right_items = [f"Page {i}" for i in range(1, 22)] 
        self.right_scroll = CurvedScroller(root, self.right_items, width=90, height=250, on_click=self.on_page_click)
        self.right_scroll.place(x=160, y=70) 

        # Footer Buttons
        self.btn_play = tk.Button(root, text="PLAY", bg=HIGHLIGHT_BG, fg=ACTIVE_COLOR, 
                                  bd=0, font=("Arial", 9, "bold"), command=self.play_audio, cursor="hand2")
        self.btn_play.place(x=50, y=350, width=80, height=30)
        
        self.btn_read = tk.Button(root, text="READ", bg=HIGHLIGHT_BG, fg=ACCENT_COLOR, 
                                    bd=0, font=("Arial", 9, "bold"), command=self.open_tafsir, cursor="hand2")
        self.btn_read.place(x=150, y=350, width=80, height=30)

        self.load_current_page()
        self.root.focus_force()
        self.root.bind("<FocusOut>", lambda e: self.root.destroy())
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def toggle_mode(self):
        if self.mode == "juz":
            self.mode = "surah"
            self.left_scroll.update_items([s[0] for s in SURAHS])
            self.lbl_title.config(text="Surah Index")
        else:
            self.mode = "juz"
            self.left_scroll.update_items([f"Juz {i}" for i in range(1, 31)])
            self.lbl_title.config(text="Juz Index")

    def on_left_change(self, item, index):
        if self.mode == "juz":
            juz_num = index + 1
            start_page = JUZ_STARTS[juz_num]
            end_page = JUZ_STARTS.get(juz_num + 1, 605) - 1
            pages = [f"Page {p}" for p in range(start_page, end_page + 1)]
            self.right_scroll.update_items(pages)
        else:
            start_page = SURAHS[index][1]
            pages = [f"Page {p}" for p in range(start_page, 605)]
            self.right_scroll.update_items(pages)

    def on_page_click(self, item):
        try:
            p_num = int(item.split()[1])
            self.right_scroll.jump_to_index(self.right_scroll.items.index(item))
            self.save_and_act("tafsir", p_num)
        except: pass

    def load_current_page(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r') as f:
                    data = json.load(f)
                    page = data.get("current_page", 1)
                    target_juz = 1
                    for j, start in JUZ_STARTS.items():
                        if page >= start: target_juz = j
                        else: break
                    self.left_scroll.jump_to_index(target_juz - 1)
                    juz_start = JUZ_STARTS[target_juz]
                    page_idx = page - juz_start
                    self.root.after(50, lambda: self.right_scroll.jump_to_index(page_idx))
            except: pass

    def save_and_act(self, action, page_override=None):
        if page_override:
            page_num = page_override
        else:
            page_str = self.right_scroll.items[self.right_scroll.selected_index]
            page_num = int(page_str.split()[1])
        
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f: data = json.load(f)
        else: data = {"pages_today": 0}
        data["current_page"] = page_num
        data["last_read_date"] = "UPDATED"
        with open(CACHE_FILE, 'w') as f: json.dump(data, f)
        
        url = f"https://quran.com/page/{page_num}"
        if action == "play":
            p_str = str(page_num).zfill(3)
            url = f"https://everyayah.com/data/Alafasy_128kbps/PageMp3s/Page{p_str}.mp3"
            subprocess.Popen(["mpv", "--no-terminal", url])
        elif action == "tafsir":
            subprocess.Popen(['xdg-open', url])
        self.root.destroy()

    def play_audio(self): self.save_and_act("play")
    def open_tafsir(self): self.save_and_act("tafsir")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuranLauncher(root)
    root.mainloop()