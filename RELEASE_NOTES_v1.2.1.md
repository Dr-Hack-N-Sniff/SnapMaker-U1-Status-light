\# Snapmaker U1 WLED Status Light v1.2.1



v1.2.1 is a maintenance release focused on safer installation, repair, uninstall, and firmware-update recovery.



The WLED status-light behavior and watchdog firmware are unchanged from v1.2.0.



\## What Changed



The installation and recovery tools now follow:



\*\*Detect -> Validate -> Back up -> Modify\*\*



Before changing the live Snapmaker startup configuration, the scripts build and validate a proposed `S99\_bootcontrol`.



If a future Snapmaker firmware changes the expected boot configuration, the operation stops instead of blindly overwriting the live configuration.



\## Safety Improvements



\- `install.sh` validates the proposed boot configuration before modifying live service or boot files.

\- `repair.sh` validates the proposed boot configuration before modifying live service or boot files.

\- `uninstall.sh` validates the proposed configuration before stopping services or removing WLED integration.

\- Install and repair syntax-check `S62u1-wled` and `S63u1-wled-heartbeat` before installation.

\- The current `S99\_bootcontrol` is backed up before modification.

\- Existing unrelated startup entries are preserved.

\- The separate `S64u1-camera` startup hook is explicitly covered by regression tests.

\- Uninstall removes only the WLED S62/S63 integration.

\- Uninstall does not restore an old full `S99\_bootcontrol`.



\## Testing



v1.2.1 passed the complete 16-test automated test suite.



The final install and repair scripts were also physically tested on a Snapmaker U1.



Live testing verified:



\- WLED bridge operation

\- Heartbeat service operation

\- Reboot recovery

\- Heating/status-light changes

\- Preservation of the separate Fluidd camera bridge

\- Preservation of all three S64/S62/S63 startup hooks



\## Upgrading from v1.2.0



The WLED watchdog firmware (`firmware.bin`) is unchanged from v1.2.0.



Users already running the v1.2.0 watchdog firmware do not need to re-flash WLED solely to upgrade to v1.2.1.



The primary changes in v1.2.1 are the Snapmaker-side installation and recovery scripts.



\## Unofficial Community Project



This project is not affiliated with, endorsed by, or supported by Snapmaker.



It modifies startup configuration on the Snapmaker U1 and is provided as-is. Use it at your own risk. Modifications to your printer may affect support or warranty coverage.
