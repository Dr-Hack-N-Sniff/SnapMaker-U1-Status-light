import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCHER = ROOT / "bootcontrol_patch.py"
REPAIR = ROOT / "repair.sh"
INSTALL = ROOT / "install.sh"
UNINSTALL = ROOT / "uninstall.sh"


class RepairSafetyTests(unittest.TestCase):
    def test_wled_patch_preserves_existing_camera_hook(self):
        original = '''case "$1" in
  start)
        echo start-work
        /etc/init.d/S64u1-camera start
        ;;
  stop)
        echo stop
        ;;
esac
exit 0
'''

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "S99_bootcontrol"
            path.write_text(original)

            cp = subprocess.run(
                ["python3", str(PATCHER), str(path)],
                text=True,
                capture_output=True,
            )

            self.assertEqual(cp.returncode, 0, cp.stderr)

            text = path.read_text()

            self.assertEqual(
                text.count("/etc/init.d/S64u1-camera start"),
                1,
            )
            self.assertEqual(
                text.count("/etc/init.d/S62u1-wled start"),
                1,
            )
            self.assertEqual(
                text.count("/etc/init.d/S63u1-wled-heartbeat start"),
                1,
            )

            start = text.index("start)")
            stop = text.index("stop)")
            camera = text.index("/etc/init.d/S64u1-camera start")

            self.assertTrue(start < camera < stop)

    def test_repair_validates_candidate_before_live_service_writes(self):
        text = REPAIR.read_text()

        self.assertIn("S99_bootcontrol.candidate", text)
        self.assertIn(
            'bootcontrol_patch.py" "$CANDIDATE"',
            text,
        )

        candidate_patch = text.index(
            'bootcontrol_patch.py" "$CANDIDATE"'
        )
        service_write = text.index(
            'cp "$HERE/S62u1-wled" "$SERVICE_DST"'
        )
        heartbeat_write = text.index(
            'cp "$HERE/S63u1-wled-heartbeat" "$HEARTBEAT_SERVICE_DST"'
        )

        self.assertLess(candidate_patch, service_write)
        self.assertLess(candidate_patch, heartbeat_write)

    def test_install_validates_candidate_before_live_service_writes(self):
        text = INSTALL.read_text()

        self.assertIn("S99_bootcontrol.candidate", text)
        self.assertIn(
            'bootcontrol_patch.py" "$CANDIDATE"',
            text,
        )

        candidate_patch = text.index(
            'bootcontrol_patch.py" "$CANDIDATE"'
        )
        service_write = text.index(
            'cp "$HERE/S62u1-wled" "$SERVICE_DST"'
        )
        heartbeat_write = text.index(
            'cp "$HERE/S63u1-wled-heartbeat" "$HEARTBEAT_SERVICE_DST"'
        )

        self.assertLess(candidate_patch, service_write)
        self.assertLess(candidate_patch, heartbeat_write)

    def test_uninstall_validates_candidate_before_live_changes(self):
        text = UNINSTALL.read_text()

        self.assertIn("S99_bootcontrol.candidate", text)
        self.assertIn(
            '--remove "$CANDIDATE"',
            text,
        )

        candidate_patch = text.index(
            '--remove "$CANDIDATE"'
        )
        service_stop = text.index(
            '"$SERVICE_DST" stop'
        )
        service_remove = text.index(
            'rm -f "$SERVICE_DST" "$HEARTBEAT_SERVICE_DST"'
        )

        self.assertLess(candidate_patch, service_stop)
        self.assertLess(candidate_patch, service_remove)

    def test_uninstall_does_not_restore_old_bootcontrol(self):
        text = UNINSTALL.read_text()

        self.assertNotIn(
            "S99_bootcontrol.bak",
            text,
        )

    def test_remove_preserves_camera_hook(self):
        original = '''case "$1" in
  start)
        echo start-work
        /etc/init.d/S64u1-camera start
        /etc/init.d/S62u1-wled start
        /etc/init.d/S63u1-wled-heartbeat start
        ;;
  stop)
        echo stop
        ;;
esac
exit 0
'''

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "S99_bootcontrol"
            path.write_text(original)

            cp = subprocess.run(
                [
                    "python3",
                    str(PATCHER),
                    "--remove",
                    str(path),
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(cp.returncode, 0, cp.stderr)

            text = path.read_text()

            self.assertEqual(
                text.count("/etc/init.d/S64u1-camera start"),
                1,
            )
            self.assertNotIn(
                "/etc/init.d/S62u1-wled start",
                text,
            )
            self.assertNotIn(
                "/etc/init.d/S63u1-wled-heartbeat start",
                text,
            )


if __name__ == "__main__":
    unittest.main()