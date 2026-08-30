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

[ "$(id -u)" = "0" ] || fail "Run this repair script as root."
[ -f "$BASE/u1_wled.py" ] || fail "$BASE/u1_wled.py is missing."
[ -f "$SERVICE_SRC" ] || fail "$SERVICE_SRC is missing."
[ -f "$BOOT" ] || fail "$BOOT was not found."

# Important: repair the CURRENT firmware's S99_bootcontrol in place.
# Do not replace it with an old firmware copy.
if [ "$(tail -n 1 "$BOOT")" != "exit 0" ]; then
    fail "$BOOT does not end with 'exit 0'. Refusing to patch it automatically."
fi

mkdir -p "$BASE/backups"
cp "$BOOT" "$BASE/backups/S99_bootcontrol.pre-repair" || fail "Could not back up current S99_bootcontrol."

cp "$SERVICE_SRC" "$SERVICE_DST" || fail "Could not restore service launcher."
chmod +x "$SERVICE_DST" || fail "Could not set service permissions."

if grep -Fq "$HOOK" "$BOOT"; then
    echo "Boot hook is already present."
else
    sed -i '$i /etc/init.d/S62u1-wled start' "$BOOT" || fail "Could not add boot hook."
    echo "Restored U1 WLED boot hook."
fi

"$SERVICE_DST" restart
sleep 2

if "$SERVICE_DST" status; then
    echo "Repair complete."
else
    fail "The bridge did not start. Check $BASE/u1_wled.log"
fi
