# Changelog

## v1.0.1

- Show initial bed/hotend warm-up before green printing status.
- Keep heating indication active until commanded heaters are within 2 C of target.
- Prevent normal in-print heater recovery from replacing green progress status.
- Bed heating color changed to RGB `255, 80, 0`.
- Hotend heating color changed to RGB `255, 20, 0`.
- Bed + hotend heating color changed to RGB `255, 50, 0`.
- Public examples use placeholder IP addresses.
- Service launcher includes a `status` command.
