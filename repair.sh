#!/bin/sh
set -eu

PROJECT_DIR="/oem/printer_data/u1_wled"
SERVICE_DST="/etc/init.d/S62u1-wled"
BOOTCONTROL="/etc/init.d/S99_bootcontrol"
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BACKUP_DIR="$PROJECT_DIR/backups"

if [ "$HERE" != "$PROJECT_DIR" ]; then
    echo "ERROR: copy the release files to $PROJECT_DIR and run this script there." >&2
    exit 1
fi

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: run this repair script as root." >&2
    exit 1
fi

for f in S62u1-wled bootcontrol_patch.py; do
    [ -f "$HERE/$f" ] || { echo "ERROR: missing $HERE/$f" >&2; exit 1; }
done
[ -f "$BOOTCONTROL" ] || { echo "ERROR: $BOOTCONTROL not found" >&2; exit 1; }

mkdir -p "$PROJECT_DIR" "$BACKUP_DIR"
STAMP=$(date +%Y%m%d-%H%M%S)
cp "$BOOTCONTROL" "$BACKUP_DIR/S99_bootcontrol.repair.$STAMP.bak"

cp "$HERE/S62u1-wled" "$SERVICE_DST"
chmod +x "$PROJECT_DIR/S62u1-wled" "$PROJECT_DIR/bootcontrol_patch.py" "$SERVICE_DST"

python3 "$PROJECT_DIR/bootcontrol_patch.py" "$BOOTCONTROL"
"$SERVICE_DST" restart
sleep 2
"$SERVICE_DST" status

echo "Repair complete."
