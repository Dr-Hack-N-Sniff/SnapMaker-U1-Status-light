#!/usr/bin/env python3

import json
import time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ============================================================
# Snapmaker U1 -> Local Moonraker -> WLED Status Bridge
# Runs directly on the Snapmaker U1.
# No third-party Python modules are required.
# ============================================================

MOONRAKER = "http://127.0.0.1:7125"
WLED = "http://YOUR_WLED_IP"   # CHANGE THIS to your WLED IP address.

POLL_INTERVAL = 1.0

BRI_PRINTING = 180
BRI_PAUSED = 160
BRI_COMPLETE = 180
BRI_ERROR = 180
BRI_IDLE = 45
BRI_HEATING = 165

COMPLETE_HOLD_SECONDS = 30
HEAT_TOLERANCE = 2.0


def http_get_json(url, timeout=5):
    req = Request(url, headers={"Accept": "application/json"})
    with urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def http_post_json(url, payload, timeout=2):
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=timeout) as response:
        response.read()


def set_wled(r, g, b, brightness, effect=0, speed=None):
    segment = {"id": 0, "fx": effect, "col": [[r, g, b]]}

    if speed is not None:
        segment["sx"] = speed

    state = {"on": True, "bri": brightness, "seg": [segment]}

    try:
        http_post_json(f"{WLED}/json/state", state, timeout=2)
        return True
    except (URLError, HTTPError, TimeoutError, ValueError, OSError) as e:
        print(f"WLED error: {e}", flush=True)
        return False


def get_print_stats():
    try:
        data = http_get_json(
            f"{MOONRAKER}/printer/objects/query?print_stats",
            timeout=5,
        )
        return data.get("result", {}).get("status", {}).get("print_stats", {})
    except (URLError, HTTPError, TimeoutError, ValueError, TypeError, OSError) as e:
        print(f"Moonraker error: {e}", flush=True)
        return None


def get_progress():
    try:
        data = http_get_json(
            f"{MOONRAKER}/printer/objects/query?virtual_sdcard=progress",
            timeout=5,
        )
        progress = (
            data.get("result", {})
            .get("status", {})
            .get("virtual_sdcard", {})
            .get("progress")
        )

        if progress is None:
            return None

        return max(0.0, min(1.0, float(progress)))
    except (URLError, HTTPError, TimeoutError, ValueError, TypeError, OSError) as e:
        print(f"Progress read error: {e}", flush=True)
        return None


def get_heaters():
    try:
        data = http_get_json(
            f"{MOONRAKER}/printer/objects/query?"
            "heater_bed&extruder&extruder1&extruder2&extruder3",
            timeout=5,
        )
        return data.get("result", {}).get("status", {})
    except (URLError, HTTPError, TimeoutError, ValueError, TypeError, OSError) as e:
        print(f"Heater read error: {e}", flush=True)
        return None


def heater_is_heating(obj):
    if not obj:
        return False

    current = float(obj.get("temperature", 0.0))
    target = float(obj.get("target", 0.0))

    return target > 0 and current < (target - HEAT_TOLERANCE)


def heating_state(heaters):
    if not heaters:
        return None

    bed = heater_is_heating(heaters.get("heater_bed"))
    hotend = any(
        heater_is_heating(heaters.get(name))
        for name in ("extruder", "extruder1", "extruder2", "extruder3")
    )

    if bed and hotend:
        return "heating_both"
    if hotend:
        return "heating_hotend"
    if bed:
        return "heating_bed"

    return None




def choose_desired_state(printer_state, heaters, last_state, warmup_active):
    """Choose the LED state without letting normal print temperature recovery flicker colors.

    Heating overrides the green printing state only during the initial warm-up
    phase of a print. Once the commanded heaters have reached their targets,
    later small temperature dips remain in the green printing indication.
    """
    heat_state = heating_state(heaters)

    if printer_state == "paused":
        return "paused", warmup_active

    if printer_state in ("cancelled", "error"):
        return printer_state, False

    if printer_state == "complete":
        # Moonraker may retain a stale complete state after a reboot/service start.
        if last_state is None:
            return (heat_state if heat_state else "standby"), False
        return "complete", False

    if printer_state == "printing":
        if warmup_active:
            if heat_state:
                return heat_state, True
            return "printing", False

        # A transition from standby/manual heating into printing marks the
        # beginning of a new print warm-up. A resume from PAUSED does not.
        new_print = last_state is None or last_state in (
            "standby",
            "heating_bed",
            "heating_hotend",
            "heating_both",
            "complete",
            "cancelled",
            "error",
        )

        if new_print and heat_state:
            return heat_state, True

        return "printing", False

    return (heat_state if heat_state else "standby"), False


def status_idle():
    print("WLED -> IDLE", flush=True)
    return set_wled(255, 255, 255, BRI_IDLE, effect=2, speed=45)


def status_heating_bed():
    print("WLED -> BED HEATING", flush=True)
    return set_wled(255, 80, 0, BRI_HEATING, effect=2, speed=80)


def status_heating_hotend():
    print("WLED -> HOTEND HEATING", flush=True)
    return set_wled(255, 20, 0, BRI_HEATING, effect=2, speed=110)


def status_heating_both():
    print("WLED -> BED + HOTEND HEATING", flush=True)
    return set_wled(255, 50, 0, BRI_HEATING, effect=2, speed=145)


def printing_bucket(progress):
    if progress is None:
        return -1
    if progress < 0.25:
        return 0
    if progress < 0.50:
        return 1
    if progress < 0.75:
        return 2
    if progress < 0.90:
        return 3
    return 4


def status_printing(progress):
    pct = int(progress * 100) if progress is not None else None

    if progress is None:
        speed = 70
    elif progress < 0.25:
        speed = 45
    elif progress < 0.50:
        speed = 75
    elif progress < 0.75:
        speed = 110
    elif progress < 0.90:
        speed = 150
    else:
        speed = 200

    if pct is None:
        print(
            f"WLED -> PRINTING | progress unknown | breathe speed {speed}",
            flush=True,
        )
    else:
        print(
            f"WLED -> PRINTING | {pct}% | breathe speed {speed}",
            flush=True,
        )

    return set_wled(0, 255, 0, BRI_PRINTING, effect=2, speed=speed)


def status_paused():
    print("WLED -> PAUSED", flush=True)
    return set_wled(255, 180, 0, BRI_PAUSED, effect=2, speed=70)


def status_complete():
    print("WLED -> COMPLETE", flush=True)
    return set_wled(0, 255, 0, BRI_COMPLETE, effect=0)


def status_cancelled():
    print("WLED -> CANCELLED", flush=True)
    return set_wled(255, 0, 0, BRI_ERROR, effect=0)


def status_error():
    print("WLED -> ERROR", flush=True)
    return set_wled(255, 0, 0, BRI_ERROR, effect=1, speed=180)


def apply_state(state, progress=None):
    if state == "printing":
        return status_printing(progress)
    if state == "paused":
        return status_paused()
    if state == "complete":
        return status_complete()
    if state == "cancelled":
        return status_cancelled()
    if state == "error":
        return status_error()
    if state == "heating_bed":
        return status_heating_bed()
    if state == "heating_hotend":
        return status_heating_hotend()
    if state == "heating_both":
        return status_heating_both()

    return status_idle()


def main():
    print("===================================", flush=True)
    print("U1 WLED status bridge started", flush=True)
    print("Moonraker:", MOONRAKER, flush=True)
    print("WLED:     ", WLED, flush=True)
    print("===================================", flush=True)

    last_state = None
    last_progress_bucket = None
    complete_since = None
    complete_finished = False
    wled_state_applied = False
    warmup_active = False

    while True:
        stats = get_print_stats()

        if stats is None:
            print(
                "Moonraker unavailable - keeping current WLED status",
                flush=True,
            )
            time.sleep(POLL_INTERVAL)
            continue

        printer_state = stats.get("state")
        heaters = get_heaters()
        desired_state, warmup_active = choose_desired_state(
            printer_state, heaters, last_state, warmup_active
        )

        if desired_state == "printing":
            progress = get_progress()
            bucket = printing_bucket(progress)
            changed = desired_state != last_state
            bucket_changed = bucket != last_progress_bucket

            if changed:
                print(f"Printer state: {last_state} -> printing", flush=True)

            if changed or bucket_changed or not wled_state_applied:
                wled_state_applied = status_printing(progress)

            last_state = desired_state
            last_progress_bucket = bucket
            complete_since = None
            complete_finished = False

        elif desired_state == "complete":
            if last_state != "complete":
                print(f"Printer state: {last_state} -> complete", flush=True)
                wled_state_applied = status_complete()
                complete_since = time.monotonic()
                complete_finished = False
            elif not wled_state_applied and not complete_finished:
                wled_state_applied = status_complete()

            if (
                not complete_finished
                and complete_since is not None
                and time.monotonic() - complete_since >= COMPLETE_HOLD_SECONDS
            ):
                print("Complete hold finished -> IDLE", flush=True)
                wled_state_applied = status_idle()
                if wled_state_applied:
                    complete_finished = True
            elif complete_finished and not wled_state_applied:
                wled_state_applied = status_idle()

            last_state = "complete"
            last_progress_bucket = None

        else:
            changed = desired_state != last_state

            if changed:
                print(f"Printer state: {last_state} -> {desired_state}", flush=True)

            if changed or not wled_state_applied:
                wled_state_applied = apply_state(desired_state)

            last_state = desired_state
            last_progress_bucket = None
            complete_since = None
            complete_finished = False

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
