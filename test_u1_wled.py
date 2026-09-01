import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).with_name('u1_wled.py')
spec = importlib.util.spec_from_file_location('u1_wled', MODULE_PATH)
u1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u1)


def heaters(bed_temp=25, bed_target=0, hotend_temp=25, hotend_target=0):
    data = {
        'heater_bed': {'temperature': bed_temp, 'target': bed_target},
        'extruder': {'temperature': hotend_temp, 'target': hotend_target},
        'extruder1': {'temperature': 25, 'target': 0},
        'extruder2': {'temperature': 25, 'target': 0},
        'extruder3': {'temperature': 25, 'target': 0},
    }
    return data


class DesiredStateTests(unittest.TestCase):
    def test_initial_print_bed_heating_overrides_green(self):
        desired, warmup = u1.choose_desired_state(
            'printing', heaters(bed_temp=25, bed_target=60), None, False
        )
        self.assertEqual(desired, 'heating_bed')
        self.assertTrue(warmup)

    def test_initial_print_hotend_heating_overrides_green(self):
        desired, warmup = u1.choose_desired_state(
            'printing', heaters(hotend_temp=25, hotend_target=210), None, False
        )
        self.assertEqual(desired, 'heating_hotend')
        self.assertTrue(warmup)

    def test_initial_print_both_heating_overrides_green(self):
        desired, warmup = u1.choose_desired_state(
            'printing', heaters(25, 60, 25, 210), None, False
        )
        self.assertEqual(desired, 'heating_both')
        self.assertTrue(warmup)

    def test_warmup_switches_to_printing_when_targets_reached(self):
        desired, warmup = u1.choose_desired_state(
            'printing', heaters(59, 60, 209, 210), 'heating_both', True
        )
        self.assertEqual(desired, 'printing')
        self.assertFalse(warmup)

    def test_normal_print_temperature_dip_does_not_replace_green(self):
        desired, warmup = u1.choose_desired_state(
            'printing', heaters(55, 60, 200, 210), 'printing', False
        )
        self.assertEqual(desired, 'printing')
        self.assertFalse(warmup)

    def test_pause_overrides_warmup(self):
        desired, warmup = u1.choose_desired_state(
            'paused', heaters(25, 60, 25, 210), 'heating_both', True
        )
        self.assertEqual(desired, 'paused')
        self.assertTrue(warmup)

    def test_resume_after_normal_pause_stays_green_even_if_temp_dips(self):
        desired, warmup = u1.choose_desired_state(
            'printing', heaters(55, 60, 200, 210), 'paused', False
        )
        self.assertEqual(desired, 'printing')
        self.assertFalse(warmup)

    def test_stale_complete_on_service_start_is_idle(self):
        desired, warmup = u1.choose_desired_state(
            'complete', heaters(), None, False
        )
        self.assertEqual(desired, 'standby')
        self.assertFalse(warmup)

    def test_idle_heating_still_reports_heating(self):
        desired, warmup = u1.choose_desired_state(
            'standby', heaters(bed_temp=25, bed_target=60), 'standby', False
        )
        self.assertEqual(desired, 'heating_bed')
        self.assertFalse(warmup)


class ColorTests(unittest.TestCase):
    def capture_set_wled(self, fn):
        calls = []
        original = u1.set_wled
        try:
            u1.set_wled = lambda *a, **k: calls.append((a, k)) or True
            fn()
        finally:
            u1.set_wled = original
        return calls[0]

    def test_bed_heating_is_deeper_orange(self):
        args, kwargs = self.capture_set_wled(u1.status_heating_bed)
        self.assertEqual(args[:3], (255, 80, 0))

    def test_hotend_heating_is_redder(self):
        args, kwargs = self.capture_set_wled(u1.status_heating_hotend)
        self.assertEqual(args[:3], (255, 20, 0))

    def test_both_heating_is_orange_red(self):
        args, kwargs = self.capture_set_wled(u1.status_heating_both)
        self.assertEqual(args[:3], (255, 50, 0))


if __name__ == '__main__':
    unittest.main()
