## IMPORTANT: Set Your WLED IP Address

Before installing, you must change the WLED IP address in `u1_wled.py` to the IP address of your own WLED controller.

Open `u1_wled.py` and find:

```python
WLED = "http://192.168.1.63"

# Snapmaker U1 WLED Status Bridge - Quick Start

This is the short copy/paste version. Read `README.md` for the explanation behind each step.

## 1. Edit the WLED IP

On your computer, edit `u1_wled.py`:

```python
WLED = "http://192.168.1.63"
```

Replace the address with your own WLED IP.

## 2. SSH into the U1

Example:

```cmd
ssh root@192.168.1.29
```

## 3. Verify Moonraker

```sh
wget -qO- "http://127.0.0.1:7125/printer/objects/query?print_stats"
```

## 4. Verify WLED

```sh
wget -qO- "http://192.168.1.63/json/info"
```

Replace the WLED IP if different.

## 5. Create the project directory

```sh
mkdir -p /oem/printer_data/u1_wled
```

## 6. From Windows, copy the repository files

Open a second Command Prompt or PowerShell in the repository folder:

```cmd
scp u1_wled.py S62u1-wled install.sh repair.sh uninstall.sh status.sh root@192.168.1.29:/oem/printer_data/u1_wled/
```

Replace the U1 IP if different.

## 7. Back in SSH, install

```sh
chmod +x /oem/printer_data/u1_wled/*.sh
chmod +x /oem/printer_data/u1_wled/S62u1-wled
chmod +x /oem/printer_data/u1_wled/u1_wled.py
/oem/printer_data/u1_wled/install.sh
```

## 8. Verify

```sh
/etc/init.d/S62u1-wled status
```

```sh
tail -n 30 /oem/printer_data/u1_wled/u1_wled.log
```

## 9. Prove autostart works

Set WLED to solid purple from its web UI, then reboot the U1:

```sh
reboot
```

Do not manually start the bridge.

If the U1 is idle, WLED should eventually change itself from purple to white breathing.

## 10. After a future firmware update

```sh
/oem/printer_data/u1_wled/repair.sh
```

Then verify:

```sh
/etc/init.d/S62u1-wled status
```

## Useful commands

Status + recent log:

```sh
/oem/printer_data/u1_wled/status.sh
```

Restart:

```sh
/etc/init.d/S62u1-wled restart
```

Live log:

```sh
tail -f /oem/printer_data/u1_wled/u1_wled.log
```

Uninstall startup integration:

```sh
/oem/printer_data/u1_wled/uninstall.sh
```
