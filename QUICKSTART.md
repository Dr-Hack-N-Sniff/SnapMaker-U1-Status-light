# Snapmaker U1 WLED Status Bridge - Quick Start

**Current release: v1.1.0** - normal U1 shutdown/reboot turns the WLED LEDs off, and boot restores the current status.

This is the short copy/paste version. Read `README.md` for the explanation behind each step.

## IMPORTANT: Set Your WLED IP Address

Before installing, you must change the WLED IP address in `u1_wled.py` to the IP address of your own WLED controller.

Open `u1_wled.py` and find:

```python
WLED = "http://YOUR_WLED_IP"
```

Replace `YOUR_WLED_IP` with your WLED controller's IP address.

For example, if your WLED controller is at `192.168.0.50`:

```python
WLED = "http://192.168.0.50"
```

Your WLED controller and Snapmaker U1 must be reachable from the same local network.

## 1. Edit the WLED IP

On your computer, edit `u1_wled.py`:

```python
WLED = "http://YOUR_WLED_IP"
```

Replace the address with your own WLED IP.

## 2. SSH into the U1

From Windows Command Prompt or PowerShell:

```cmd
ssh root@YOUR_U1_IP
```

Example:

```cmd
ssh root@YOUR_U1_IP
```

## 3. Create the Project Directory

On the U1:

```sh
mkdir -p /oem/printer_data/u1_wled
```

## 4. Copy the Project Files

From your Windows computer, open Command Prompt or PowerShell in the folder containing the downloaded project files.

Copy them to the U1:

```cmd
scp u1_wled.py S62u1-wled bootcontrol_patch.py install.sh repair.sh uninstall.sh status.sh root@YOUR_U1_IP:/oem/printer_data/u1_wled/
```

## 5. Set Permissions

Back in the U1 SSH session:

```sh
chmod +x /oem/printer_data/u1_wled/*.sh
chmod +x /oem/printer_data/u1_wled/S62u1-wled
chmod +x /oem/printer_data/u1_wled/u1_wled.py
chmod +x /oem/printer_data/u1_wled/bootcontrol_patch.py
```

## 6. Test WLED Connectivity

Replace the IP with your WLED controller's address:

```sh
wget -qO- http://YOUR_WLED_IP/json/info
```

You should receive WLED JSON information.

## 7. Test Moonraker

```sh
wget -qO- "http://127.0.0.1:7125/printer/objects/query?print_stats"
```

You should receive JSON containing the printer state.

## 8. Install the Bridge

Run:

```sh
/oem/printer_data/u1_wled/install.sh
```

The installer creates the U1 startup service, safely patches the existing Snapmaker boot script, starts the bridge, and verifies that it is running.

## 9. Check Status

```sh
/oem/printer_data/u1_wled/status.sh
```

You can also view the log directly:

```sh
tail -n 50 /oem/printer_data/u1_wled/u1_wled.log
```

## 10. Reboot Test

Reboot the U1:

```sh
reboot
```

Do not manually start the bridge.

During reboot, the LEDs should first turn **off**. After the U1, Wi-Fi, and WLED are available again, the LEDs should automatically return to the current printer status. If idle, that is:

**White breathing**

A short delay is normal while networking becomes available.

## v1.1 Power-Off Note

Normal software shutdown/reboot runs the U1 shutdown scripts and sends WLED an OFF command. Abruptly flipping the physical U1 power switch does not give Linux time to send that command, so a separately powered WLED controller may remain on.

**v1.2 is in development:** the planned heartbeat/failsafe aims to handle physical-switch power loss using software only and no additional hardware.

## Expected Status Colors

| Printer Condition | LED Behavior |
|---|---|
| Standby / Idle | White breathing |
| Heated bed warming | Orange breathing |
| Hotend warming | Red-orange breathing |
| Bed + hotend warming | Faster orange/red breathing |
| Printing 0-24% | Green, slow breathing |
| Printing 25-49% | Green, faster breathing |
| Printing 50-74% | Green, faster breathing |
| Printing 75-89% | Green, fast breathing |
| Printing 90-100% | Green, very fast breathing |
| Paused | Yellow/orange breathing |
| Complete | Solid green for about 30 seconds |
| Cancelled | Solid red |
| Error | Fast red effect |

## After a Snapmaker Firmware Update

If a firmware update removes the custom startup integration, SSH into the U1 and run:

```sh
/oem/printer_data/u1_wled/repair.sh
```

The repair script patches the current firmware's boot script instead of replacing it with an old firmware copy.

Then verify:

```sh
/oem/printer_data/u1_wled/status.sh
```

Reboot once more to verify automatic startup.

## Uninstall

To remove the startup integration:

```sh
/oem/printer_data/u1_wled/uninstall.sh
```

See `README.md` for the full technical explanation and troubleshooting information.
