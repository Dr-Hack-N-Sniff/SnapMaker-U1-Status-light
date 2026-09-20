# Snapmaker U1 WLED Status Bridge v1.2.2

## Firmware 2.0.0 compatibility validation

v1.2.2 is a maintenance/documentation release based on a real Snapmaker U1 firmware upgrade from **1.6.0 to 2.0.0**.

The WLED lighting behavior, heartbeat protocol, and included WLED watchdog firmware are unchanged from v1.2.1/v1.2.0.

### What was verified

On a real Snapmaker U1, upgrading from firmware 1.6.0 to 2.0.0:

- Preserved the persistent project directory at `/oem/printer_data/u1_wled/`.
- Removed the live WLED init services from `/etc/init.d`.
- Removed the WLED launchers from the firmware's live `/etc/init.d/S99_bootcontrol`.
- Left the printer's Moonraker/Fluidd environment operational.
- Required the WLED integration to be restored after the firmware upgrade.

The existing safe installer was then run against the new 2.0.0 startup configuration:

```sh
cd /oem/printer_data/u1_wled
./install.sh
```

The installer successfully:

- Patched the **current firmware 2.0.0** `S99_bootcontrol` rather than restoring an old copy.
- Restored `/etc/init.d/S62u1-wled`.
- Restored `/etc/init.d/S63u1-wled-heartbeat`.
- Restored both WLED startup launchers.
- Restarted both services successfully.

Verified post-upgrade status:

```text
U1 WLED IS RUNNING
U1 WLED HEARTBEAT IS RUNNING
```

### Important firmware-upgrade note

A Snapmaker firmware update may replace files under `/etc/init.d` even though the persistent project files under `/oem/printer_data/u1_wled/` survive.

After a firmware update, if the WLED status light no longer starts automatically, use the included recovery tooling against the **current** firmware configuration:

```sh
cd /oem/printer_data/u1_wled
./repair.sh
```

or rerun:

```sh
./install.sh
```

Both tools use the current firmware's `S99_bootcontrol`, create and validate a candidate configuration, back up the live file, and only then apply the WLED launchers.

**Do not restore an old complete `S99_bootcontrol` from a previous firmware release.**

### Compatibility

Physically validated on:

- Snapmaker U1 firmware 1.6.0
- Snapmaker U1 firmware 2.0.0
- Python 3.11.x U1 environment
- WLED 0.16.x test installation

### No WLED firmware reflash required

The included WLED watchdog firmware is unchanged. If you are already running the watchdog firmware from v1.2.0 or v1.2.1, you do not need to re-flash the WLED controller solely for this update.

