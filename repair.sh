#!/bin/sh
set -eu

PROJECT_DIR="/oem/printer_data/u1_wled"
SERVICE_DST="/etc/init.d/S62u1-wled"
HEARTBEAT_SERVICE_DST="/etc/init.d/S63u1-wled-heartbeat"
BOOTCONTROL="/etc/init.d/S99_bootcontrol"
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BACKUP_DIR="$PROJECT_DIR/backups"
CANDIDATE="/tmp/S99_bootcontrol.candidate"

if [ "$HERE" != "$PROJECT_DIR" ]; then
    echo "ERROR: copy the release files to $PROJECT_DIR and run this script there." >&2
    exit 1
fi

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: run this repair script as root." >&2
    exit 1
fi

for f in S62u1-wled S63u1-wled-heartbeat bootcontrol_patch.py; do
    [ -f "$HERE/$f" ] || {
        echo "ERROR: missing $HERE/$f" >&2
        exit 1
    }
done

[ -f "$BOOTCONTROL" ] || {
    echo "ERROR: $BOOTCONTROL not found" >&2
    exit 1
}

# Validate service scripts before touching live init files.
if ! sh -n "$HERE/S62u1-wled"; then
    echo "ERROR: S62u1-wled failed shell validation." >&2
    echo "No live WLED service or boot files were changed." >&2
    exit 1
fi

if ! sh -n "$HERE/S63u1-wled-heartbeat"; then
    echo "ERROR: S63u1-wled-heartbeat failed shell validation." >&2
    echo "No live WLED service or boot files were changed." >&2
    exit 1
fi

# Build and validate a proposed S99_bootcontrol before changing
# any live service or boot files.
rm -f "$CANDIDATE"
cp "$BOOTCONTROL" "$CANDIDATE"

if ! python3 "$PROJECT_DIR/bootcontrol_patch.py" "$CANDIDATE"; then
    rm -f "$CANDIDATE"
    echo "ERROR: current firmware boot configuration is not compatible with this repair." >&2
    echo "No live WLED service or boot files were changed." >&2
    exit 1
fi

if ! sh -n "$CANDIDATE"; then
    rm -f "$CANDIDATE"
    echo "ERROR: proposed S99_bootcontrol failed shell validation." >&2
    echo "No live WLED service or boot files were changed." >&2
    exit 1
fi

# Validation passed. Back up the current boot configuration.
mkdir -p "$PROJECT_DIR" "$BACKUP_DIR"
STAMP=$(date +%Y%m%d-%H%M%S)
cp "$BOOTCONTROL" "$BACKUP_DIR/S99_bootcontrol.repair.$STAMP.bak"

# Install validated service scripts.
cp "$HERE/S62u1-wled" "$SERVICE_DST"
cp "$HERE/S63u1-wled-heartbeat" "$HEARTBEAT_SERVICE_DST"

chmod +x \
    "$PROJECT_DIR/S62u1-wled" \
    "$PROJECT_DIR/S63u1-wled-heartbeat" \
    "$PROJECT_DIR/bootcontrol_patch.py" \
    "$SERVICE_DST" \
    "$HEARTBEAT_SERVICE_DST"

# Replace live S99 only with the already validated candidate.
cp "$CANDIDATE" "$BOOTCONTROL"
rm -f "$CANDIDATE"

"$SERVICE_DST" restart
"$HEARTBEAT_SERVICE_DST" restart

sleep 2

"$SERVICE_DST" status
"$HEARTBEAT_SERVICE_DST" status

echo "Repair complete."