#!/bin/bash

# Define your wallpapers directory
wallpaper_dir="/home/ateeb/.config/hypr/wallpapers/"

# Get a random wallpaper from the directory
random_wallpaper=$(ls -1 "$wallpaper_dir" | shuf -n 1)

# Full path to the random wallpaper
full_path="$wallpaper_dir$random_wallpaper"

# Use hyprctl to preload and set the new wallpaper
hyprctl hyprpaper preload "$full_path"
hyprctl hyprpaper wallpaper ",$full_path"
