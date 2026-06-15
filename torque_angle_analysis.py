#!/usr/bin/env python3
"""
Analyze PM-gradient torque-vs-angle measurements.

Reads a CSV containing angle, force, lever arm, and/or torque columns, then
integrates torque over rotor angle to estimate net work per revolution. The
script reports whether measured PM-only net work over 360 degrees is positive,
negative, or approximately zero. It does not assume permanent magnets provide
continuous net output; it reports only what the measured data support.

Optional plotting uses matplotlib when installed, but analysis works without it.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

REQUIRED_COLUMNS = {"angle_deg", "force_n", "lever_arm_m"}
DEFAULT_ZERO_THRESHOLD_J = 0.001
DEFAULT_RELATIVE_THRESHOLD = 0.02


@dataclass(frozen=True)
class Measurement:
    angle_deg: float
    angle_rad: float
    force_n: float
    lever_arm_m: float
    torque_nm: float
    air_gap_mm: str
    magnet_configuration: str
    notes: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Integrate measured PM-gradient torque vs angle over one revolution."
    )
    parser.add_argument("input_csv", help="Torque-angle measurement CSV path.")
    parser.add_argument(
        "--report",
        default="torque_angle_analysis_report.md",
        help="Markdown report output path. Default: torque_angle_analysis_report.md",
    )
    parser.add_argument(
        "--plot",
        default="torque_angle_plot.png",
        help="Plot output path if matplotlib is available. Default: torque_angle_plot.png",
    )
    parser.add_argument(
        "--zero-threshold-j",
        type=float,
        default=DEFAULT_ZERO_THRESHOLD_J,
        help="Absolute work magnitude at or below this is approximately zero. Default: 0.001 J",
    )
    parser.add_argument(
        "--relative-threshold",
        type=float,
        default=DEFAULT_RELATIVE_THRESHOLD,
        help="Also treat net work as approximately zero if |net| is below this fraction of gross absolute work. Default: 0.02",
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Skip plotting even if matplotlib is available.",
    )
    return parser.parse_args()


def optional_float(value: str, default: float = 0.0) -> float:
    value = (value or "").strip()
    if not value:
        return default
    return float(value)


def read_measurements(path: Path) -> list[Measurement]:
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")
        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")

        measurements: list[Measurement] = []
        for line_number, row in enumerate(reader, start=2):
            if not row.get("angle_deg", "").strip():
                continue
            try:
                angle_deg = float(row["angle_deg"])
                force_n = float(row["force_n"])
                lever_arm_m = float(row["lever_arm_m"])
                torque_nm = optional_float(row.get("torque_nm", ""), force_n * lever_arm_m)
            except ValueError as exc:
                raise ValueError(f"Invalid numeric value on CSV line {line_number}: {exc}") from exc

            calculated_torque = force_n * lever_arm_m
            if abs(torque_nm - calculated_torque) > max(1e-9, abs(calculated_torque) * 1e-6):
                print(
                    f"Warning: line {line_number} torque_nm differs from force_n * lever_arm_m; "
                    "using calculated torque."
                )
                torque_nm = calculated_torque

            measurements.append(
                Measurement(
                    angle_deg=angle_deg,
                    angle_rad=math.radians(angle_deg),
                    force_n=force_n,
                    lever_arm_m=lever_arm_m,
                    torque_nm=torque_nm,
                    air_gap_mm=row.get("air_gap_mm", ""),
                    magnet_configuration=row.get("magnet_configuration", ""),
                    notes=row.get("notes", ""),
                )
            )

    if len(measurements) < 2:
        raise ValueError("At least two measurements are required for integration")

    return sorted(measurements, key=lambda item: item.angle_deg)


def integrate_trapezoid(measurements: list[Measurement]) -> tuple[float, float]:
    """Return signed net work and gross absolute work in joules."""
    net_work_j = 0.0
    gross_abs_work_j = 0.0
    for left, right in zip(measurements, measurements[1:]):
        delta_theta = right.angle_rad - left.angle_rad
        if delta_theta <= 0:
            raise ValueError("Angles must be strictly increasing after sorting")
        avg_torque = 0.5 * (left.torque_nm + right.torque_nm)
        net_work_j += avg_torque * delta_theta
        gross_abs_work_j += 0.5 * (abs(left.torque_nm) + abs(right.torque_nm)) * delta_theta
    return net_work_j, gross_abs_work_j


def classify_work(net_work_j: float, gross_abs_work_j: float, zero_threshold_j: float, relative_threshold: float) -> str:
    threshold = max(zero_threshold_j, gross_abs_work_j * relative_threshold)
    if abs(net_work_j) <= threshold:
        return "approximately zero"
    if net_work_j > 0:
        return "positive"
    return "negative"


def maybe_plot(measurements: list[Measurement], output_path: Path, no_plot: bool) -> str:
    if no_plot:
        return "Plot skipped by --no-plot."
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except ImportError:
        return "Plot skipped because matplotlib is not installed."

    angles = [item.angle_deg for item in measurements]
    torques = [item.torque_nm for item in measurements]
    plt.figure(figsize=(9, 5))
    plt.plot(angles, torques, marker="o")
    plt.axhline(0.0, color="black", linewidth=0.8)
    plt.xlabel("Rotor angle (deg)")
    plt.ylabel("Torque (N*m)")
    plt.title("Measured PM-gradient torque vs rotor angle")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return f"Plot written to {output_path}."


def write_report(
    path: Path,
    input_csv: Path,
    measurements: list[Measurement],
    net_work_j: float,
    gross_abs_work_j: float,
    classification: str,
    plot_message: str,
    zero_threshold_j: float,
    relative_threshold: float,
) -> None:
    torques = [item.torque_nm for item in measurements]
    forces = [item.force_n for item in measurements]
    lever_arms = [item.lever_arm_m for item in measurements]
    angle_min = measurements[0].angle_deg
    angle_max = measurements[-1].angle_deg
    threshold = max(zero_threshold_j, gross_abs_work_j * relative_threshold)

    report = f"""# Torque-vs-Angle Analysis Report

## Input

- Source CSV: `{input_csv}`
- Measurement count: {len(measurements)}
- Angle range: {angle_min:.6g}° to {angle_max:.6g}°
- Mean lever arm: {mean(lever_arms):.9g} m

## Equations

```text
torque_Nm = force_N * lever_arm_m
work_J = integral(torque_Nm dtheta_rad)
```

The integration uses the trapezoidal rule on measured torque vs rotor angle.

## Results

- Net measured work over recorded angle span: **{net_work_j:.9g} J**
- Gross absolute torque-angle work: **{gross_abs_work_j:.9g} J**
- Approximately-zero threshold used: **{threshold:.9g} J**
- PM-only net work classification: **{classification}**
- Minimum torque: **{min(torques):.9g} N*m**
- Maximum torque: **{max(torques):.9g} N*m**
- Mean torque: **{mean(torques):.9g} N*m**
- Minimum force: **{min(forces):.9g} N**
- Maximum force: **{max(forces):.9g} N**
- {plot_message}

## Interpretation Rule

A positive PM-only integrated result is not automatically a validated continuous motor output. It must be repeated, uncertainty-bounded, and reconciled with the full 360° mechanical and electrical energy budget. A result near zero is consistent with conservative magnetic-field behavior over a closed path. A negative result indicates net drag over the measured revolution.

## Data Quality Checks

- Confirm that 0° and 360° represent the same physical rotor reference.
- Confirm that force sign convention was not changed during the sweep.
- Confirm that the force gauge was zeroed and calibrated before and after the run.
- Confirm that the air gap and magnet configuration did not change during the sweep.
- Confirm that no external electrical pulse or mechanical assist was applied during PM-only measurements.
"""
    path.write_text(report, encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_csv = Path(args.input_csv)
    measurements = read_measurements(input_csv)
    net_work_j, gross_abs_work_j = integrate_trapezoid(measurements)
    classification = classify_work(
        net_work_j,
        gross_abs_work_j,
        args.zero_threshold_j,
        args.relative_threshold,
    )
    plot_message = maybe_plot(measurements, Path(args.plot), args.no_plot)
    write_report(
        Path(args.report),
        input_csv,
        measurements,
        net_work_j,
        gross_abs_work_j,
        classification,
        plot_message,
        args.zero_threshold_j,
        args.relative_threshold,
    )

    print(f"Net work: {net_work_j:.9g} J")
    print(f"Gross absolute work: {gross_abs_work_j:.9g} J")
    print(f"PM-only net work classification: {classification}")
    print(plot_message)
    print(f"Report written to {args.report}")


if __name__ == "__main__":
    main()
