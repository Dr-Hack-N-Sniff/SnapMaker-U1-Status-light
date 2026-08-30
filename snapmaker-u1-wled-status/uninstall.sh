#!/bin/sh

set -u

BASE="/oem/printer_data/u1_wled"
SERVICE="/etc/init.d/S62u1-wled"
BOOT="/etc/init.d/S99_bootcontrol"
HOOK="/etc/init.d/S62u1-wled start"

fail() {
    echo "ERROR: $1" >&2
    exit 1
}

[ "$(id -u)" = "0" ] || fail "Run this uninstaller as root."

if [ -x "$SERVICE" ]; then
    "$SERVICE" stop || true
fi

if [ -f "$BOOT" ] && grep -Fq "$HOOK" "$BOOT"; then
    cp "$BOOT" "$BASE/backups/S99_bootcontrol.pre-uninstall" 2>/dev/null || true
    sed -i '\|^/etc/init.d/S62u1-wled start$|d' "$BOOT"
    echo "Removed U1 WLED boot hook."
fi

rm -f "$SERVICE"
rm -f /var/run/u1_wled.pid

echo "Service removed."
echo "Project files were left in $BASE so logs/backups are not destroyed."
echo "Delete that directory manually only if you no longer want the project files."
