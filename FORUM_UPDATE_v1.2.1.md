# Snapmaker U1 WLED Status Bridge v1.2.1

v1.2.1 is now available.

This is primarily a maintenance and recovery-safety release. The WLED status behavior, heartbeat, and watchdog firmware are unchanged from v1.2.0.

## What's improved

The install, repair, and uninstall tools have been updated to use a safer recovery process:

**Detect -> Validate -> Back up -> Modify**

Before changing the live U1 startup configuration, v1.2.1 builds and validates a proposed `S99_bootcontrol`.

If a future Snapmaker firmware changes the expected startup layout, the tools stop instead of blindly forcing an older configuration.

Other improvements include:

- Validation of WLED service scripts before installation
- Backup of the current boot configuration before modification
- Preservation of unrelated startup hooks
- Targeted removal of only the WLED S62/S63 hooks during uninstall
- No restoration of an old full `S99_bootcontrol`
- Regression testing for coexistence with other startup modifications
- 16 automated tests

The final install and repair scripts were also physically tested on my Snapmaker U1.

I tested the WLED status bridge and heartbeat alongside my separate Fluidd stock-camera bridge, including a full reboot and heater/status-light test.

## Already using v1.2.0?

You do not need to re-flash the WLED controller solely for this update.

The watchdog firmware is unchanged from v1.2.0. The v1.2.1 changes are primarily the Snapmaker-side installation and recovery tools.

## Firmware updates

If a future Snapmaker firmware update removes the WLED startup integration, use the included:

```sh
/oem/printer_data/u1_wled/repair.sh
```

If the new firmware no longer matches the expected safe patch structure, repair will stop rather than overwrite an unfamiliar configuration.

## Unofficial Community Project

This project is not affiliated with, endorsed by, or supported by Snapmaker.

It modifies startup configuration on the Snapmaker U1 and is provided as-is. Use it at your own risk.