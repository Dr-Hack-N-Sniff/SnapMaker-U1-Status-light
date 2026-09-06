import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / 'u1_wled_heartbeat.py'


def load_module():
    spec = importlib.util.spec_from_file_location('u1_wled_heartbeat', MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HeartbeatTests(unittest.TestCase):
    def test_heartbeat_packet_exact_bytes(self):
        m = load_module()
        self.assertEqual(m.HEARTBEAT_PACKET, bytes([0xA5, 0x55, 0x31, 0x48, 0x42, 0x01]))

    def test_default_interval_is_three_seconds(self):
        m = load_module()
        self.assertEqual(m.HEARTBEAT_INTERVAL, 3.0)

    def test_send_once_sends_six_bytes_to_udp_port(self):
        m = load_module()

        class FakeSocket:
            def __init__(self):
                self.calls = []

            def sendto(self, payload, target):
                self.calls.append((payload, target))
                return len(payload)

        sock = FakeSocket()
        sent = m.send_once(sock, '192.0.2.10', 21324)
        self.assertEqual(sent, 6)
        self.assertEqual(sock.calls, [(m.HEARTBEAT_PACKET, ('192.0.2.10', 21324))])

    def test_loop_catches_network_error_and_keeps_running(self):
        m = load_module()

        class FlakySocket:
            def __init__(self):
                self.calls = 0

            def sendto(self, payload, target):
                self.calls += 1
                if self.calls == 1:
                    raise OSError('temporary network failure')
                return len(payload)

        sleeps = []
        sock = FlakySocket()
        m.heartbeat_loop(
            sock,
            '192.0.2.10',
            21324,
            3.0,
            sleep_fn=lambda seconds: sleeps.append(seconds),
            iterations=2,
        )
        self.assertEqual(sock.calls, 2)
        self.assertEqual(sleeps, [3.0, 3.0])


if __name__ == '__main__':
    unittest.main()
