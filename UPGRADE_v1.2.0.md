# Upgrade to v1.2.0

v1.2.0 is the recommended release and adds the power-loss heartbeat failsafe.

## 1. Back up WLED

In WLED, go to **Config -> Security & Updates** and download backups of your configuration and presets.

## 2. Update WLED

Use **Update WLED** on the same page and upload the included `firmware.bin`. Allow WLED to reboot.

## 3. Set your WLED address

Set `YOUR_WLED_IP` in both:

- `u1_wled.py`
- `u1_wled_heartbeat.py`

Both must point to the same WLED controller.

## 4. Copy the v1.2 files to the U1

Copy the release files to:

`/oem/printer_data/u1_wled/`

Then run as root:

```sh
chmod +x /oem/printer_data/u1_wled/*.sh
chmod +x /oem/printer_data/u1_wled/S62u1-wled /oem/printer_data/u1_wled/S63u1-wled-heartbeat
chmod +x /oem/printer_data/u1_wled/*.py
/oem/printer_data/u1_wled/install.sh
```

The installer backs up `S99_bootcontrol`, installs both services, adds both late-boot launchers inside the `start)` branch, and checks both services.

## 5. Reboot and verify

```sh
reboot
```

After boot:

```sh
/etc/init.d/S62u1-wled status
/etc/init.d/S63u1-wled-heartbeat status
```

At idle, the LEDs should return to white breathing and remain on.

## 6. Physical power test

With the U1 idle, use the U1 physical power switch. The separately powered WLED LEDs should turn off after about 10 seconds. Power the U1 back on; after boot, status lighting should return automatically.
