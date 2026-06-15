# Energy Measurement Protocol

## Objective

Measure whether the smallest prototype produces mechanical output energy that is fully explained by measured electrical input, measured recovery, kinetic-energy change, and losses. The protocol is neutral: the expected outcome is unknown until measured.

## Pre-Test Setup

1. Install one rotor, one PM gradient section, and one EML50mm-24 channel.
2. Measure and record rotor geometry, magnet geometry, air gap, and alignment.
3. Install position/RPM, voltage, current, torque, recovery, and temperature sensors.
4. Confirm all sensors are connected to a synchronized logger.
5. Define positive rotation, positive torque, positive coil current, positive bus current, and positive recovery current before collecting data.

## Calibration Checklist

| Calibration | Method | Acceptance Requirement |
|---|---|---|
| Voltage channels | Apply known voltages across expected range | Gain/offset documented and stable |
| Current channels | Apply known currents including recovery direction | Polarity and scale documented |
| Torque channel | Apply known weights at known lever arm | Linear fit documented before and after test |
| Position/RPM | Compare encoder/Hall timing with physical marks and tachometer | Counts/angle and RPM agree within required uncertainty |
| Time alignment | Apply a known timing event visible on multiple channels | Channel skew is known or corrected |
| Friction baseline | Coast-down test with channel unpowered | Loss torque curve recorded |

## Measurement Runs

### Run A: Unpowered Baseline

- Spin the rotor through the PM gradient with the EML50mm-24 unpowered.
- Record position, RPM, torque/load if connected, and temperature.
- Use this run to identify passive magnetic drag, bearing loss, windage, and sensor noise.

### Run B: Single-Pulse Characterization

- Run the rotor at a controlled initial speed.
- Apply one pulse at a known rotor angle.
- Record coil voltage/current, bus voltage/current, recovery voltage/current, position, RPM, and torque.
- Repeat at multiple timing advances and pulse widths.
- Compare rotor kinetic-energy change before and after the pulse.

### Run C: Repeated Full-Revolution Test

- Apply the selected pulse schedule over at least 30 consecutive full revolutions.
- Compute electrical and mechanical energy per pulse and per revolution.
- Verify whether rotor speed returns to equivalent initial conditions for each compared interval.

### Run D: Loaded Output Test

- Apply a calibrated mechanical load or brake.
- Record shaft torque and RPM continuously.
- Compute mechanical output energy delivered to the load.
- Compare against net electrical input and measured losses over the same interval.

## Energy Accounting

### Instantaneous Electrical Power at Driver Input

```text
P_bus(t) = V_bus(t) * I_bus(t)
```

### Driver Input Energy

```text
E_bus_in = integral(P_bus(t) dt)
```

### Coil Terminal Energy

```text
P_coil(t) = V_coil(t) * I_coil(t)
E_coil_terminal = integral(P_coil(t) dt)
```

### Recovered Energy

```text
P_recovery(t) = V_recovery(t) * I_recovery(t)
E_recovered = integral(P_recovery(t) dt)
```

Only count `E_recovered` if it is measured as energy returned to a reusable storage element. Do not count an uncollected inductive voltage spike as recovered energy.

### Net Electrical Energy

Use one of these accounting modes and state it in the run log:

```text
Mode 1: E_elec_net = E_bus_in - E_recovered
Mode 2: E_elec_net = signed integral(V_bus(t) * I_bus(t) dt)
```

Do not subtract recovery twice.

### Mechanical Output Energy

```text
P_mech(t) = tau(t) * omega(t)
E_mech_out = integral(P_mech(t) dt)
```

### Rotor Kinetic-Energy Change

```text
Delta_E_kinetic = 0.5 * J * (omega_final^2 - omega_initial^2)
```

### Loss Accounting

```text
E_loss_est = integral(tau_loss(omega) dtheta)
```

Estimate `tau_loss(omega)` from unpowered coast-down data and report uncertainty. Do not hide unexplained energy in a loss term unless it is measured or bounded.

### Balance Residual

```text
E_residual = E_elec_net - E_mech_out - Delta_E_kinetic - E_loss_est
```

Interpretation:

- `E_residual >= 0` within uncertainty: output is not greater than measured input after accounting terms.
- `E_residual < 0` beyond uncertainty: mechanical output is greater than measured electrical input and modeled losses; result is **unbalanced pending source identification** unless another measured source is identified.

## Pass/Fail Criteria

### Pass for Energy-Accounted Operation

A run may be called energy-accounted only if:

1. All required channels are calibrated and synchronized.
2. The comparison interval covers complete rotor revolutions or identical initial/final rotor states.
3. Net electrical energy, recovered energy, mechanical output, kinetic-energy change, and losses are computed over the same interval.
4. The balance residual is nonnegative or consistent with zero within uncertainty.
5. Results repeat across independent runs.

### Falsification or Inconclusive Outcome

The claim is falsified or must be reported as inconclusive if:

- Mechanical output exceeds measured net electrical input without a measured source.
- The system only appears favorable when selected angular windows are analyzed.
- Sensor calibration or timing uncertainty can change the energy-balance conclusion.
- The rotor slows down or speeds up substantially and kinetic-energy change is not included.
- Recovery is claimed but not measured into reusable storage.

When output mechanical energy is greater than measured electrical input, do not call it success. Call it **unbalanced pending source identification**.

## Repeatability and Reporting

For every condition:

- Collect at least 30 full revolutions per run.
- Repeat the run at least three times after stopping and restarting.
- Report mean, standard deviation, minimum, and maximum for:
  - `E_bus_in`
  - `E_recovered`
  - `E_elec_net`
  - `E_mech_out`
  - `Delta_E_kinetic`
  - `E_loss_est`
  - `E_residual`
  - RPM
  - torque
- Report environmental and component temperatures.
- Preserve raw data and analysis scripts.

## Required Conclusion Language

Use one of these conclusion labels:

- `energy-accounted within uncertainty`
- `loss-dominated or below breakeven`
- `unbalanced pending source identification`
- `inconclusive due to measurement uncertainty`

Do not use `success`, `over-unity`, or similar language unless the energy source is measured and the accounting closes.
