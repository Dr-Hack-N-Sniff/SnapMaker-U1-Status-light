#!/usr/bin/env python3

import socket
import sys
import time

WLED_IP = "YOUR_WLED_IP"
WLED_PORT = 21324
HEARTBEAT_INTERVAL = 3.0
HEARTBEAT_PACKET = bytes([0xA5, 0x55, 0x31, 0x48, 0x42, 0x01])


def send_once(sock, host=WLED_IP, port=WLED_PORT):
    return sock.sendto(HEARTBEAT_PACKET, (host, port))


def heartbeat_loop(
    sock,
    host=WLED_IP,
    port=WLED_PORT,
    interval=HEARTBEAT_INTERVAL,
    sleep_fn=time.sleep,
    iterations=None,
):
    count = 0
    while iterations is None or count < iterations:
        try:
            send_once(sock, host, port)
        except OSError as exc:
            print(f"WLED heartbeat send error: {exc}", file=sys.stderr, flush=True)
        sleep_fn(interval)
        count += 1


def main():
    print("U1 WLED heartbeat sender started", flush=True)
    print(f"Target: {WLED_IP}:{WLED_PORT}", flush=True)
    print(f"Interval: {HEARTBEAT_INTERVAL:.0f} seconds", flush=True)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        heartbeat_loop(sock)


if __name__ == "__main__":
    main()
