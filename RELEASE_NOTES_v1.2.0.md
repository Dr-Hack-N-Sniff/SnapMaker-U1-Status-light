# Snapmaker U1 WLED Status Bridge v1.2.0

**v1.2.0 is the current recommended release.**

This release solves the remaining v1.1 limitation: a separately powered WLED strip can now turn itself off after the Snapmaker U1 loses power, including an abrupt physical power-switch shutdown.

## What's new

- Adds a lightweight heartbeat from the U1 every 3 seconds.
- Adds a WLED-side watchdog with an approximately 10-second timeout.
- If the heartbeat disappears, the LEDs turn off while the WLED controller remains powered.
- When the U1 boots again, the heartbeat resumes and the normal status bridge restores the current printer indication.
- Adds the separate `S63u1-wled-heartbeat` service so heartbeat handling remains isolated from the printer-status bridge.
- Updates the late-boot integration so both `S62u1-wled` and `S63u1-wled-heartbeat` start reliably.

## WLED firmware update

v1.2 includes the tested `firmware.bin`. Users do not need to compile WLED or install PlatformIO.

Back up WLED configuration and presets, then use the normal WLED web updater:

1. Open WLED.
2. Go to **Config -> Security & Updates -> Update WLED**.
3. Select the included `firmware.bin`.
4. Upload it and allow WLED to reboot.

No USB connection or ESP32 programming tools are required for the tested OTA-capable controller.

## Hardware validation

The v1.2 behavior was tested on the actual Snapmaker U1/WLED installation:

- Continuous heartbeat keeps the status lighting active.
- Stopping heartbeat turns the LEDs off after about 10 seconds.
- Reboot starts both U1 services and restores white idle status.
- Physical U1 power switch OFF causes WLED LEDs to turn off after the watchdog timeout.
- Powering the U1 back on restores the status lighting automatically.

## Upgrade note

v1.1.0 remains available as the previous release and rollback point, but v1.2.0 supersedes it for new installations.
