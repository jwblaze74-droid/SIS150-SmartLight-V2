"""Optional SmartLight v2 demonstration; does not replace the SIS150 v1 project."""

import json
from datetime import datetime
from pathlib import Path


class SmartLight:
    """One independently controlled light with a name, power state, and brightness."""

    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Light name must not be empty.")
        self.name = name.strip()
        self.is_on = False
        self.brightness = 0

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False
        self.brightness = 0

    def set_brightness(self, level):
        if type(level) is not int or not 0 <= level <= 100:
            raise ValueError("Brightness must be an integer from 0 to 100.")
        self.brightness = level

    def to_record(self):
        return {
            "name": self.name,
            "is_on": self.is_on,
            "brightness": self.brightness,
        }


class SmartLightSystem:
    """Coordinate multiple lights, simulated scheduled actions, and JSON storage."""

    def __init__(self):
        self.lights = {}
        self.schedules = []

    def add_light(self, name):
        new_light = SmartLight(name)
        if new_light.name in self.lights:
            raise ValueError(f"Light already exists: {new_light.name}")
        self.lights[new_light.name] = new_light
        return new_light

    def get_light(self, name):
        if name not in self.lights:
            raise KeyError(f"Unknown light: {name}")
        return self.lights[name]

    def schedule_activation(self, name, activation_time):
        """Queue a one-time ON action (no background timer is started)."""
        self.get_light(name)  # Confirm the light exists before queueing a schedule.
        if not isinstance(activation_time, datetime):
            raise TypeError("activation_time must be a datetime object.")
        self.schedules.append({"name": name, "activation_time": activation_time})

    def process_due_schedules(self, current_time):
        """Execute due ON actions once when the caller checks the schedule."""
        if not isinstance(current_time, datetime):
            raise TypeError("current_time must be a datetime object.")
        remaining_schedules = []
        actions_executed = 0
        for scheduled_action in self.schedules:
            if current_time >= scheduled_action["activation_time"]:
                self.get_light(scheduled_action["name"]).turn_on()
                actions_executed += 1
            else:
                remaining_schedules.append(scheduled_action)
        self.schedules = remaining_schedules
        return actions_executed

    def save_settings(self, file_path):
        """Save light settings and queued actions to a local JSON file."""
        settings = {
            "lights": [light.to_record() for light in self.lights.values()],
            "schedules": [
                {
                    "name": action["name"],
                    "activation_time": action["activation_time"].isoformat(),
                }
                for action in self.schedules
            ],
        }
        Path(file_path).write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")

    @classmethod
    def load_settings(cls, file_path):
        """Restore settings from a trusted JSON file produced by this program."""
        settings = json.loads(Path(file_path).read_text(encoding="utf-8"))
        system = cls()
        for record in settings["lights"]:
            light = system.add_light(record["name"])
            if type(record["is_on"]) is not bool:
                raise ValueError("Saved light power state must be True or False.")
            light.set_brightness(record["brightness"])
            light.is_on = record["is_on"]
        for action in settings["schedules"]:
            system.schedule_activation(
                action["name"], datetime.fromisoformat(action["activation_time"])
            )
        return system
