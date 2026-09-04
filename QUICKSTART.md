# Snapmaker U1 WLED Status Bridge - Quick Start

**Current recommended release: v1.2.0**

v1.2 adds the power-off failsafe: if the U1 disappears, WLED turns the LEDs off after about 10 seconds.

## 1. Back up and update WLED

In WLED, open **Config -> Security & Updates** and back up both configuration and presets. Then choose **Update WLED**, upload the included `firmware.bin`, and allow WLED to reboot.

This is a normal browser-based OTA update on the tested WLED controller. No compiling, PlatformIO, USB programmer, or extra hardware is required.

## 2. Set your WLED IP

Replace `YOUR_WLED_IP` in both `u1_wled.py` and `u1_wled_heartbeat.py` with your WLED controller address.

## 3. Copy files to the U1

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

Verify:

```sh
/oem/printer_data/u1_wled/status.sh
```

Both the status bridge and heartbeat service should report running.

## 5. Reboot test

```sh
reboot
```

After boot, idle should return to **white breathing** and both services should be running.

## 6. Power-off failsafe test

With the U1 idle and WLED separately powered, switch the U1 off physically. After about 10 seconds the LEDs should go dark. Power the U1 back on; after boot the status lighting should return automatically.

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

If the startup hook is removed, run:

```sh
/oem/printer_data/u1_wled/repair.sh
```

## Uninstall

```sh
/oem/printer_data/u1_wled/uninstall.sh
```
