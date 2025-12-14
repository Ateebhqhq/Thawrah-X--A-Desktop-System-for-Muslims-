#!/usr/bin/env python3
import tkinter as tk
import json
import os
import math

# --- CONFIGURATION ---
BG_COLOR = "#1e1e2e"
GRID_BG = "#313244"   # Empty square color
GRID_FG = "#a6e3a1"   # Read square color (Green)
GRID_CUR = "#ebcb8b"  # Current page color (Gold)
TEXT_COLOR = "#cdd6f4"

CACHE_FILE = os.path.expanduser("~/.cache/thawrah_khatmah.json")
TOTAL_PAGES = 604

class QuranHeatmap:
    def __init__(self, root):
        self.root = root
        self.root.title("Khatmah Progress")
        
        # Center the window
        w, h = 800, 500
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        self.root.configure(bg=BG_COLOR)
        
        # Data Loading
        self.current_page = 0
        self.load_data()

        # UI Header
        header = tk.Frame(root, bg=BG_COLOR)
        header.pack(fill="x", pady=20, padx=20)
        
        tk.Label(header, text="Khatmah Visualization", font=("Amiri", 20, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(side="left")
        
        percent = int((self.current_page / TOTAL_PAGES) * 100)
        tk.Label(header, text=f"{percent}% Complete", font=("Arial", 14, "bold"), bg=BG_COLOR, fg=GRID_FG).pack(side="right")

        # The Grid Canvas
        self.canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.draw_heatmap()
        
        # Legend
        footer = tk.Frame(root, bg=BG_COLOR)
        footer.pack(fill="x", pady=10)
        self.create_legend(footer)

    def load_data(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r') as f:
                    data = json.load(f)
                    self.current_page = data.get("current_page", 0)
            except: pass

    def draw_heatmap(self):
        # Grid settings
        cols = 30 # 30 Juz columns roughly? Or just 30 columns for aesthetics
        rows = math.ceil(TOTAL_PAGES / cols)
        
        sq_size = 22
        gap = 4
        
        start_x = 20
        start_y = 20
        
        for i in range(TOTAL_PAGES):
            page_num = i + 1
            
            # Calculate grid position
            col = i % cols
            row = i // cols
            
            x1 = start_x + (col * (sq_size + gap))
            y1 = start_y + (row * (sq_size + gap))
            x2 = x1 + sq_size
            y2 = y1 + sq_size
            
            # Determine Color
            if page_num < self.current_page:
                color = GRID_FG # Read (Green)
            elif page_num == self.current_page:
                color = GRID_CUR # Current (Gold)
            else:
                color = GRID_BG # Unread (Grey)
            
            # Draw Square
            tag = f"page_{page_num}"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags=tag)
            
            # Hover Effect binding
            self.canvas.tag_bind(tag, "<Enter>", lambda e, p=page_num: self.show_tooltip(e, p))

    def show_tooltip(self, event, page):
        # Simple print to console or update a label for now
        # A full tooltip in Tkinter canvas is complex, but we can change the title
        juz = math.ceil(page / 20)
        self.root.title(f"Page {page} - Juz {juz}")

    def create_legend(self, parent):
        # Helper to draw legend circles
        def draw_dot(color, text):
            f = tk.Frame(parent, bg=BG_COLOR)
            f.pack(side="right", padx=10)
            tk.Canvas(f, width=15, height=15, bg=color, highlightthickness=0).pack(side="left")
            tk.Label(f, text=text, bg=BG_COLOR, fg="#888").pack(side="left", padx=5)

        draw_dot(GRID_BG, "Unread")
        draw_dot(GRID_CUR, "Current")
        draw_dot(GRID_FG, "Completed")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuranHeatmap(root)
    root.mainloop()