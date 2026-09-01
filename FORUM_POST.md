# Snapmaker U1 WLED Status Bridge - Real-Time Printer Status Without a Raspberry Pi

I wanted an easy way to see what my Snapmaker U1 was doing from across the room, so I built an open-source WLED status bridge that runs directly on the U1.

No Raspberry Pi, Home Assistant server, external PC, or cloud service is required once installed.

The bridge reads the U1's local Moonraker data and translates printer state into WLED lighting:

- White breathing - Idle
- Orange - Bed heating
- Red-orange - Hotend heating
- Orange-red - Bed + hotend heating
- Green breathing - Printing
- Yellow/orange - Paused
- Solid green - Print complete
- Solid red - Cancelled
- Fast red - Error

During printing, the green breathing rate increases as the print progresses, giving a rough visual indication of progress from across the room.

Version 1.0.1 also tracks the initial warm-up sequence. The LEDs show the appropriate heating state while the U1 is warming up and only switch to green once the commanded heaters reach their targets. Normal temperature fluctuations later in the print do not cause the LEDs to jump back into heating mode.

## How it works

```text
Snapmaker U1 -> Local Moonraker API -> Python bridge -> WLED JSON API -> LED strip
```

The Python bridge runs directly on the U1 and starts automatically with the printer. It is designed to preserve/retry the desired lighting state through temporary Moonraker, Wi-Fi, or WLED startup delays.

I developed and tested the project on an actual Snapmaker U1 with a WLED-controlled LED strip installed beneath a BIQU PopStation Mini. The heated bed and all four toolheads were tested.

The project includes the Python bridge, installation script, startup service, repair script, uninstall script, documentation, tests, and troubleshooting.

## GitHub

https://github.com/Dr-Hack-N-Sniff/SnapMaker-U1-Status-light

Current release: **v1.0.1**

Everything needed to reproduce the project is available there.

**Important:** This project requires root SSH access to the U1 and modifies the printer's startup environment. Back up your configuration and understand the changes before installing.

This is an unofficial community modification and is not affiliated with or endorsed by Snapmaker or WLED.
