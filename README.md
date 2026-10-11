# SIS150 SmartLight — Optional Version 2 Demonstration

This standalone practice extension builds on concepts in `SIS150-SmartLight` **without changing the existing Version 1.0 GitHub assignment**.

## New features (demonstration only)

1. **Multiple light objects:** Each light keeps independent power and brightness state.
2. **Simulated scheduled activation:** Queue a one-time activation for a named light. Calling `process_due_schedules(current_time)` executes due actions. **This program is not a real-time background scheduler** and does not run when Python is closed.
3. **Save/load settings:** Persist named lights, power, brightness, and outstanding schedules to a local JSON file.

No connection to physical smart bulbs, power systems, network devices, or external services is provided. No actual devices are controlled.

## Files

- `smart_light_v2.py` — SmartLight and SmartLightSystem classes
- `main_v2.py` — simple demonstration using simulated timestamps
- `test_smart_light_v2.py` — automated tests for the new capabilities
- `.gitignore` — omits local generated settings file

## Run

In PowerShell, open the **extracted** folder containing `main_v2.py`.

```powershell
python main_v2.py
python -m unittest discover -v
```

The demo will create `smartlight_settings.json` in the current directory. It uses **simulated January 1, 2030 timestamps** for repeatable demonstrations; it does not wait until 2030.

## Optional next step

A real-world scheduler would require a running event loop, OS scheduling, or another approved service, plus additional security and recovery tests.
