import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCHER = ROOT / "bootcontrol_patch.py"

ORIGINAL = '''COMMIT_LOG_FILE_DIR="/home/lava/printer_data/ota"
case "$1" in
  start)
        echo start-work
        ;;
  stop)
        printf "stop finished\\n"
        ;;
  *)
        exit 1
        ;;
esac
/etc/init.d/S62u1-wled start
exit 0
'''

CORRECTED = '''COMMIT_LOG_FILE_DIR="/home/lava/printer_data/ota"
case "$1" in
  start)
        echo start-work
        /etc/init.d/S62u1-wled start
        /etc/init.d/S63u1-wled-heartbeat start
        ;;
  stop)
        printf "stop finished\\n"
        ;;
  *)
        exit 1
        ;;
esac
exit 0
'''

class BootcontrolPatchTests(unittest.TestCase):
    def run_patcher(self, content):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "S99_bootcontrol"
            path.write_text(content)
            cp = subprocess.run(
                ["python3", str(PATCHER), str(path)],
                text=True,
                capture_output=True,
            )
            return cp, path.read_text()

    def test_moves_old_unconditional_launcher_into_start_branch(self):
        cp, text = self.run_patcher(ORIGINAL)
        self.assertEqual(cp.returncode, 0, cp.stderr)
        self.assertEqual(text.count("/etc/init.d/S62u1-wled start"), 1)
        self.assertEqual(text.count("/etc/init.d/S63u1-wled-heartbeat start"), 1)
        start = text.index("start)")
        stop = text.index("stop)")
        hook = text.index("/etc/init.d/S62u1-wled start")
        self.assertTrue(start < hook < stop)
        self.assertNotIn("esac\n/etc/init.d/S62u1-wled start", text)

    def test_is_idempotent(self):
        cp, text = self.run_patcher(CORRECTED)
        self.assertEqual(cp.returncode, 0, cp.stderr)
        self.assertEqual(text.count("/etc/init.d/S62u1-wled start"), 1)
        self.assertEqual(text.count("/etc/init.d/S63u1-wled-heartbeat start"), 1)
        cp2, text2 = self.run_patcher(text)
        self.assertEqual(cp2.returncode, 0, cp2.stderr)
        self.assertEqual(text2.count("/etc/init.d/S62u1-wled start"), 1)
        self.assertEqual(text, text2)

    def test_refuses_unknown_layout_without_start_branch(self):
        cp, text = self.run_patcher('case "$1" in\n  stop) echo stop ;;\nesac\n')
        self.assertNotEqual(cp.returncode, 0)
        self.assertNotIn("/etc/init.d/S62u1-wled start", text)

    def test_remove_deletes_launcher_without_other_changes(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "S99_bootcontrol"
            path.write_text(CORRECTED)
            cp = subprocess.run(
                ["python3", str(PATCHER), "--remove", str(path)],
                text=True,
                capture_output=True,
            )
            self.assertEqual(cp.returncode, 0, cp.stderr)
            text = path.read_text()
            self.assertNotIn("/etc/init.d/S62u1-wled start", text)
            self.assertIn("echo start-work", text)

if __name__ == "__main__":
    unittest.main()
