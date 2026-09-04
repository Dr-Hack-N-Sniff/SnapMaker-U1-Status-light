#!/bin/sh
SERVICE="/etc/init.d/S62u1-wled"
HEARTBEAT_SERVICE="/etc/init.d/S63u1-wled-heartbeat"
LOG="/oem/printer_data/u1_wled/u1_wled.log"

if [ -x "$SERVICE" ]; then
    "$SERVICE" status
else
    echo "U1 WLED service is not installed."
fi

if [ -x "$HEARTBEAT_SERVICE" ]; then
    "$HEARTBEAT_SERVICE" status
else
    echo "U1 WLED heartbeat service is not installed."
fi

echo
if [ -f "$LOG" ]; then
    echo "Recent log:"
    tail -n 30 "$LOG"
else
    echo "No log file found at $LOG"
fi
