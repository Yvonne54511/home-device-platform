"""Driver contract shared by mock, GPIO, and Modbus implementations."""

from abc import ABC, abstractmethod

from device.types import Command, TelemetryReading


class Driver(ABC):
    """Base type for a device driver.

    Callers only read telemetry and apply commands. They do not care whether
    the object talks to a simulation, GPIO, or Modbus.
    """

    @abstractmethod
    def read_telemetry(self) -> TelemetryReading:
        """Return the current sensors and motor state."""

    @abstractmethod
    def apply_command(self, command: Command) -> None:
        """Apply one command. For a pump, this sets the motor."""
