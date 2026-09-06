# Snapmaker U1 WLED Status Bridge - Quick Start

**Current recommended release: v1.2.1**

v1.2.1 is a maintenance release that improves installation, repair, uninstall, and firmware-update safety.

The WLED status behavior, heartbeat, and watchdog firmware are unchanged from v1.2.0.

## 1. Back up and update WLED

In WLED, open **Config -> Security & Updates** and back up both configuration and presets.

Then choose **Update WLED**, upload the included `firmware.bin`, and allow WLED to reboot.

This is a normal browser-based OTA update on the tested WLED controller. No compiling, PlatformIO, USB programmer, or extra hardware is required.

> Already using the v1.2.0 watchdog firmware? You do not need to re-flash WLED solely to upgrade to v1.2.1.

## 2. Set your WLED IP

Replace `YOUR_WLED_IP` in both:

```text
u1_wled.py
u1_wled_heartbeat.py
```

with your WLED controller address.

## 3. Copy files to the U1

Connect:

```cmd
ssh root@YOUR_U1_IP
```

On the U1:

```sh
mkdir -p /oem/printer_data/u1_wled
```

From the computer containing the release files:

```cmd
scp u1_wled.py u1_wled_heartbeat.py S62u1-wled S63u1-wled-heartbeat bootcontrol_patch.py install.sh repair.sh uninstall.sh status.sh root@YOUR_U1_IP:/oem/printer_data/u1_wled/
```

## 4. Install

On the U1:

```sh
chmod +x /oem/printer_data/u1_wled/*.sh
chmod +x /oem/printer_data/u1_wled/S62u1-wled /oem/printer_data/u1_wled/S63u1-wled-heartbeat
chmod +x /oem/printer_data/u1_wled/*.py
/oem/printer_data/u1_wled/install.sh
```

v1.2.1 validates the current boot configuration before changing live startup files.

The safety sequence is:

**Detect -> Validate -> Back up -> Modify**

If the installer reports that the current firmware boot configuration is incompatible, stop and check the project repository for an update rather than forcing the installation.

Verify:

```sh
/etc/init.d/S62u1-wled status
/etc/init.d/S63u1-wled-heartbeat status
```

Both services should report running.

You can also run:

```sh
/oem/printer_data/u1_wled/status.sh
```

## 5. Reboot test

```sh
reboot
```

Do not manually start the services after reboot.

After the U1 finishes booting, idle should return to **white breathing** automatically.

Verify:

```sh
/etc/init.d/S62u1-wled status
/etc/init.d/S63u1-wled-heartbeat status
```

## 6. Power-off failsafe test

This test assumes WLED remains separately powered when the U1 is switched off.

With the U1 idle and WLED operating normally:

1. Switch the U1 off with its physical power switch.
2. The U1 heartbeat stops.
3. After approximately 10 seconds, the WLED watchdog should turn the LEDs off.
4. Turn the U1 back on.
5. After boot and network recovery, normal status lighting should return automatically.

## Status colors

| Printer condition | LED behavior |
|---|---|
| Idle | White breathing |
| Bed heating | Deep orange breathing |
| Hotend heating | Red-orange breathing |
| Bed + hotend heating | Orange-red breathing |
| Printing | Green breathing; speed increases with progress |
| Paused | Yellow/orange breathing |
| Complete | Solid green for about 30 seconds |
| Cancelled | Solid red |
| Error | Fast red |

## After a Snapmaker firmware update

A Snapmaker firmware update may replace the WLED services or startup hooks.

Run:

```sh
/oem/printer_data/u1_wled/repair.sh
```

v1.2.1 repair:

- Uses the current firmware's `S99_bootcontrol`.
- Validates the WLED service scripts.
- Builds and validates a proposed boot configuration before changing live files.
- Backs up the current boot configuration after validation succeeds.
- Restores both WLED services.
- Preserves unrelated startup hooks.
- Does not restore an old full `S99_bootcontrol`.

If compatibility validation fails, the repair stops instead of blindly modifying an unfamiliar firmware configuration.

After successful repair:

```sh
/etc/init.d/S62u1-wled status
/etc/init.d/S63u1-wled-heartbeat status
```

Then reboot once and verify normal operation.

## Uninstall

```sh
/oem/printer_data/u1_wled/uninstall.sh
```

v1.2.1 uninstall validates the proposed boot configuration before making live changes and removes only the WLED S62/S63 integration.

Unrelated startup hooks are preserved.

## Unofficial Community Project

This project is not affiliated with, endorsed by, or supported by Snapmaker.

It modifies startup configuration on the Snapmaker U1 and is provided as-is. Use it at your own risk.