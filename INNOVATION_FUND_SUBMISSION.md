# Snapmaker U1 Innovation Fund Submission Draft

## Project name

**Snapmaker U1 WLED Status Bridge**

## Public creator name

**Hack-N-Sniff**

## Project URL

https://github.com/Dr-Hack-N-Sniff/SnapMaker-U1-Status-light

## Short description

Open-source U1 status bridge that runs directly on the printer and turns WLED lighting into real-time heating, printing, pause, completion, and error indicators.

## Project description

I built the Snapmaker U1 WLED Status Bridge to make the printer's operating state visible from across the room without adding another always-on computer. The bridge runs directly on the U1, reads local Moonraker telemetry, and sends status commands to a network-connected WLED controller.

The bridge monitors print state, print progress, the heated bed, and all four U1 hotends. It provides separate lighting states for idle, bed heating, hotend heating, combined heating, printing, paused, complete, cancelled, and error conditions. During printing, the green breathing speed increases with print progress. Version 1.0.1 also keeps the warm-up indication active after a print starts until the commanded heaters reach target, while ignoring small normal temperature recovery later in the print so the status does not flicker.

The project is designed to be self-contained and reproducible. It uses only Python standard-library modules, starts automatically with the U1, retries temporary startup/network failures, and includes installation, status, repair, and uninstall scripts. The firmware-repair workflow patches the current firmware startup configuration instead of blindly restoring an older firmware file.

The complete source code, documentation, Quick Start guide, tests, troubleshooting, and release history are available publicly on GitHub.

## Problem solved

The U1 provides detailed state and temperature information, but that information normally requires looking at the printer interface or another monitoring device. This project turns that existing telemetry into a simple ambient indicator that can be understood from across a room. Because the software runs on the U1 itself, the solution does not require a Raspberry Pi, Home Assistant, cloud service, or PC to remain powered on.

## Technical innovation

- Runs directly on the Snapmaker U1
- Uses local Moonraker telemetry instead of an external monitoring server
- Monitors all four hotends and the heated bed
- Converts print progress into a whole-strip breathing-speed indication
- Separates initial warm-up from normal mid-print temperature recovery
- Handles stale Moonraker completion state
- Retries WLED commands after network startup delays
- Uses Python standard library only
- Includes firmware-update recovery and reversible uninstall tooling

## Testing completed

The project has been physically tested on a Snapmaker U1 for:

- Idle / standby
- Bed heating
- Extruder 0 heating
- Extruder 1 heating
- Extruder 2 heating
- Extruder 3 heating
- Combined bed + hotend heating
- Initial print warm-up
- Printing and progress behavior
- Pause
- Completion and return to idle
- Cancel/error indications
- Cold-boot autostart
- Network/WLED startup delay recovery
- Moonraker startup delay recovery
- Firmware repair script

A real tested warm-up sequence was:

```text
standby -> heating_both -> heating_bed -> printing
```

## Open-source / reproducibility

The repository includes:

- `u1_wled.py`
- `S62u1-wled`
- `install.sh`
- `repair.sh`
- `status.sh`
- `uninstall.sh`
- automated tests
- Quick Start guide
- detailed README
- changelog and release notes

## Media to add before submission

- 640 x 360 cover image
- Hero installation photo
- Heating-state photo
- Printing-state photo
- Hardware close-up
- Demonstration video
