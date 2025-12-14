#!/bin/bash
# Simple Power Menu for Thawrah-X using Rofi
# Make sure you have rofi installed: sudo pacman -S rofi

chosen=$(echo -e "🔒 Lock\n🛑 Logout\n🔄 Reboot\n⏻ Shutdown" | rofi -dmenu -i -p "Power Menu:")

case "$chosen" in
    "🔒 Lock") hyprlock ;;
    "🛑 Logout") loginctl terminate-user $USER ;;
    "🔄 Reboot") systemctl reboot ;;
    "⏻ Shutdown") systemctl poweroff ;;
esac