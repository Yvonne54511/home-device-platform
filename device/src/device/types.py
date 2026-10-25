"""Shared values passed between drivers and the rest of the platform."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TelemetryReading:
    """One snapshot of pump sensors and the motor.

    ``level_percent`` is the simulated water level from 0 to 100.
    The two float switches are derived from that level:
    ``level_low`` is true when water covers the lower float,
    ``level_high`` is true when water covers the upper float.
    A healthy tank never reports high-without-low.
    """

    level_high: bool
    level_low: bool
    motor: bool
    level_percent: float


@dataclass(frozen=True)
class Command:
    """Ask a pump driver to turn the motor on or off."""

    motor: bool
