# Project Summary - Snapmaker U1 WLED Status Bridge

## Public project name

**Snapmaker U1 WLED Status Bridge**

## Author / public handle

**Dr-Hack-N-Sniff**

## Repository

https://github.com/Dr-Hack-N-Sniff/SnapMaker-U1-Status-light

## Short description

Open-source U1 status bridge that runs directly on the printer and turns WLED lighting into real-time heating, printing, pause, completion, and error indicators.

## One-paragraph description

The Snapmaker U1 WLED Status Bridge is an open-source modification that runs directly on the Snapmaker U1 and converts the printer's local Moonraker telemetry into visible WLED status lighting. It monitors the heated bed, all four hotends, printer state, and print progress without requiring a Raspberry Pi, Home Assistant server, cloud service, or always-on PC. The bridge provides distinct idle, warm-up, printing, pause, completion, cancellation, and error indications; starts automatically with the U1; retries when network services are not ready; and includes installation, repair, uninstall, status, and testing tools for reproducible deployment.

## Technical highlights

- Runs directly on the Snapmaker U1
- Uses local Moonraker API data
- No third-party Python modules required
- Reads heated bed and all four extruders
- Warm-up lighting remains active until commanded heaters reach target
- Progress represented by increasing green breathing speed
- Avoids normal mid-print heater recovery flicker
- Retries temporary WLED/network failures
- Handles Moonraker startup delays
- Automatic boot integration
- Firmware-repair workflow
- Reversible uninstall workflow
- Public source, documentation, tests, and troubleshooting

## Validated behavior

- Idle: white breathing
- Bed heating: deep orange breathing
- Hotend heating: red-orange breathing
- Bed + hotend heating: faster orange-red breathing
- Printing: green breathing, progressively faster by print percentage
- Paused: yellow/orange breathing
- Complete: solid green for about 30 seconds, then idle
- Cancelled: solid red
- Error: fast red effect

## Hardware tested

- Snapmaker U1
- BIQU PopStation Mini installation
- WLED-compatible controller
- Approximately 3 ft addressable RGB LED strip
- 20 LEDs configured in WLED
- WLED 0.16.x

## What makes it different

The bridge is not just an external dashboard. It runs on the U1 itself and uses the printer's existing local telemetry. Once installed, the U1 independently controls the status lighting. The design deliberately avoids adding Python packages to Snapmaker's software environment and includes recovery tooling for firmware-update scenarios.

## Media still to add

- Hero installation photo
- Idle photo
- Heating photo
- Printing photo
- Hardware close-up
- Short demonstration video
