# Changelog


## v1.2.1

- Improved firmware-update and recovery safety for install, repair, and uninstall operations.
- `install.sh` now builds and validates a candidate `S99_bootcontrol` before modifying live startup files.
- `repair.sh` now builds and validates a candidate `S99_bootcontrol` before modifying live startup files.
- `uninstall.sh` now validates the proposed boot configuration before stopping services or changing live files.
- Install and repair now syntax-check `S62u1-wled` and `S63u1-wled-heartbeat` before copying them into `/etc/init.d`.
- Current `S99_bootcontrol` is backed up before live changes.
- Existing unrelated startup hooks are preserved instead of restoring an older full boot configuration.
- Added regression coverage to ensure the separate `S64u1-camera` startup hook is preserved.
- Uninstall removes only the WLED S62/S63 integration and does not restore an old `S99_bootcontrol`.
- Expanded the automated test suite to 16 tests.
- Final install and repair scripts were physically validated on a Snapmaker U1 alongside the separate Fluidd camera bridge.

## v1.2.0

- Added custom WLED heartbeat watchdog firmware (`firmware.bin`).
- U1 sends a 6-byte heartbeat every 3 seconds over UDP.
- WLED turns the LEDs off after approximately 10 seconds without a heartbeat.
- Added separate `S63u1-wled-heartbeat` service.
- Updated `S99_bootcontrol` integration to late-start both S62 and S63.
- Physical U1 power-switch shutdown now results in separately powered WLED LEDs turning off automatically.
- Power-on/reboot restores heartbeat and normal printer status automatically.
- OTA firmware update uses the normal WLED web updater; users do not need to compile firmware.
- Physically validated heartbeat, timeout, reboot recovery, and physical power-off/on recovery on the development U1.

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
