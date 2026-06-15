# Sensor Wiring Diagram

## Purpose

This wiring plan captures the minimum sensor layout needed to validate or falsify the one-rotor, one-gradient, one-EML50mm-24 prototype. It prioritizes synchronized measurements and clear energy-flow sign conventions.

## High-Level Block Diagram

```text
                +----------------------+
                |      DC SUPPLY       |
                |  +              -    |
                +--|--------------|----+
                   |              |
             V_bus sense      I_bus sensor
                   |              |
                   v              v
             +--------------------------+
             |       PULSE DRIVER       |
             | command in / gate timing |
             +-----------+--------------+
                         |
                         | switched output
                         v
        V_coil sense +---------+ I_coil sensor
              across | EML50mm | in series with coil
                     |   -24   |
                     +----+----+
                          |
                          v
              +------------------------+
              | flyback/recovery path  |
              | V_recovery/I_recovery  |
              +------------------------+

      +-----------------------------------------------+
      | ROTOR: one PM gradient section on one rotor    |
      +-----------------------------------------------+
             ^                         |
             |                         v
      Hall sensor or encoder      torque sensor/load cell
             |                         |
             v                         v
      position/RPM channel        torque channel

All sensor outputs go to one synchronized DAQ/logger.
```

## Required Connections

| Signal | Sensor/Connection | Logger Channel | Sign Convention |
|---|---|---|---|
| `V_bus(t)` | Differential measurement at driver DC input | Analog voltage | Positive when supply positive terminal is above supply return |
| `I_bus(t)` | Current sensor in positive supply lead | Analog current | Positive when energy flows from supply into driver |
| `V_coil(t)` | Differential measurement across EML50mm-24 terminals | Analog voltage | Positive at driver-switched terminal relative to return terminal |
| `I_coil(t)` | Series current sensor in EML50mm-24 path | Analog current | Positive for intended assist pulse direction |
| `V_recovery(t)` | Differential measurement across recovery destination | Analog voltage | Positive when recovered storage element is charged |
| `I_recovery(t)` | Current sensor in recovery path | Analog current | Positive when energy returns to reusable storage |
| `theta(t)` | Hall sensor, index sensor, or encoder | Digital/position | Increasing angle in the defined forward rotation direction |
| `RPM(t)` | Derived from encoder/Hall and optionally tachometer | Computed plus optional analog/digital | Positive in forward rotation direction |
| `tau(t)` | Shaft torque sensor or load cell amplifier | Analog torque | Positive when load receives output torque |
| `T_coil/driver/magnet/bearing` | Thermocouples or temperature sensors | Analog/digital temperature | Absolute temperature for drift tracking |

## Logger Requirements

- All channels used in energy equations must share the same time base.
- Electrical voltage/current sampling must be fast enough to resolve pulse edges and flyback events.
- Position timestamps must be accurate enough to assign each pulse to its angular window.
- Torque and RPM must be logged continuously, not only as display readings.
- Raw data must be retained; do not keep only averaged values.

## Isolation and Grounding Notes

- Use differential or isolated measurements for coil voltage and bus voltage to avoid shorting the driver through oscilloscope grounds.
- Confirm current sensor polarity with a known low-current test before powered rotor testing.
- Keep high-current coil wiring physically separated from Hall/encoder wiring to reduce timing noise.
- Use twisted pairs or shielded cables for low-level torque and position signals where practical.

## Timing Reference

The encoder or Hall sensor is the timing reference for pulse advance and pulse-window analysis. The logger should record the pulse command signal as an additional digital channel when available, so the commanded pulse can be compared against actual coil current and rotor position.
