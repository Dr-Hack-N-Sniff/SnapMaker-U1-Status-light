#!/bin/sh
set -eu

PROJECT_DIR="/oem/printer_data/u1_wled"
SERVICE_DST="/etc/init.d/S62u1-wled"
HEARTBEAT_SERVICE_DST="/etc/init.d/S63u1-wled-heartbeat"
BOOTCONTROL="/etc/init.d/S99_bootcontrol"
PATCHER="$PROJECT_DIR/bootcontrol_patch.py"
BACKUP_DIR="$PROJECT_DIR/backups"
CANDIDATE="/tmp/S99_bootcontrol.candidate"

if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: run this uninstaller as root." >&2
    exit 1
fi

[ -f "$BOOTCONTROL" ] || {
    echo "ERROR: $BOOTCONTROL not found." >&2
    echo "No live WLED service or boot files were changed." >&2
    exit 1
}

[ -f "$PATCHER" ] || {
    echo "ERROR: $PATCHER not found." >&2
    echo "No live WLED service or boot files were changed." >&2
    exit 1
}

#
# Build and validate the proposed S99_bootcontrol with only
# the WLED hooks removed. Do not touch the live system yet.
#
rm -f "$CANDIDATE"
cp "$BOOTCONTROL" "$CANDIDATE"

if ! python3 "$PATCHER" --remove "$CANDIDATE"; then
    rm -f "$CANDIDATE"
    echo "ERROR: current firmware boot configuration is not compatible with this uninstaller." >&2
    echo "No live WLED service or boot files were changed." >&2
    exit 1
fi

if ! sh -n "$CANDIDATE"; then
    rm -f "$CANDIDATE"
    echo "ERROR: proposed S99_bootcontrol failed shell validation." >&2
    echo "No live WLED service or boot files were changed." >&2
    exit 1
fi

#
# Candidate validated. Back up the CURRENT boot configuration.
# Never restore an older S99_bootcontrol during uninstall.
#
mkdir -p "$BACKUP_DIR"
STAMP=$(date +%Y%m%d-%H%M%S)
cp "$BOOTCONTROL" "$BACKUP_DIR/S99_bootcontrol.uninstall.$STAMP.bak"

#
# Now it is safe to stop the WLED services.
#
if [ -x "$SERVICE_DST" ]; then
    "$SERVICE_DST" stop || true
fi

if [ -x "$HEARTBEAT_SERVICE_DST" ]; then
    "$HEARTBEAT_SERVICE_DST" stop || true
fi

#
# Install the already-validated boot configuration.
# This removes only the WLED S62/S63 hooks and preserves
# unrelated entries such as S64u1-camera.
#
cp "$CANDIDATE" "$BOOTCONTROL"
rm -f "$CANDIDATE"

rm -f "$SERVICE_DST" "$HEARTBEAT_SERVICE_DST"

echo "WLED startup integration removed."
echo "Project files remain in $PROJECT_DIR for backup/reinstall."