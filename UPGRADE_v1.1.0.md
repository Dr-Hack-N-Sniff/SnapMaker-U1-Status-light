# Upgrade from v1.0.1 to v1.1.0

This upgrade adds WLED OFF handling during normal U1 shutdown/reboot and fixes the late-boot hook so it runs only during `S99_bootcontrol start`.

## Before upgrading

Back up the working bridge on the U1:

```sh
cp /oem/printer_data/u1_wled/u1_wled.py /oem/printer_data/u1_wled/u1_wled_v1.0.1_backup.py
cp /etc/init.d/S62u1-wled /oem/printer_data/u1_wled/S62u1-wled_v1.0.1_backup
cp /etc/init.d/S99_bootcontrol /oem/printer_data/u1_wled/S99_bootcontrol_before_v1.1.0
```

## Preserve your WLED address

The public `u1_wled.py` contains:

```python
WLED = "http://YOUR_WLED_IP"
```

Set that to your WLED controller address before copying the v1.1.0 Python file onto the U1.

## Copy the v1.1.0 files

From your computer:

```cmd
scp u1_wled.py S62u1-wled bootcontrol_patch.py install.sh repair.sh uninstall.sh status.sh root@YOUR_U1_IP:/oem/printer_data/u1_wled/
```

On the U1:

```sh
chmod +x /oem/printer_data/u1_wled/*.sh
chmod +x /oem/printer_data/u1_wled/S62u1-wled
chmod +x /oem/printer_data/u1_wled/u1_wled.py
chmod +x /oem/printer_data/u1_wled/bootcontrol_patch.py
```

Run:

```sh
/oem/printer_data/u1_wled/install.sh
```

The installer backs up the current `S99_bootcontrol`, installs the v1.1 service, removes any older unconditional WLED launcher, and installs exactly one launcher inside the `start)` branch.

## Verify before rebooting

```sh
/etc/init.d/S62u1-wled status
/oem/printer_data/u1_wled/u1_wled.py --off
/etc/init.d/S62u1-wled start
```

Expected behavior:

1. `--off` turns the LEDs dark.
2. Starting the bridge restores the current printer state.
3. If idle, the LEDs return to white breathing.

Then test reboot:

```sh
reboot
```

Expected: LEDs turn off during reboot, then return after the U1 and network finish starting.

## Physical power-switch limitation

Abruptly cutting U1 power with the physical switch bypasses Linux shutdown, so a separately powered WLED controller may remain in its last state. A software heartbeat/failsafe for this case is planned for v1.2.0.
