#!/bin/bash

# This script takes a screenshot of a selected area and copies it to the clipboard.
# It automatically detects if you are using Wayland or Xorg and uses the appropriate tools.

# --- Dependencies ---
# For Wayland: grim, slurp, wl-clipboard (wl-copy)
# For Xorg: scrot, xclip

# Function to check if a command exists
command_exists () {
  type "$1" &> /dev/null ;
}

# Check if Wayland is in use
if [[ -n "$WAYLAND_DISPLAY" ]]; then
  # Wayland
  if ! command_exists grim || ! command_exists slurp || ! command_exists wl-copy; then
    echo "Error: For Wayland, 'grim', 'slurp', and 'wl-copy' are required."
    echo "Please install them using: sudo pacman -S grim slurp wl-clipboard"
    exit 1
  fi
  
  # Take screenshot of selected area and copy to clipboard
  grim -g "$(slurp)" - | wl-copy -t image/png
  echo "Screenshot of selected area copied to clipboard (Wayland)."

elif [[ -n "$DISPLAY" ]]; then
  # Xorg
  if ! command_exists scrot || ! command_exists xclip; then
    echo "Error: For Xorg, 'scrot' and 'xclip' are required."
    echo "Please install them using: sudo pacman -S scrot xclip"
    exit 1
  fi

  # Take screenshot of selected area and copy to clipboard
  scrot -s '/tmp/screenshot.png' && xclip -selection clipboard -t image/png -i '/tmp/screenshot.png' && rm '/tmp/screenshot.png'
  echo "Screenshot of selected area copied to clipboard (Xorg)."

else
  echo "Error: Could not detect display server (Wayland or Xorg)."
  echo "Please ensure either WAYLAND_DISPLAY or DISPLAY environment variables are set."
  exit 1
fi
