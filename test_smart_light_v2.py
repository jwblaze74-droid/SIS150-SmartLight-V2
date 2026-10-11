"""Tests for the optional v2 SmartLight demonstration."""

import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from smart_light_v2 import SmartLightSystem


class TestSmartLightSystem(unittest.TestCase):
    def setUp(self):
        self.system = SmartLightSystem()
        self.system.add_light("Kitchen")
        self.system.add_light("Porch")

    def test_multiple_lights_remain_independent(self):
        self.system.get_light("Kitchen").turn_on()
        self.assertTrue(self.system.get_light("Kitchen").is_on)
        self.assertFalse(self.system.get_light("Porch").is_on)

    def test_schedule_does_not_activate_early(self):
        self.system.schedule_activation("Porch", datetime(2030, 1, 1, 19, 0))
        self.assertEqual(self.system.process_due_schedules(datetime(2030, 1, 1, 18, 59)), 0)
        self.assertFalse(self.system.get_light("Porch").is_on)

    def test_schedule_activates_when_due(self):
        self.system.schedule_activation("Porch", datetime(2030, 1, 1, 19, 0))
        self.assertEqual(self.system.process_due_schedules(datetime(2030, 1, 1, 19, 0)), 1)
        self.assertTrue(self.system.get_light("Porch").is_on)

    def test_scheduled_action_executes_only_once(self):
        self.system.schedule_activation("Porch", datetime(2030, 1, 1, 19, 0))
        self.system.process_due_schedules(datetime(2030, 1, 1, 19, 0))
        self.assertEqual(self.system.process_due_schedules(datetime(2030, 1, 1, 19, 1)), 0)

    def test_settings_can_be_saved_and_reloaded(self):
        self.system.get_light("Kitchen").turn_on()
        self.system.get_light("Kitchen").set_brightness(60)
        self.system.schedule_activation("Porch", datetime(2030, 1, 1, 19, 0))
        with tempfile.TemporaryDirectory() as temp_folder:
            settings_path = Path(temp_folder) / "settings.json"
            self.system.save_settings(settings_path)
            restored = SmartLightSystem.load_settings(settings_path)
        self.assertTrue(restored.get_light("Kitchen").is_on)
        self.assertEqual(restored.get_light("Kitchen").brightness, 60)
        self.assertEqual(len(restored.schedules), 1)

    def test_invalid_brightness_is_rejected(self):
        with self.assertRaises(ValueError):
            self.system.get_light("Kitchen").set_brightness(120)

    def test_unknown_light_cannot_be_scheduled(self):
        with self.assertRaises(KeyError):
            self.system.schedule_activation("Garage", datetime(2030, 1, 1, 19, 0))

    def test_duplicate_light_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.system.add_light("Kitchen")


if __name__ == "__main__":
    unittest.main()
