# Snapmaker U1 WLED Status Bridge v1.0.1

This release improves the beginning-of-print status behavior and makes heating colors easier to distinguish.

## Changes

- A print no longer turns green immediately while the printer is still warming up.
- Initial bed/hotend heating is displayed until commanded heaters are within 2 C of target.
- Once warm-up finishes, the bridge switches to green progress breathing.
- Small normal temperature dips later in a print remain green to avoid distracting color flicker.
- Bed heating is a deeper orange.
- Hotend heating is a redder red-orange.
- Bed + hotend heating uses a stronger orange-red.
- The service supports `status` in addition to `start`, `stop`, and `restart`.

## Tested live sequence

```text
standby -> heating_both -> heating_bed -> printing
IDLE -> BED + HOTEND HEATING -> BED HEATING -> PRINTING
```
