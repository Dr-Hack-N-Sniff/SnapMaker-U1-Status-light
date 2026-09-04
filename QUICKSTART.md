# Snapmaker U1 WLED Status Bridge - Quick Start

**Recommended release: v1.2.0**

v1.2.0 is for both **new installations** and **v1.1.0 upgrades**. A new user does **not** need to install v1.1.0 first.

The troubleshooting order is:

**WLED first -> U1 Status Bridge second -> v1.2 heartbeat/watchdog third**

This makes it much easier to know which part needs attention if something does not work.

---

## Before you begin: make WLED work first

Before installing anything on the Snapmaker U1, power on your WLED controller and LED strip and verify normal WLED operation from its web interface.

Confirm that:

- You can reach the WLED web interface from your network.
- The LED strip turns on.
- You can manually change the LED color.
- You can select an effect such as **Breathe**.
- The correct number of LEDs is configured.
- WLED remains reachable after a normal reboot.

**Do not continue until basic WLED operation works.**

The U1 Status Bridge assumes you already have a functioning WLED controller and LED strip.

For reliability, a DHCP reservation or static IP for WLED is recommended so its address does not unexpectedly change.

---

# Choose your path

## New installation

If you have never installed the U1 WLED Status Bridge, follow **Path A**.

You do **not** need v1.1.0 first.

## Already running v1.1.0

If v1.1.0 is already installed and working, use **Path B** or the more detailed [UPGRADE_v1.2.0.md](UPGRADE_v1.2.0.md).

---

# Path A - New v1.2.0 installation

## A1. Back up WLED

In WLED, open:

**Config -> Security & Updates**

Download backups of:

- WLED configuration
- WLED presets

Keep those backups somewhere safe before updating firmware.

## A2. Install the v1.2.0 WLED firmware

Download the tested prebuilt firmware:

**[Download Snapmaker_U1_WLED_v1.2.0_ESP32_Watchdog.bin](firmware/Snapmaker_U1_WLED_v1.2.0_ESP32_Watchdog.bin)**

The full v1.2.0 release ZIP contains the same firmware as `firmware.bin`.

In WLED, go to:

**Config -> Security & Updates -> Update WLED**

Select the `.bin` file, upload it, and allow WLED to reboot.

On the tested OTA-capable ESP32 WLED controller, this is a normal browser-based update. No PlatformIO, VS Code, Git, Node.js, USB programmer, or local compiling is required for normal installation.

> The prebuilt binary is the firmware tested on this project's ESP32 WLED controller. If you use materially different WLED hardware, confirm firmware compatibility before updating.

After WLED reboots, reconnect to its web interface. Your saved startup preset may appear until the U1 Status Bridge sends a printer state. That is normal.

## A3. Find the U1 and WLED IP addresses

You need:

```text
U1:   YOUR_U1_IP
WLED: YOUR_WLED_IP
```

Test U1 SSH from Windows PowerShell or Command Prompt:

```cmd
ssh root@YOUR_U1_IP
```

## A4. Verify Moonraker on the U1

After SSHing into the U1, run:

```sh
wget -qO- "http://127.0.0.1:7125/printer/objects/query?print_stats"
```

You should receive JSON containing `print_stats`.

Check Python:

```sh
python3 --version
```

No `pip install` is required. The bridge and heartbeat sender use Python standard-library modules.

## A5. Verify the U1 can reach WLED

Still in SSH, run:

```sh
wget -qO- "http://YOUR_WLED_IP/json/info"
```

Replace `YOUR_WLED_IP` with your WLED address.

If WLED does not return JSON, fix network connectivity before continuing.

## A6. Set the WLED IP in both Python files

On your computer, edit:

```text
u1_wled.py
u1_wled_heartbeat.py
```

In `u1_wled.py`, change:

```python
WLED = "http://YOUR_WLED_IP"
```

In `u1_wled_heartbeat.py`, change:

```python
WLED_IP = "YOUR_WLED_IP"
```

Both must point to the same WLED controller.

Do not change the local Moonraker address unless your U1 is configured differently.

## A7. Create the project directory

On the U1:

```sh
mkdir -p /oem/printer_data/u1_wled
```

## A8. Copy the v1.2.0 files to the U1

From the computer containing the release files:

```cmd
scp u1_wled.py u1_wled_heartbeat.py S62u1-wled S63u1-wled-heartbeat bootcontrol_patch.py install.sh repair.sh uninstall.sh status.sh root@YOUR_U1_IP:/oem/printer_data/u1_wled/
```

## A9. Install

Back in the U1 SSH session:

```sh
chmod +x /oem/printer_data/u1_wled/*.sh
chmod +x /oem/printer_data/u1_wled/S62u1-wled /oem/printer_data/u1_wled/S63u1-wled-heartbeat
chmod +x /oem/printer_data/u1_wled/*.py
/oem/printer_data/u1_wled/install.sh
```

The installer installs both services and adds their late-boot launchers to the current U1 startup configuration.

Verify:

```sh
/oem/printer_data/u1_wled/status.sh
```

You can also check them individually:

```sh
/etc/init.d/S62u1-wled status
/etc/init.d/S63u1-wled-heartbeat status
```

Both should report running.

## A10. Verify normal U1 status lighting

Before testing the power-off watchdog, verify the normal bridge works.

At idle, the strip should show **white breathing**.

As you use the printer, the U1 bridge should control the status lighting rather than the WLED startup preset.

Expected states include:

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

If the U1 is not controlling the LEDs correctly, fix the normal status bridge before testing the watchdog.

## A11. Reboot test

Run:

```sh
reboot
```

After the U1 boots:

- Both services should start automatically.
- Idle should return to white breathing.
- The lights should remain on while the heartbeat service is running.

If needed, verify again:

```sh
/etc/init.d/S62u1-wled status
/etc/init.d/S63u1-wled-heartbeat status
```

## A12. Physical power-off failsafe test

This is the v1.2.0 feature.

With the U1 idle and WLED separately powered:

1. Confirm the LEDs are showing normal idle status.
2. Turn the U1 off using its physical power switch.
3. Leave WLED powered.
4. Wait about 10 seconds.

The LEDs should turn off automatically because the heartbeat has stopped.

Power the U1 back on normally. After boot, the two U1 services should restart and normal status lighting should return automatically.

**New v1.2.0 installation complete.**

---

# Path B - Upgrade from v1.1.0

If v1.1.0 is already installed, first make sure it is working normally.

At idle, verify white breathing and check:

```sh
/etc/init.d/S62u1-wled status
```

If the existing bridge is not working, repair that before adding the v1.2.0 watchdog.

Then:

1. Back up WLED configuration and presets.
2. Install the v1.2.0 WLED firmware using **Config -> Security & Updates -> Update WLED**.
3. Set `YOUR_WLED_IP` in both `u1_wled.py` and `u1_wled_heartbeat.py` from the v1.2.0 release.
4. Copy the v1.2.0 release files to `/oem/printer_data/u1_wled/`.
5. Run the v1.2.0 `install.sh` as root.
6. Verify both `S62u1-wled` and `S63u1-wled-heartbeat` report running.
7. Reboot and confirm idle returns to white breathing.
8. Perform the physical power-off test and confirm the LEDs turn off after about 10 seconds.
9. Power the U1 back on and confirm status lighting returns.

For the detailed upgrade procedure, see [UPGRADE_v1.2.0.md](UPGRADE_v1.2.0.md).

---

# After a Snapmaker firmware update

A Snapmaker firmware update may replace the U1 startup integration.

If the project files still exist under `/oem/printer_data/u1_wled/` but the lighting no longer starts automatically, run:

```sh
/oem/printer_data/u1_wled/repair.sh
```

Then verify both services and reboot.

---

# Uninstall

```sh
/oem/printer_data/u1_wled/uninstall.sh
```

---

# Troubleshooting order

If something does not work, check in this order:

1. **WLED itself:** Can you reach WLED and manually control the LEDs?
2. **Network:** Can the U1 reach `http://YOUR_WLED_IP/json/info`?
3. **Status bridge:** Does `/etc/init.d/S62u1-wled status` report running, and does idle become white breathing?
4. **Heartbeat:** Does `/etc/init.d/S63u1-wled-heartbeat status` report running?
5. **Watchdog:** With the heartbeat stopped or the U1 physically powered off, do the LEDs turn off after about 10 seconds?

Keeping these layers separate makes troubleshooting much easier.
