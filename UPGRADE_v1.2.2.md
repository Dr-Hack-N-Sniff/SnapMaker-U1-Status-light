# Upgrade to v1.2.2

v1.2.2 documents and validates recovery after a Snapmaker U1 firmware upgrade to **2.0.0**.

The lighting logic and WLED watchdog firmware are unchanged.

## If WLED is currently working

No immediate reinstall is required solely because of v1.2.2.

Update your project files when convenient and keep `repair.sh` and `install.sh` available for future Snapmaker firmware updates.

## After a Snapmaker firmware update

A firmware update may preserve:

```text
/oem/printer_data/u1_wled/
```

while replacing live startup files under:

```text
/etc/init.d/
```

On the tested upgrade from U1 firmware 1.6.0 to 2.0.0, the persistent WLED project files survived, but the live WLED services and WLED `S99_bootcontrol` launchers were removed.

### Check the services

```sh
/etc/init.d/S62u1-wled status
/etc/init.d/S63u1-wled-heartbeat status
```

If those files are missing or the services are not running, use the project recovery tooling.

### Preferred recovery

```sh
cd /oem/printer_data/u1_wled
./repair.sh
```

The repair process:

1. Uses the current firmware's `/etc/init.d/S99_bootcontrol`.
2. Validates the WLED service scripts.
3. Creates a temporary candidate boot configuration.
4. Applies only the WLED startup hooks to the candidate.
5. Syntax-checks the candidate.
6. Stops without touching live startup files if validation fails.
7. Backs up the current live `S99_bootcontrol`.
8. Restores the WLED services.
9. Installs the validated candidate.
10. Restarts and verifies both WLED services.

You can also rerun the installer:

```sh
cd /oem/printer_data/u1_wled
./install.sh
```

This was physically tested successfully after upgrading a U1 from firmware 1.6.0 to 2.0.0.

## Verify recovery

```sh
/etc/init.d/S62u1-wled status
/etc/init.d/S63u1-wled-heartbeat status

grep -nE 'S62u1-wled|S63u1-wled-heartbeat' /etc/init.d/S99_bootcontrol
```

Expected service status:

```text
U1 WLED IS RUNNING
U1 WLED HEARTBEAT IS RUNNING
```

Expected launchers:

```text
/etc/init.d/S62u1-wled start
/etc/init.d/S63u1-wled-heartbeat start
```

## Important

Do **not** copy an old full `S99_bootcontrol` from firmware 1.x onto firmware 2.0.0.

Firmware revisions may legitimately change Snapmaker startup logic. The project intentionally patches the current firmware configuration instead of replacing it with an old known-good file.

## WLED firmware

No WLED firmware reflash is required when upgrading from v1.2.0 or v1.2.1 to v1.2.2.

