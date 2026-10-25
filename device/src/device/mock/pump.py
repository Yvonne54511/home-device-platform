"""Simulated sump pump: the tank fills on its own and empties while the motor runs."""

from collections.abc import Callable

from device.base import Driver
from device.types import Command, TelemetryReading

Clock = Callable[[], float]


class MockPumpDriver(Driver):
    """In-memory pump used until real hardware exists.

    Water rises at ``inflow_per_second`` while the motor is off.
    While the motor is on, outflow is ``pump_per_second`` (larger than inflow),
    so the level falls. Both rates are percent of a full tank per second.
    Time comes from ``clock`` (default: ``time.monotonic``), so a test can
    pass a fake clock instead of sleeping.
    """

    def __init__(
        self,
        *,
        level_percent: float = 40.0,
        low_threshold: float = 30.0,
        high_threshold: float = 70.0,
        inflow_per_second: float = 1.0,
        pump_per_second: float = 4.0,
        clock: Clock | None = None,
    ) -> None:
        if not 0.0 <= level_percent <= 100.0:
            raise ValueError("level_percent must be between 0 and 100")
        if not 0.0 <= low_threshold < high_threshold <= 100.0:
            raise ValueError("thresholds must satisfy 0 <= low < high <= 100")
        if inflow_per_second < 0.0:
            raise ValueError("inflow_per_second must be >= 0")
        if pump_per_second <= inflow_per_second:
            raise ValueError("pump_per_second must be greater than inflow_per_second")

        if clock is None:
            import time

            clock = time.monotonic

        self._level = level_percent
        self._low_threshold = low_threshold
        self._high_threshold = high_threshold
        self._inflow_per_second = inflow_per_second
        self._pump_per_second = pump_per_second
        self._clock = clock
        self._motor = False
        self._last_time = clock()

    def read_telemetry(self) -> TelemetryReading:
        self._advance(self._clock())
        return self._reading()

    def apply_command(self, command: Command) -> None:
        if not isinstance(command, Command):
            raise TypeError("command must be a Command")
        # Settle the level under the previous motor state, then switch.
        self._advance(self._clock())
        self._motor = command.motor

    def _advance(self, now: float) -> None:
        delta = now - self._last_time
        if delta < 0.0:
            raise ValueError("clock moved backwards")
        net_per_second = self._inflow_per_second
        if self._motor:
            net_per_second -= self._pump_per_second
        self._level = min(100.0, max(0.0, self._level + net_per_second * delta))
        self._last_time = now

    def _reading(self) -> TelemetryReading:
        return TelemetryReading(
            level_high=self._level >= self._high_threshold,
            level_low=self._level >= self._low_threshold,
            motor=self._motor,
            level_percent=self._level,
        )
