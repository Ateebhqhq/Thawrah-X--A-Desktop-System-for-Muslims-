#!/bin/bash

# This script will write its findings to a log file in your /tmp directory.
LOG_FILE="/tmp/mic_debug.log"

# ---- SCRIPT STARTS ----
echo "--- Script started at $(date) ---" >> "$LOG_FILE"

echo "Running as user: $(whoami)" >> "$LOG_FILE"
echo "PATH is: $PATH" >> "$LOG_FILE"
echo "DBUS_SESSION_BUS_ADDRESS is: $DBUS_SESSION_BUS_ADDRESS" >> "$LOG_FILE"
echo "---------------------------" >> "$LOG_FILE"

# Define the audio source
ID="@DEFAULT_AUDIO_SOURCE@"

# Toggle mute first
wpctl set-mute "$ID" toggle
sleep 0.1 # Give it a moment

# Check the volume status and log it
echo "Checking volume status for ID: $ID" >> "$LOG_FILE"
wpctl get-volume "$ID" >> "$LOG_FILE" 2>&1
WpctlExitCode=$?
echo "wpctl exit code: $WpctlExitCode" >> "$LOG_FILE"
echo "---------------------------" >> "$LOG_FILE"

if wpctl get-volume "$ID" | grep -q "MUTED"; then
    echo "Condition met: Microphone is MUTED." >> "$LOG_FILE"
    notify-send "🎙️ Microphone Muted"
    NotifyExitCode=$?
else
    echo "Condition met: Microphone is UNMUTED." >> "$LOG_FILE"
    notify-send "🎙️ Microphone Unmuted"
    NotifyExitCode=$?
fi

echo "notify-send command finished with exit code: $NotifyExitCode" >> "$LOG_FILE"
echo "--- Script finished ---" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
