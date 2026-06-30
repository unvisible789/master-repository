# Torque-vs-Angle Measurement Report

## Run Metadata

| Field | Value |
|---|---|
| Date/time |  |
| Operator |  |
| Calibration ID |  |
| Prototype ID |  |
| Rotor ID |  |
| PM gradient configuration |  |
| Magnet grade/orientation |  |
| Air gap (mm) |  |
| Lever arm (m) |  |
| Sweep direction | forward / reverse |
| Angle increment (deg) |  |
| Raw CSV file |  |
| Analysis command |  |

## Purpose

Measure actual PM-gradient magnetic torque versus rotor angle over a full 0° to 360° revolution and integrate measured torque to determine net PM-only work. This report must reflect measured data only and must not assume continuous permanent-magnet net output.

## Calibration Summary

### Load Cell / Force Gauge

- Zero/tare reading before run:
- Calibration loads used:
- Positive direction calibration result:
- Negative direction calibration result:
- Post-test zero reading:
- Post-test calibration check:
- Calibration pass/fail or uncertainty note:

### Geometry

- Lever arm measurement method:
- Lever arm uncertainty:
- Air-gap measurement method:
- Air-gap uncertainty:
- Rotor angle reference method:
- Angle uncertainty:

## Measurement Method

- Coils/pulse electronics disabled for PM-only measurement: yes / no
- Rotor stepped manually from 0° to 360°: yes / no
- Both 0° and 360° measured: yes / no
- Reverse sweep performed: yes / no
- Force sign convention used:
- Notes about stiction, backlash, fixture movement, or unstable readings:

## Equations

```text
torque_Nm = force_N * lever_arm_m
work_J = integral(torque_Nm dtheta_rad)
```

Trapezoidal integration:

```text
W_net = sum(0.5 * (tau_i + tau_i+1) * (theta_i+1 - theta_i))
```

## Results Summary

| Result | Value |
|---|---:|
| Number of angle samples |  |
| Minimum torque (N*m) |  |
| Maximum torque (N*m) |  |
| Mean torque (N*m) |  |
| Net work over 0°–360° (J) |  |
| Gross absolute torque-angle work (J) |  |
| Approximately-zero threshold (J) |  |
| PM-only net work classification | positive / negative / approximately zero / inconclusive |

## Plot

Attach or link torque-vs-angle plot here if generated.

## Interpretation

State only what the measured data support. A positive integral is not automatically continuous motor output. A closed-path PM-only measurement must be repeatable, uncertainty-bounded, and reconciled with the full energy budget before any claim is made.

Use one of these conclusion labels:

- `positive PM-only net work measured; requires replication and source identification`
- `negative PM-only net work measured`
- `approximately zero PM-only net work measured`
- `inconclusive due to measurement uncertainty or setup error`
- `unbalanced pending source identification`

## Uncertainty and Error Notes

Document the relevant error terms:

- load-cell zero drift:
- load-cell calibration uncertainty:
- lever-arm uncertainty:
- angle indexing uncertainty:
- air-gap uncertainty:
- force line-of-action alignment:
- bearing stiction/friction:
- fixture compliance:
- magnetic hysteresis/path dependence:
- temperature drift:
- angular resolution limits:
- 0°/360° closure mismatch:

## Repeatability

| Repeat | Direction | Net work (J) | Classification | Notes |
|---:|---|---:|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |

If repeat runs disagree in sign or uncertainty overlaps zero, report the result as inconclusive rather than positive output.

## Raw Data Location

- Raw CSV:
- Analysis report:
- Plot file:
- Photos/setup documentation:
