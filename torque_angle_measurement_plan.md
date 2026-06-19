# Simulation/Test Package #4: Torque-vs-Angle Measurement Tool

## Goal

Build a practical tool and protocol to measure actual magnetic torque versus rotor angle for the PM-gradient motor prototype. The purpose is to report the truth from measured data only. The test must not assume that permanent-magnet torque is continuous net output.

## Deliverables in This Package

1. `torque_angle_measurement_plan.md` — this measurement plan and protocol.
2. `torque_angle_logger.py` — manual angle-stepping CSV logger.
3. `torque_angle_template.csv` — starter CSV format for hand entry or logger output.
4. `torque_angle_analysis.py` — torque calculation, integration, classification, report, and optional plot tool.
5. `torque_angle_report_template.md` — reporting template for measured runs.

## Measurement Principle

A rotor-mounted PM gradient can create positive torque over some angular regions and negative torque over others. The only honest PM-only question is the integrated torque around a closed path:

```text
torque_Nm = force_N * lever_arm_m
work_J = integral(torque_Nm dtheta_rad)
```

If the measured integral over 0° to 360° is positive, that result still requires repeatability, uncertainty analysis, and independent verification before it can be treated as a real energy source. If the integral is approximately zero, the result is consistent with conservative magnetic behavior over a closed path. If the integral is negative, the PM gradient behaves as net drag over the measured revolution.

## Required Hardware

- One rotor with a marked 0° reference.
- One PM gradient section installed in the intended prototype geometry.
- One stationary force gauge or load cell attached at a known lever arm from the shaft center.
- Rigid fixture that prevents the stator/load-cell reference from moving during each reading.
- Angle reference system:
  - rotary table, indexed wheel, encoder display, protractor disk, or printed degree wheel,
  - resolution fine enough for the expected torque variation.
- Calipers or feeler gauges for air-gap measurement.
- Data sheet or notes describing magnet grade, orientation, spacing, and gradient configuration.
- Computer with Python 3 for logging and analysis.

## Coordinate and Sign Convention

Define these before the first reading and keep them unchanged:

- `angle_deg`: rotor mechanical angle, increasing in the intended forward rotation direction.
- `force_n`: signed force reading in newtons.
- Positive force: force that would produce positive forward torque.
- Negative force: force that would resist forward rotation or produce reverse torque.
- `lever_arm_m`: perpendicular distance from shaft center to the force line of action.
- `torque_nm`: `force_n * lever_arm_m`.

Photograph the setup and mark the positive force direction on the fixture.

## Load Cell / Force Gauge Calibration

### Pre-Test Calibration

1. Warm up the load-cell amplifier or force gauge for the manufacturer-recommended time.
2. Mount the sensor in the same orientation used during testing.
3. With no applied load, zero/tare the sensor and record at least 30 seconds of zero readings.
4. Apply at least three known calibration loads spanning the expected force range.
5. Calibrate both positive and negative directions if bidirectional force is expected.
6. Fit or record the force conversion factor and zero offset.
7. Record calibration ID, date, operator, calibration masses, local gravity assumption, and sensor range.

### Post-Test Calibration Check

1. Repeat the zero reading after the torque sweep.
2. Re-apply at least one known positive and one known negative load.
3. If the post-test error exceeds the required uncertainty, mark the run as inconclusive or repeat the sweep.

## Manual Angle-Stepping Protocol

1. Disable all coils and pulse electronics for PM-only measurement.
2. Set and record the air gap.
3. Record magnet configuration, magnet orientation, and gradient-section geometry.
4. Set rotor to 0° and verify that the force sensor is not preloaded outside its calibrated range.
5. Step the rotor from 0° to 360° using a fixed angle increment.
6. At each angle:
   - allow the rotor and force reading to settle,
   - record `angle_deg`, `force_n`, `lever_arm_m`, `air_gap_mm`, `magnet_configuration`, and notes,
   - calculate `torque_nm = force_n * lever_arm_m`,
   - note stiction, backlash, contact, fixture movement, or reading instability.
7. Include both 0° and 360° readings to verify closure at the same physical position.
8. Repeat the sweep in the reverse direction to reveal hysteresis, stiction, or backlash.
9. Repeat the complete forward/reverse sequence at least three times.

## Suggested Angle Resolution

- Start with 5° increments for a full scan.
- Use 1° or 2° increments near sharp gradient regions or sign changes.
- Do not integrate only favorable regions. The energy question requires the full 0° to 360° sweep.

## Using the Logger

Example command:

```bash
python3 torque_angle_logger.py \
  --output torque_angle_measurements.csv \
  --step-deg 5 \
  --lever-arm-m 0.150 \
  --air-gap-mm 5.0 \
  --magnet-configuration "one-gradient-config-A" \
  --calibration-id "cal-001" \
  --operator "OP"
```

The logger prompts for signed force at each angle, calculates torque, and writes a CSV row immediately so partial runs are not lost.

## Using the Analysis Tool

Example command:

```bash
python3 torque_angle_analysis.py torque_angle_measurements.csv \
  --report torque_angle_analysis_report.md \
  --plot torque_angle_plot.png
```

The analysis script:

- reads angle, force, lever arm, air gap, magnet configuration, and notes,
- recalculates torque from force and lever arm,
- integrates torque over angle with the trapezoidal rule,
- classifies PM-only net work over the measured revolution as positive, negative, or approximately zero,
- writes a markdown report,
- creates a plot if `matplotlib` is available.

The script must still run if `matplotlib` is not installed.

## Integration and Classification

The work estimate is:

```text
W_net = sum(0.5 * (tau_i + tau_i+1) * (theta_i+1 - theta_i))
```

where `theta` is in radians. The analysis tool also computes gross absolute torque-angle work:

```text
W_abs = sum(0.5 * (abs(tau_i) + abs(tau_i+1)) * (theta_i+1 - theta_i))
```

Classification defaults:

- approximately zero: `abs(W_net)` is less than `max(0.001 J, 0.02 * W_abs)`
- positive: `W_net` is above that threshold
- negative: `W_net` is below the negative threshold

These thresholds are screening thresholds only. Final claims require a formal uncertainty budget.

## Uncertainty and Error Notes

Track or estimate:

- load-cell zero drift,
- calibration mass uncertainty,
- local gravity assumption,
- lever-arm length uncertainty,
- force line-of-action alignment error,
- angle indexing error,
- air-gap measurement error,
- fixture compliance or movement,
- rotor bearing stiction,
- magnetic hysteresis and path dependence,
- temperature drift,
- operator reading/parallax error for manual force gauges,
- insufficient angular resolution near sharp torque changes,
- mismatch between 0° and 360° closure readings.

The uncertainty in torque can be approximated for first-pass reporting as:

```text
u_tau = sqrt((lever_arm_m * u_force_N)^2 + (force_N * u_lever_arm_m)^2)
```

The uncertainty in integrated work should be computed from the angular samples and reported with the sign of `W_net`. If uncertainty overlaps zero, report the result as approximately zero or inconclusive, not as positive output.

## Pass/Fail Interpretation

This test does not prove a motor by itself. It only measures PM-only torque versus angle.

- Positive measured net work over 360°: possible anomaly or measurement/setup issue requiring repeatability, uncertainty analysis, and independent replication before any energy claim.
- Approximately zero measured net work over 360°: no PM-only continuous net output detected.
- Negative measured net work over 360°: PM gradient imposes net drag in the measured configuration.

If the data show output mechanical work greater than a modeled or measured input, do not call it success unless the source is identified and measured. Use: **unbalanced pending source identification**.

## Minimum Reporting Requirements

Every completed run should report:

- date, operator, calibration ID,
- magnet configuration and air gap,
- angle increment and direction of sweep,
- raw force readings and calculated torque,
- net integrated work per revolution,
- gross absolute torque-angle work,
- classification: positive, negative, approximately zero, or inconclusive,
- uncertainty notes and observed errors,
- plots if available,
- raw CSV file path and analysis command.
