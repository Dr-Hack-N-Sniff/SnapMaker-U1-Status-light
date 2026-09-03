# Snapmaker U1 WLED Status Bridge v1.1.0

v1.1.0 adds power-state-aware WLED handling for normal U1 shutdowns and reboots.

## What changed

The bridge now includes a dedicated WLED-off command. During the U1 BusyBox shutdown sequence, `S62u1-wled stop` stops the bridge process and sends WLED an `on:false` state while network connectivity is still available.

The startup hook was also corrected. The WLED bridge launcher is now installed **inside the `start)` branch of `S99_bootcontrol` only**. This prevents the launcher from being executed during `S99_bootcontrol stop` while still preserving the late-boot start behavior required by the tested U1 firmware.

## Tested behavior

On the development Snapmaker U1, the following were physically verified:

- Service stop: LEDs turn off.
- Service start: current printer status returns.
- Service restart: current printer status returns without using shutdown behavior.
- Reboot: LEDs turn off during shutdown and return after the U1/network/WLED become available.
- Software poweroff: LEDs turn off and remain off.
- Cold startup after poweroff: bridge starts and idle returns to white breathing.

## Important limitation

If the U1 is switched off by **abruptly cutting physical power**, Linux does not get time to run its shutdown sequence. A separately powered WLED controller therefore cannot receive the final `on:false` command and may remain on in its last state.

This is not presented as fixed in v1.1.0.

## v1.2.0 in development

The next planned feature is a software heartbeat/failsafe so stock WLED can automatically go dark after the U1 disappears from the network, including when the physical power switch is used. The goal is to require **no relay, Raspberry Pi, smart plug, or other additional hardware**.

That feature is still under investigation and testing and is not included in v1.1.0.
