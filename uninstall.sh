#!/bin/sh
set -eu

PROJECT_DIR="/oem/printer_data/u1_wled"
SERVICE_DST="/etc/init.d/S62u1-wled"
BOOTCONTROL="/etc/init.d/S99_bootcontrol"
PATCHER="$PROJECT_DIR/bootcontrol_patch.py"

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: run this uninstaller as root." >&2
    exit 1
fi

if [ -x "$SERVICE_DST" ]; then
    "$SERVICE_DST" stop || true
fi

if [ -f "$BOOTCONTROL" ] && [ -f "$PATCHER" ]; then
    python3 "$PATCHER" --remove "$BOOTCONTROL"
else
    echo "WARNING: boot hook was not automatically removed; review $BOOTCONTROL manually."
fi

rm -f "$SERVICE_DST"
echo "Startup integration removed. Project files remain in $PROJECT_DIR for backup/reinstall."
