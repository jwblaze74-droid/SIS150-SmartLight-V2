"""Demonstrate three OPTIONAL future improvements using simulated time."""

from datetime import datetime
from smart_light_v2 import SmartLightSystem


def main():
    lighting_system = SmartLightSystem()
    living_room_light = lighting_system.add_light("Living room")
    lighting_system.add_light("Bedroom")
    lighting_system.add_light("Porch")

    living_room_light.turn_on()
    living_room_light.set_brightness(75)

    activation_time = datetime(2030, 1, 1, 19, 0)
    lighting_system.schedule_activation("Porch", activation_time)

    print(f"Number of lights: {len(lighting_system.lights)}")
    print(f"Porch on before schedule: {lighting_system.get_light('Porch').is_on}")
    lighting_system.process_due_schedules(datetime(2030, 1, 1, 18, 59))
    print(f"Porch on at 6:59 PM: {lighting_system.get_light('Porch').is_on}")
    lighting_system.process_due_schedules(activation_time)
    print(f"Porch on at 7:00 PM: {lighting_system.get_light('Porch').is_on}")

    lighting_system.save_settings("smartlight_settings.json")
    restored_system = SmartLightSystem.load_settings("smartlight_settings.json")
    print(f"Saved settings to: smartlight_settings.json")
    print(f"Restored living room brightness: {restored_system.get_light('Living room').brightness}")
    print(f"Restored porch power: {restored_system.get_light('Porch').is_on}")


if __name__ == "__main__":
    main()
