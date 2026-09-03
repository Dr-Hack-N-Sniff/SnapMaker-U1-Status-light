# Changelog

## v1.1.0

- Added a `--off` command to `u1_wled.py` that sends WLED `{"on": false}` while leaving the controller powered.
- Updated `S62u1-wled stop` so BusyBox shutdown/reboot turns the LEDs off before networking is stopped.
- Kept `restart` separate from shutdown behavior so maintenance restarts do not intentionally blank the LEDs.
- Fixed the `S99_bootcontrol` integration so the WLED bridge launcher is placed inside the `start)` branch only.
- Added an idempotent `bootcontrol_patch.py` helper that removes old/unconditional launcher lines before installing the corrected boot-only hook.
- Added updated install, repair, uninstall, and status helpers.
- Physically tested on a Snapmaker U1: manual stop/start, reboot off/on recovery, software poweroff, and cold startup recovery.
- Documented the limitation that abruptly cutting U1 power with the physical switch cannot send a final network command to a separately powered WLED controller.
- Added a v1.2 roadmap item for a software heartbeat/failsafe intended to handle physical-switch power loss without extra hardware.

## v1.0.1

- Show initial bed/hotend warm-up before green printing status.
- Keep heating indication active until commanded heaters are within 2 C of target.
- Prevent normal in-print heater recovery from replacing green progress status.
- Bed heating color changed to RGB `255, 80, 0`.
- Hotend heating color changed to RGB `255, 20, 0`.
- Bed + hotend heating color changed to RGB `255, 50, 0`.
- Public examples use placeholder IP addresses.
- Service launcher includes a `status` command.
