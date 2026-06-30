#!/usr/bin/env python3
"""
Manual torque-vs-angle logger for the PM-gradient motor prototype.

This tool supports stepping the rotor from 0 to 360 degrees and recording a
force/load-cell reading at each angle. Torque is calculated as:

    torque_Nm = force_N * lever_arm_m

The script is intentionally simple and uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

FIELDNAMES = [
    "timestamp_utc",
    "angle_deg",
    "force_n",
    "lever_arm_m",
    "torque_nm",
    "air_gap_mm",
    "magnet_configuration",
    "calibration_id",
    "operator",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Log manual torque-vs-angle measurements for a PM-gradient prototype."
    )
    parser.add_argument(
        "--output",
        default="torque_angle_measurements.csv",
        help="CSV output path. Default: torque_angle_measurements.csv",
    )
    parser.add_argument(
        "--start-deg",
        type=float,
        default=0.0,
        help="First angle in degrees. Default: 0",
    )
    parser.add_argument(
        "--stop-deg",
        type=float,
        default=360.0,
        help="Last angle in degrees. Default: 360",
    )
    parser.add_argument(
        "--step-deg",
        type=float,
        default=5.0,
        help="Manual stepping increment in degrees. Default: 5",
    )
    parser.add_argument(
        "--lever-arm-m",
        type=float,
        required=True,
        help="Lever arm length in meters from shaft center to force line of action.",
    )
    parser.add_argument(
        "--air-gap-mm",
        type=float,
        required=True,
        help="Air gap in millimeters for this measurement run.",
    )
    parser.add_argument(
        "--magnet-configuration",
        required=True,
        help="Short description or ID for the PM gradient configuration.",
    )
    parser.add_argument(
        "--calibration-id",
        default="",
        help="Load-cell/force-gauge calibration record ID.",
    )
    parser.add_argument("--operator", default="", help="Operator name or initials.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append to an existing CSV instead of overwriting it.",
    )
    return parser.parse_args()


def angle_sequence(start: float, stop: float, step: float) -> list[float]:
    if step <= 0:
        raise ValueError("step-deg must be greater than zero")
    angles: list[float] = []
    current = start
    # Small epsilon avoids missing the final value due to floating-point roundoff.
    while current <= stop + 1e-9:
        angles.append(round(current, 10))
        current += step
    return angles


def prompt_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Enter a numeric value.")


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    mode = "a" if args.append else "w"
    write_header = not args.append or not output_path.exists() or output_path.stat().st_size == 0

    angles = angle_sequence(args.start_deg, args.stop_deg, args.step_deg)

    print("Manual torque-vs-angle logging")
    print("Use signed force in newtons. Positive force is the defined forward-torque direction.")
    print("Press Ctrl+C to stop early; completed rows remain written to disk.")
    print(f"Output: {output_path}")

    with output_path.open(mode, newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()

        try:
            for angle_deg in angles:
                print(f"\nSet rotor angle to {angle_deg:.3f} degrees and let the force reading settle.")
                force_n = prompt_float("Force/load-cell reading [N]: ")
                notes = input("Notes for this angle (optional): ").strip()
                torque_nm = force_n * args.lever_arm_m
                row = {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "angle_deg": angle_deg,
                    "force_n": force_n,
                    "lever_arm_m": args.lever_arm_m,
                    "torque_nm": torque_nm,
                    "air_gap_mm": args.air_gap_mm,
                    "magnet_configuration": args.magnet_configuration,
                    "calibration_id": args.calibration_id,
                    "operator": args.operator,
                    "notes": notes,
                }
                writer.writerow(row)
                csv_file.flush()
                print(f"Recorded torque: {torque_nm:.9g} N*m")
        except KeyboardInterrupt:
            print("\nLogging stopped by operator.")


if __name__ == "__main__":
    main()
