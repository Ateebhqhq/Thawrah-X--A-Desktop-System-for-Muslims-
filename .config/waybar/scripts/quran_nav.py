#!/usr/bin/env python3
import tkinter as tk
import json
import os
import math
import webbrowser
import sys

# --- CONFIGURATION ---
# Colors (Catppuccin Mocha)
BG_COLOR = "#1e1e2e"       # Dark Background
TEXT_COLOR = "#6c7086"     # Dimmed Text
ACTIVE_COLOR = "#ebcb8b"   # Gold (Center Item)
HIGHLIGHT_BG = "#313244"   # Selection Bar Background

# File Paths
CACHE_FILE = os.path.expanduser("~/.cache/thawrah_khatmah.json")
TOTAL_PAGES = 604

# Madani Mushaf: Approx start page for each Juz (1-30)
JUZ_STARTS = {
    1: 1, 2: 22, 3: 42, 4: 62, 5: 82, 6: 102, 7: 122, 8: 142, 9: 162, 10: 182,
    11: 202, 12: 222, 13: 242, 14: 262, 15: 282, 16: 302, 17: 322, 18: 342, 19: 362, 20: 382,
    21: 402, 22: 422, 23: 442, 24: 462, 25: 482, 26: 502, 27: 522, 28: 542, 29: 562, 30: 582
}

class CurvedScroller(tk.Canvas):
    def __init__(self, master, items, width=100, height=300, on_select=None):
        super().__init__(master, width=width, height=height, bg=BG_COLOR, highlightthickness=0)
        self.items = items
        self.selected_index = 0
        self.on_select = on_select
        self.height = height
        self.width = width
        
        # Physics / Animation variables
        self.offset_y = 0
        self.target_offset = 0
        self.item_height = 40
        self.scroll_speed = 0
        
        # Bindings
        self.bind("<Motion>", self.handle_hover)
        self.bind("<Button-1>", self.handle_click)
        self.bind("<MouseWheel>", self.handle_wheel) # Windows/MacOS
        self.bind("<Button-4>", lambda e: self.scroll_fixed(-1)) # Linux Scroll Up
        self.bind("<Button-5>", lambda e: self.scroll_fixed(1))  # Linux Scroll Down
        
        self.animate()

    def scroll_fixed(self, direction):
        """Standard mouse wheel scrolling"""
        self.target_offset -= direction * self.item_height
        self.limit_scroll()

    def handle_wheel(self, event):
        """Windows/Mac scroll support"""
        self.target_offset += event.delta
        self.limit_scroll()

    def handle_hover(self, event):
        """
        The 'Curved' Effect Logic:
        If mouse is at top 20% -> Scroll Up
        If mouse is at bottom 20% -> Scroll Down
        """
        y = event.y
        threshold = self.height * 0.25 # Top/Bottom 15% trigger zone
        
        if y < threshold:
            self.scroll_speed = 5  # Scroll down (content moves down)
        elif y > self.height - threshold:
            self.scroll_speed = -5 # Scroll up (content moves up)
        else:
            self.scroll_speed = 0
            # Snap to nearest item when not scrolling
            if abs(self.target_offset - self.offset_y) < 1:
                idx = round(-self.target_offset / self.item_height)
                self.target_offset = -idx * self.item_height

    def limit_scroll(self):
        """Keep the scroll within bounds"""
        max_scroll = -(len(self.items) - 1) * self.item_height
        if self.target_offset > 0: self.target_offset = 0
        if self.target_offset < max_scroll: self.target_offset = max_scroll

    def handle_click(self, event):
        """Select the item currently in the center"""
        center_y = self.height / 2
        # Logic to find which item is clicked or effectively selected
        # For this design, we just use the center item
        if self.on_select:
            self.on_select(self.items[self.selected_index])

    def update_items(self, new_items):
        self.items = new_items
        self.target_offset = 0
        self.offset_y = 0
        self.selected_index = 0

    def animate(self):
        # 1. Apply auto-scroll (from hover)
        if self.scroll_speed != 0:
            self.target_offset += self.scroll_speed
            self.limit_scroll()

        # 2. Smoothly interpolate current offset to target
        self.offset_y += (self.target_offset - self.offset_y) * 0.2

        # 3. Calculate selected index based on center
        center_idx = round(-self.offset_y / self.item_height)
        center_idx = max(0, min(center_idx, len(self.items)-1))
        
        if center_idx != self.selected_index:
            self.selected_index = center_idx
            if self.on_select:
                self.on_select(self.items[self.selected_index])

        # 4. Draw
        self.delete("all")
        
        # Draw Selection Highlight Bar
        cy = self.height / 2
        self.create_rectangle(10, cy - 20, self.width-10, cy + 20, fill=HIGHLIGHT_BG, outline="")

        # Draw Items with "Curved" math
        visible_range = int(self.height / self.item_height / 2) + 2
        
        for i in range(center_idx - visible_range, center_idx + visible_range + 1):
            if 0 <= i < len(self.items):
                # Distance from center
                item_y_pos = cy + (i * self.item_height) + self.offset_y
                dist = abs(cy - item_y_pos)
                
                # Math for the "Curve": 
                # Further from center = smaller font + transparent color + x-indent
                scale = max(0.6, 1 - (dist / (self.height * 0.8)))
                font_size = int(14 * scale)
                
                # Color fade
                if i == center_idx:
                    color = ACTIVE_COLOR
                    font_weight = "bold"
                    x_pos = self.width / 2  # Center
                else:
                    color = TEXT_COLOR
                    font_weight = "normal"
                    # Indent slightly to right to simulate 3D cylinder
                    x_pos = (self.width / 2) + (dist * 0.1) 

                self.create_text(
                    x_pos, item_y_pos, 
                    text=str(self.items[i]), 
                    font=("Noto Sans", font_size, font_weight), 
                    fill=color
                )

        # Loop
        self.after(20, self.animate)

class QuranLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Quran Nav")
        
        # Window Setup (Frameless, Right Side)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        win_w, win_h = 240, 400
        
        # Position at Top-Right (adjust x/y as needed for your bar)
        x_pos = screen_width - win_w - 10 
        y_pos = 50 
        
        self.root.geometry(f"{win_w}x{win_h}+{x_pos}+{y_pos}")
        self.root.overrideredirect(True) # Remove borders
        self.root.configure(bg=BG_COLOR)
        
        # Exit on focus loss (Close when clicking away)
        self.root.bind("<FocusOut>", lambda e: self.root.destroy())
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # Header
        lbl = tk.Label(root, text="Select Page", bg=BG_COLOR, fg=ACTIVE_COLOR, font=("Arial", 12, "bold"))
        lbl.pack(pady=10)

        # Container for Scrollers
        container = tk.Frame(root, bg=BG_COLOR)
        container.pack(expand=True, fill="both", padx=10, pady=10)

        # -- LEFT SCROLLER (Juz) --
        self.juz_items = [f"Juz {i}" for i in range(1, 31)]
        self.left_scroll = CurvedScroller(
            container, 
            self.juz_items, 
            width=100, 
            height=300, 
            on_select=self.on_juz_change
        )
        self.left_scroll.pack(side="left", padx=5)

        # -- RIGHT SCROLLER (Page) --
        self.right_scroll = CurvedScroller(
            container, 
            [], 
            width=100, 
            height=300, 
            on_select=None
        )
        self.right_scroll.pack(side="right", padx=5)
        
        # Double Click Action (on the Page scroller)
        self.right_scroll.bind("<Button-1>", self.on_page_confirm)
        
        # Initialize
        self.on_juz_change("Juz 1")
        self.root.focus_force()

    def on_juz_change(self, juz_str):
        # Parse "Juz 5" -> 5
        juz_num = int(juz_str.split()[1])
        
        start_page = JUZ_STARTS[juz_num]
        # End page is start of next Juz - 1, or 604 if last
        next_juz = juz_num + 1
        end_page = JUZ_STARTS.get(next_juz, 605) - 1
        
        pages = [f"Page {p}" for p in range(start_page, end_page + 1)]
        self.right_scroll.update_items(pages)

    def on_page_confirm(self, event=None):
        # Get selected page
        idx = self.right_scroll.selected_index
        if 0 <= idx < len(self.right_scroll.items):
            page_str = self.right_scroll.items[idx]
            page_num = int(page_str.split()[1])
            
            self.save_and_open(page_num)

    def save_and_open(self, page_num):
        # 1. Update the JSON file so Waybar updates
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = {"pages_today": 0}
            
        data["current_page"] = page_num
        # Update date if needed
        data["last_read_date"] = "UPDATED" # Simple trigger for main script to handle date
        
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)

        # 2. Open the Page
        # Option A: Online (Quran.com)
        url = f"https://quran.com/page/{page_num}"
        webbrowser.open(url)
        
        # Option B: Local PDF (Uncomment to use)
        # os.system(f"zathura ~/Documents/Quran.pdf -P {page_num} &")

        print(f"Opened Page {page_num}")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuranLauncher(root)
    root.mainloop()