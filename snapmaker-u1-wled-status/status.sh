#!/bin/sh

BASE="/oem/printer_data/u1_wled"
SERVICE="/etc/init.d/S62u1-wled"

if [ -x "$SERVICE" ]; then
    "$SERVICE" status
else
    echo "U1 WLED service launcher is not installed."
fi

echo ""
echo "Recent log entries:"
if [ -f "$BASE/u1_wled.log" ]; then
    tail -n 25 "$BASE/u1_wled.log"
else
    echo "No log exists yet."
fi
