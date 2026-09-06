\# Upgrading to Snapmaker U1 WLED Status Bridge v1.2.1



v1.2.1 is a maintenance release focused on safer installation, repair, uninstall, and firmware-update recovery.



The WLED status behavior, heartbeat protocol, and watchdog firmware are unchanged from v1.2.0.



\## If You Are Already Running v1.2.0



You do \*\*not\*\* need to re-flash WLED.



The included `firmware.bin` and watchdog behavior are unchanged from v1.2.0.



The v1.2.1 changes are primarily on the Snapmaker U1 side.



\## What v1.2.1 Improves



v1.2.1 changes the recovery process to:



\*\*Detect -> Validate -> Back up -> Modify\*\*



Before modifying live startup files, the install and repair tools:



1\. Verify the required files.

2\. Validate the WLED init service scripts.

3\. Copy the current firmware's `S99\_bootcontrol` to a temporary candidate.

4\. Apply the WLED startup hooks to that candidate.

5\. Validate the candidate.

6\. Stop without changing live WLED service or boot files if validation fails.

7\. Back up the current boot configuration after validation succeeds.

8\. Install the validated changes.



The uninstaller uses the same principle before removing the WLED integration.



\## Upgrade from v1.2.0



On your computer, configure your WLED address in:



```text

u1\_wled.py

u1\_wled\_heartbeat.py

```



Replace:



```text

YOUR\_WLED\_IP

```



with your WLED controller address.



Create the persistent directory if it does not already exist:



```sh

mkdir -p /oem/printer\_data/u1\_wled

```



From the computer containing the v1.2.1 release files:



```cmd

scp u1\_wled.py u1\_wled\_heartbeat.py S62u1-wled S63u1-wled-heartbeat bootcontrol\_patch.py install.sh repair.sh uninstall.sh status.sh root@YOUR\_U1\_IP:/oem/printer\_data/u1\_wled/

```



On the U1:



```sh

chmod +x /oem/printer\_data/u1\_wled/\*.sh

chmod +x /oem/printer\_data/u1\_wled/S62u1-wled

chmod +x /oem/printer\_data/u1\_wled/S63u1-wled-heartbeat

chmod +x /oem/printer\_data/u1\_wled/\*.py

```



Then run:



```sh

/oem/printer\_data/u1\_wled/install.sh

```



The installer is idempotent and can update an existing installation.



\## Verify



Check both services:



```sh

/etc/init.d/S62u1-wled status

/etc/init.d/S63u1-wled-heartbeat status

```



Both should report running.



Then reboot:



```sh

reboot

```



After startup, verify both services again.



Normal idle status should return to white breathing automatically.



\## Firmware Updates



If a future Snapmaker firmware update removes the WLED services or startup hooks, run:



```sh

/oem/printer\_data/u1\_wled/repair.sh

```



The repair tool uses the \*\*current firmware's\*\* `S99\_bootcontrol`.



It does not restore an old full copy from a previous firmware version.



If the current firmware no longer matches the expected safe patch structure, repair stops instead of forcing the modification.



If that happens, stop and check the project repository for an updated release.



\## Other Startup Modifications



v1.2.1 removes and adds only the WLED-specific S62/S63 startup hooks.



Unrelated startup entries are preserved.



Regression testing specifically verifies preservation of an independent:



```sh

/etc/init.d/S64u1-camera start

```



hook used by the separate Snapmaker U1 Fluidd camera project.



The camera project is not required to use the WLED Status Bridge.



\## Uninstall



To remove the WLED startup integration:



```sh

/oem/printer\_data/u1\_wled/uninstall.sh

```



The v1.2.1 uninstaller:



\- Validates a candidate boot configuration first.

\- Backs up the current configuration.

\- Stops both WLED services.

\- Removes only the WLED S62/S63 startup hooks.

\- Removes the live S62/S63 init services.

\- Preserves unrelated startup hooks.

\- Does not restore an old full `S99\_bootcontrol`.

\- Leaves the persistent project directory intact.



\## Testing



v1.2.1 passed the complete 16-test automated test suite.



The final install and repair scripts were also physically tested on a Snapmaker U1.



Testing verified that the WLED status bridge, heartbeat service, and separate Fluidd camera bridge continued to operate together.



\## Unofficial Community Project



This project is not affiliated with, endorsed by, or supported by Snapmaker.



It modifies startup configuration on the Snapmaker U1 and is provided as-is. Use it at your own risk.
