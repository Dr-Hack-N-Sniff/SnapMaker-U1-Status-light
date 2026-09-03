## Project Update - v1.1.0 Released

I've finished testing v1.1.0 of the **Snapmaker U1 WLED Status Bridge**.

### What's new

The bridge can now turn the WLED LEDs **off during a normal U1 shutdown or reboot**.

With v1.1.0:

- **U1 reboot:** LEDs turn off during shutdown and automatically return to the current printer status after the U1 finishes booting and the network is ready.
- **U1 software shutdown:** LEDs turn off and remain off.
- **U1 startup:** the bridge automatically starts again and restores the current status.
- **Service restart:** the bridge restores the current printer status without treating maintenance as a shutdown.

I physically tested the stop/start, reboot, software shutdown, and cold-start sequences on my U1.

### One remaining limitation

If you simply flip the U1's **physical power switch**, Linux loses power immediately and never gets the opportunity to send the final OFF command to a separately powered WLED controller. In that case, WLED can remain displaying its last state.

That leads directly to the next update.

### v1.2.0 - In Development

For v1.2, I'm working on a **software heartbeat/failsafe** between the U1 and WLED.

The goal is:

**U1 running -> heartbeat present -> status lights operate normally**

**U1 physically switched off -> heartbeat disappears -> WLED automatically turns the LEDs off**

I want this to work with standard WLED and **without requiring users to buy a relay, smart plug, Raspberry Pi, or any other additional hardware**.

The heartbeat feature is still under development and testing, so it is not part of v1.1.0 yet.

GitHub:
https://github.com/Dr-Hack-N-Sniff/SnapMaker-U1-Status-light
