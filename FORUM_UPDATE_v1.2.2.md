# Snapmaker U1 WLED Status Bridge v1.2.2 - Firmware 2.0.0 Tested

I tested the WLED Status Bridge through a real Snapmaker U1 firmware upgrade from **1.6.0 to 2.0.0**.

The good news: the project works on 2.0.0.

During the upgrade, the persistent WLED project directory under `/oem/printer_data/u1_wled/` survived, but Snapmaker replaced the live startup environment under `/etc/init.d`. That removed the two WLED services and the WLED startup hooks from `S99_bootcontrol`, so the lights did not automatically come back after the first 2.0.0 boot.

Running the project's safe installer against the new 2.0.0 configuration restored everything successfully:

```sh
cd /oem/printer_data/u1_wled
./install.sh
```

After recovery:

- WLED status bridge running
- WLED heartbeat running
- Both startup hooks restored
- Normal status lighting working on firmware 2.0.0

The important part is that the installer/repair process patches the **current firmware's** `S99_bootcontrol`. It does not restore an old full boot-control file from an earlier firmware version.

If you update your U1 firmware and the status light stops starting automatically, use:

```sh
cd /oem/printer_data/u1_wled
./repair.sh
```

or rerun `./install.sh`.

Do not manually copy an old `S99_bootcontrol` from a previous firmware version onto 2.0.0.

No WLED firmware reflash is required for this release if you are already using the watchdog firmware from v1.2.0/v1.2.1.

Tested firmware now includes:

- U1 1.6.0
- U1 2.0.0

