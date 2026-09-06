import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "u1_wled.py"

spec = importlib.util.spec_from_file_location("u1_wled", MODULE_PATH)
u1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u1)


class WledPowerTests(unittest.TestCase):
    def test_wled_off_posts_off_state(self):
        calls = []
        original = u1.http_post_json
        try:
            u1.http_post_json = lambda url, payload, timeout=2: calls.append((url, payload, timeout))
            self.assertTrue(u1.wled_off())
        finally:
            u1.http_post_json = original
        self.assertEqual(calls, [(f"{u1.WLED}/json/state", {"on": False}, 2)])

    def test_normal_status_explicitly_turns_wled_on(self):
        calls = []
        original = u1.http_post_json
        try:
            u1.http_post_json = lambda url, payload, timeout=2: calls.append((url, payload, timeout))
            self.assertTrue(u1.set_wled(255, 255, 255, 45, effect=2, speed=45))
        finally:
            u1.http_post_json = original
        self.assertEqual(calls[0][1]["on"], True)


if __name__ == "__main__":
    unittest.main()
