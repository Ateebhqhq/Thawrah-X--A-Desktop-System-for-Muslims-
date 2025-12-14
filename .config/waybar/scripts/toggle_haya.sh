#!/usr/bin/env bash

# Check if a shader is currently applied
CURRENT_SHADER=$(hyprctl getoption decoration:screen_shader | grep 'str' | awk '{print $2}')

if [[ "$CURRENT_SHADER" == *"haya.glsl"* ]]; then
    # Turn OFF: Set shader to empty string
    hyprctl keyword decoration:screen_shader "[[EMPTY]]"
    notify-send -u low "👁️ Haya Mode Disabled" "Screen is clear."
else
    # Turn ON: Apply the censorship shader
    hyprctl keyword decoration:screen_shader "~/.config/hypr/shaders/haya.glsl"
    notify-send -u critical "🛡️ Haya Mode Active" "Gaze Lowered."
fi
