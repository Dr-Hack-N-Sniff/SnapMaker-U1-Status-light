#!/bin/sh

set -u

BASE="/oem/printer_data/u1_wled"
SERVICE_SRC="$BASE/S62u1-wled"
SERVICE_DST="/etc/init.d/S62u1-wled"
BOOT="/etc/init.d/S99_bootcontrol"
HOOK="/etc/init.d/S62u1-wled start"

fail() {
    echo "ERROR: $1" >&2
    exit 1
}

[ "$(id -u)" = "0" ] || fail "Run this installer as root."
[ -f "$BASE/u1_wled.py" ] || fail "$BASE/u1_wled.py is missing."
[ -f "$SERVICE_SRC" ] || fail "$SERVICE_SRC is missing."
[ -f "$BOOT" ] || fail "$BOOT was not found. This firmware layout may be different."

if ! command -v python3 >/dev/null 2>&1; then
    fail "python3 was not found."
fi

if [ "$(tail -n 1 "$BOOT")" != "exit 0" ]; then
    fail "$BOOT does not end with 'exit 0'. Refusing to patch it automatically."
fi

mkdir -p "$BASE/backups"

if [ ! -f "$BASE/backups/S99_bootcontrol.original" ]; then
    cp "$BOOT" "$BASE/backups/S99_bootcontrol.original" || fail "Could not back up S99_bootcontrol."
    echo "Saved original boot script to $BASE/backups/S99_bootcontrol.original"
fi

cp "$SERVICE_SRC" "$SERVICE_DST" || fail "Could not install service launcher."
chmod +x "$SERVICE_DST" || fail "Could not set service permissions."
chmod +x "$BASE/u1_wled.py" 2>/dev/null || true

if grep -Fq "$HOOK" "$BOOT"; then
    echo "Boot hook already present."
else
    cp "$BOOT" "$BASE/backups/S99_bootcontrol.before-last-patch" || fail "Could not save pre-patch backup."
    sed -i '$i /etc/init.d/S62u1-wled start' "$BOOT" || fail "Could not patch S99_bootcontrol."
    echo "Added U1 WLED boot hook."
fi

"$SERVICE_DST" restart
sleep 2

if "$SERVICE_DST" status; then
    echo ""
    echo "Install complete."
    echo "Log: $BASE/u1_wled.log"
    echo ""
    echo "Recommended final test:"
    echo "  1. Set WLED to a clearly different color."
    echo "  2. Reboot the U1."
    echo "  3. Verify the bridge changes WLED back to the correct printer state."
else
    fail "The service did not remain running. Check $BASE/u1_wled.log"
fi
