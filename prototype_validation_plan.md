# Simulation #3: Prototype Validation Plan

## Goal

Design the smallest physical experiment capable of validating or falsifying the PM-gradient motor concept with honest energy accounting. The experiment uses one rotor, one permanent-magnet gradient section, and one EML50mm-24 interaction channel. The purpose is to discover the truth, not to prove the concept.

## Minimum Prototype Scope

### Mechanical System

- One rigid rotor with known radius and moment of inertia.
- One permanent-magnet gradient section mounted at a fixed angular location.
- One stationary EML50mm-24 electromagnetic actuator/channel aligned to interact with the gradient section.
- One low-friction shaft and bearing set.
- One torque measurement element, either:
  - a calibrated reaction torque sensor on a controllable load/brake, or
  - a calibrated dynamometer/load cell and known lever arm.

### Electrical System

- One pulse driver for the EML50mm-24.
- A measured DC supply input to the driver.
- A measured coil voltage channel.
- A measured coil current channel.
- A measured flyback/recovery path, if energy recovery is claimed.
- A Hall sensor or encoder for angular position and timing.
- RPM measurement derived from encoder/Hall timing and independently cross-checked where possible.

### Data Logging System

The logger must record synchronized electrical, mechanical, and position data. Minimum channels:

| Channel | Required Signal | Minimum Use |
|---|---|---|
| Rotor position | Hall sensor index pulses or encoder angle | Pulse timing, RPM, per-event segmentation |
| Coil voltage | Differential voltage across EML50mm-24 | Electrical energy into/out of coil |
| Coil current | Hall current sensor, shunt amplifier, or current probe | Electrical energy into/out of coil |
| Supply voltage | DC bus voltage at driver input | Driver-level input energy |
| Supply current | DC bus current into driver | Driver-level input energy |
| Flyback voltage/current | Recovery path voltage and current | Claimed recovered energy |
| Torque | Shaft torque or reaction torque | Mechanical output work/power |
| RPM | Encoder/Hall-derived and logged | Mechanical power calculation |
| Temperature | Coil, driver, magnets, bearings | Drift and loss tracking |

## Exact Measurements Required

### Geometry and Mechanical Constants

1. Rotor radius and diameter.
2. Rotor mass and moment of inertia.
3. Magnet positions and gradient-section angular span.
4. EML50mm-24 air gap and alignment relative to the gradient section.
5. Load/brake lever arm length if using a load cell.
6. Bearing preload and baseline friction estimate.

### Electrical Measurements

1. Coil voltage waveform, `V_coil(t)`.
2. Coil current waveform, `I_coil(t)`.
3. Driver DC input voltage, `V_bus(t)`.
4. Driver DC input current, `I_bus(t)`.
5. Flyback/recovery voltage, `V_recovery(t)`, if applicable.
6. Flyback/recovery current, `I_recovery(t)`, if applicable.
7. Pulse command timing relative to rotor angle.
8. Driver switching state, if available.

### Mechanical Measurements

1. Shaft or reaction torque, `tau(t)`.
2. Rotor angular position, `theta(t)`.
3. Rotor speed, `omega(t)`.
4. Load setting and load torque calibration.
5. Coast-down deceleration for friction/windage estimation.

## Calibration Procedure

### 1. Sensor Zero Checks

- With the system unpowered and stationary, record all voltage, current, torque, and position channels for at least 30 seconds.
- Store mean offsets and standard deviations.
- Subtract offsets from all subsequent measurements.
- Fail calibration if any zero offset is unstable by more than the sensor accuracy needed for the expected signal.

### 2. Voltage Calibration

- Apply at least three known DC voltages spanning the expected measurement range.
- Record each logger channel response.
- Fit gain and offset for each voltage channel.
- Verify differential coil voltage polarity by applying a known low-voltage current-limited test pulse.

### 3. Current Calibration

- Pass known DC currents through the current sensor or shunt path at several levels, including both directions if bidirectional recovery is measured.
- Fit gain and offset.
- Verify bandwidth is sufficient to resolve pulse edges and flyback current.

### 4. Torque Calibration

- Apply known static torques using calibrated weights and a measured lever arm.
- Calibrate both torque directions.
- Verify torque sensor linearity over the expected operating range.
- Repeat after the run to check drift.

### 5. Position and RPM Calibration

- Verify encoder counts per revolution or Hall pulse angle using a marked rotor and reference index.
- Confirm that the measured gradient-section angle matches the physical magnet placement.
- Compare logged RPM against an independent optical tachometer at several speeds.

### 6. Friction and Windage Baseline

- Run coast-down tests with the EML50mm-24 unpowered and the load disconnected or set to zero.
- Estimate loss torque from angular deceleration:

```text
tau_loss(omega) = -J * domega/dt
```

- Repeat coast-down with the magnet gradient installed and removed if possible to separate magnetic drag from bearing/windage losses.

## Test Sequence

1. Assemble the one-rotor, one-gradient, one-channel prototype.
2. Complete all calibrations before energizing the motor channel.
3. Record an unpowered spin/coast baseline through the gradient section.
4. Run low-energy single-pulse tests at fixed rotor speeds.
5. Sweep pulse timing around the nominal advance angle, including the requested timing advance if applicable.
6. Sweep pulse window widths while keeping bus voltage, current limit, and load constant.
7. Repeat each condition for enough revolutions to support repeatability criteria.
8. Perform a post-test zero and torque calibration check.
9. Compare measured electrical input, recovered energy, mechanical output, and losses over identical angular windows and full revolutions.

## Energy Accounting Equations

### Electrical Input to Driver

```text
E_bus_in = integral(V_bus(t) * I_bus(t) dt) over the test interval
```

Use signed current convention. Positive `I_bus` means energy leaves the supply and enters the driver.

### Coil Electrical Energy

```text
E_coil_terminal = integral(V_coil(t) * I_coil(t) dt)
```

This is terminal energy at the coil and may differ from bus energy because of driver losses and recovery paths.

### Recovered Energy

```text
E_recovered = integral(V_recovery(t) * I_recovery(t) dt)
```

Only count recovered energy if it is measured returning to a reusable storage element such as the DC bus capacitor or battery. Do not count open-circuit voltage spikes as recovered energy.

### Net Electrical Energy

```text
E_elec_net = E_bus_in - E_recovered
```

If recovery is already included in signed bus power, do not subtract it again. The accounting method must be declared before testing.

### Mechanical Output Power

```text
P_mech_out(t) = tau_load(t) * omega(t)
```

### Mechanical Output Energy

```text
E_mech_out = integral(tau_load(t) * omega(t) dt)
```

For angle-based analysis:

```text
E_mech_out = integral(tau_load(theta) dtheta)
```

### Rotor Kinetic Energy Change

```text
Delta_E_kinetic = 0.5 * J * (omega_final^2 - omega_initial^2)
```

### Full Energy Balance

```text
E_elec_net + E_initial_stored = E_mech_out + Delta_E_kinetic + E_losses + E_final_stored
```

For steady repeated operation over full revolutions, the rotor should return to the same speed and stored-field state. If not, report the result as transient energy exchange, not continuous output.

## Pass/Fail Criteria

The prototype must not be declared successful merely because it rotates or because instantaneous torque is positive. It passes only if all applicable criteria are satisfied.

### Pass Criteria

- Electrical, torque, RPM, and position measurements are synchronized and calibrated.
- The same energy accounting convention is used for all test cases.
- Over repeated full revolutions, net mechanical output plus measured losses does not exceed net electrical input unless an additional measured energy source is explicitly identified.
- Any claimed recovery is directly measured as reusable returned energy.
- Rotor speed and stored energy return to equivalent initial conditions for steady-state comparisons.
- Results are repeatable within the stated repeatability requirement.

### Fail or Inconclusive Criteria

- Mechanical output exceeds net electrical input with no measured source for the difference.
- Only favorable angular sectors are measured while unfavorable sectors are omitted.
- Flyback is inferred but not measured as returned reusable energy.
- Rotor kinetic energy changes are ignored.
- Torque is assumed rather than measured.
- Sensor timing, polarity, or calibration uncertainty is large enough to change the conclusion.

If mechanical output is greater than measured electrical input and no modeled/measured source explains the difference, the conclusion is **unbalanced pending source identification**, not success.

## Sources of Error

- Current sensor bandwidth too low for short pulses.
- Voltage probe ground reference errors or insufficient common-mode rejection.
- Incorrect sign convention for current during flyback/recovery.
- Torque sensor zero drift or dynamic response limitations.
- Encoder/Hall timing jitter.
- Incorrect rotor moment of inertia.
- Ignoring rotor acceleration or deceleration during the measurement interval.
- Measuring only the attractive portion of a PM gradient and omitting exit drag.
- Magnetic hysteresis, eddy-current drag, and heating.
- Bearing friction changes with temperature and speed.
- Driver switching losses omitted from coil-terminal-only measurements.
- Aliasing from inadequate sample rate.

## Repeatability Requirements

- Record at least 30 consecutive full revolutions for each steady test condition.
- Repeat each test condition at least three separate times after stopping and restarting the prototype.
- Report mean, standard deviation, minimum, and maximum for net electrical energy, mechanical output energy, RPM, and torque.
- A claimed positive energy margin must exceed combined measurement uncertainty by at least 5 standard deviations.
- If the sign of the net balance changes across repeats, the result is inconclusive.

## Data Retention Requirements

Save raw and processed data for every run:

- Raw time-series CSV or binary logger file.
- Calibration records before and after the run.
- Processed per-pulse and per-revolution energy tables.
- Test configuration notes, including air gap, magnet orientation, pulse timing, pulse width, bus voltage, current limit, and load setting.
- Photos or diagrams documenting the physical setup.
