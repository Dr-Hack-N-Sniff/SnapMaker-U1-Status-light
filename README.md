# Snapmaker U1 WLED Status Bridge

> Real-time WLED status lighting driven directly by the Snapmaker U1. No Raspberry Pi, Home Assistant server, cloud service, or always-on PC is required after installation.

**Current recommended release: v1.2.0**

[Quick Start](QUICKSTART.md) | [Upgrade from v1.1.0](UPGRADE_v1.2.0.md) | [Changelog](CHANGELOG.md)

## New here? Start with v1.2.0

v1.2.0 is the recommended version for **new installations and upgrades**. You do **not** need to install v1.1.0 first.

The setup order is intentionally simple:

1. Get WLED working normally first.
2. Back up WLED and install the included v1.2.0 firmware using WLED's normal OTA update page.
3. Install the U1 Status Bridge and heartbeat service.
4. Verify the U1 controls the LED status correctly.
5. Test the physical U1 power switch failsafe.

Already running v1.1.0? Use the [v1.2.0 upgrade guide](UPGRADE_v1.2.0.md).

## Before installing: verify WLED first

Before changing anything on the U1, make sure the WLED controller and LED strip work normally from the WLED web interface.

Verify that you can:

- Reach the WLED controller from your network.
- Turn the LED strip on and off.
- Change colors manually.
- Select an effect such as **Breathe**.
- Confirm the correct LED count is configured.
- Reboot WLED and reconnect to it.

**Do not troubleshoot the U1 bridge until basic WLED operation works.** This gives you a known-good starting point.

## Download the v1.2.0 WLED firmware

For the easiest install, use the prebuilt firmware in this repository:

**[Download Snapmaker_U1_WLED_v1.2.0_ESP32_Watchdog.bin](firmware/Snapmaker_U1_WLED_v1.2.0_ESP32_Watchdog.bin)**

Install it through:

**WLED -> Config -> Security & Updates -> Update WLED**

Back up your WLED configuration and presets first. On the tested OTA-capable ESP32 WLED controller, no USB programmer, PlatformIO, VS Code, Git, Node.js, or local firmware compiling is required for normal installation.

The full v1.2.0 release package also contains the same tested firmware under the simpler filename `firmware.bin`.

> **Important:** The prebuilt binary is the firmware tested on this project's ESP32 WLED controller. If you use materially different WLED hardware, confirm firmware compatibility before updating.

## What v1.2.0 adds

v1.2.0 fixes the main limitation of v1.1.0 when WLED has its own power supply.

The U1 sends a tiny heartbeat every 3 seconds. The included WLED watchdog firmware listens for it without changing the current color or effect. If the heartbeat disappears for about 10 seconds, WLED turns the LEDs off.

That means:

```text
U1 running
    -> heartbeat every 3 seconds
    -> normal printer status lighting

Physical U1 power switch OFF
    -> heartbeat stops
    -> about 10 seconds
    -> WLED LEDs OFF

U1 powered ON
    -> services restart
    -> heartbeat returns
    -> printer status lighting returns
```

The heartbeat is a separate service from the normal status bridge. It does not control printer motion, heaters, Klipper, or the print job.

## Status lighting

| U1 state | WLED behavior |
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

During printing, green breathing speeds up as progress increases:

| Print progress | Breathing speed |
|---|---:|
| 0-24% | 45 |
| 25-49% | 75 |
| 50-74% | 110 |
| 75-89% | 150 |
| 90-100% | 200 |

## How it works

Two lightweight Python processes run directly on the U1:

```text
Snapmaker U1
    |
    +-- u1_wled.py
    |      Moonraker -> printer state -> WLED colors/effects
    |
    +-- u1_wled_heartbeat.py
           heartbeat every 3 seconds
                    |
                    v
              WLED controller
                    |
                    +-- normal status lighting
                    +-- no heartbeat ~10 sec -> LEDs OFF
```

`u1_wled.py` uses the local Moonraker API at `127.0.0.1:7125`. Both U1 scripts use only Python standard-library modules; no `pip install` is required.

## Tested hardware and behavior

The project has been tested on a real Snapmaker U1 with:

- Root SSH access
- Python 3.11
- Moonraker running locally on the U1
- ESP32 WLED controller on the same LAN
- WLED 16.0.1 base firmware
- 20 addressable RGB LEDs in the tested installation
- BIQU PopStation Mini used as the physical mounting location

The PopStation Mini is **not required**. It is simply where the tested controller and strip are installed.

Hardware testing has included:

- Idle indication
- Bed warm-up
- Hotend warm-up across the U1 toolheads
- Combined bed + hotend warm-up
- Warm-up to printing transition
- Progress-dependent green breathing
- Pause, complete, cancel, and error states
- Reboot recovery
- WLED/network startup delays
- Heartbeat every 3 seconds
- Watchdog timeout after about 10 seconds without heartbeat
- Physical U1 power-switch OFF -> LEDs OFF
- U1 power-on -> heartbeat and status recovery

## New v1.2.0 installation

For a fresh installation, follow the complete [QUICKSTART.md](QUICKSTART.md).

You do **not** need v1.1.0 first.

At a high level:

1. Verify normal WLED operation.
2. Back up WLED configuration and presets.
3. OTA-update WLED with the included v1.2.0 watchdog firmware.
4. Set `YOUR_WLED_IP` in both U1 Python files.
5. Copy the v1.2.0 files to `/oem/printer_data/u1_wled/`.
6. Run `install.sh` as root.
7. Verify both services.
8. Reboot and verify white idle lighting.
9. Test the physical U1 power switch.

## Upgrade from v1.1.0

If v1.1.0 is already working, do not install it again. Follow [UPGRADE_v1.2.0.md](UPGRADE_v1.2.0.md).

v1.1.0 remains available as the previous release and rollback point, but v1.2.0 supersedes it for normal new installations.

## Service checks

The normal status bridge is:

```sh
/etc/init.d/S62u1-wled status
```

The v1.2 heartbeat service is:

```sh
/etc/init.d/S63u1-wled-heartbeat status
```

Or use:

```sh
/oem/printer_data/u1_wled/status.sh
```

Both services should report running during normal operation.

## After a Snapmaker firmware update

A Snapmaker firmware update may replace startup files under `/etc/init.d`.

The project files are stored separately under:

```text
/oem/printer_data/u1_wled/
```

If status lighting no longer starts automatically after a Snapmaker firmware update, SSH into the U1 and run:

```sh
/oem/printer_data/u1_wled/repair.sh
```

The repair workflow patches the current firmware's startup file rather than blindly restoring an old complete copy.

## Uninstall

To remove the startup integration:

```sh
/oem/printer_data/u1_wled/uninstall.sh
```

## Repository files

```text
u1_wled.py                 Printer-status bridge
u1_wled_heartbeat.py       v1.2 heartbeat sender
S62u1-wled                 Status-bridge service
S63u1-wled-heartbeat       Heartbeat service
bootcontrol_patch.py       Safe late-boot launcher patch
install.sh                 Installation and startup setup
repair.sh                  Repair after startup integration is replaced
status.sh                  Status helper
uninstall.sh               Removes startup integration
firmware/                   Prebuilt WLED watchdog firmware
QUICKSTART.md              New v1.2.0 installation guide
UPGRADE_v1.2.0.md          v1.1.0 -> v1.2.0 upgrade guide
CHANGELOG.md               Release history
```

## Safety and scope

This is an unofficial community modification, not an official Snapmaker product.

The status bridge is designed to **observe** printer state through Moonraker and control a separate WLED lighting device. The heartbeat service only sends a small UDP heartbeat to WLED. It does not command printer motion or heater operation.

Back up relevant files and WLED settings before modifying firmware or startup configuration. Use at your own risk.

## License / contribution

Issues, testing reports, controller compatibility results, documentation improvements, and pull requests are welcome. Reports from different ESP32/WLED controllers are especially useful for expanding the tested-hardware list.
## Support the Project

If this project saved you some time or you just want to support future Snapmaker and 3D-printing projects:

### ☕ Buy Me a Roll of Filament

[**Buy me a roll of filament**](https://www.buymeacoffee.com/hacknsniff)

Contributions are completely optional. The project will remain free and open source.
