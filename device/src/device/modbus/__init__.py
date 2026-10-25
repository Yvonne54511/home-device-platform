"""Modbus drivers are reserved for a later phase. Nothing here opens a serial port."""

from device.base import Driver
from device.types import Command, TelemetryReading


class ModbusPumpDriver(Driver):
    """Placeholder for a Modbus RTU relay driver.

    A later phase will implement this. Calling either method raises
    ``NotImplementedError``.
    """

    def read_telemetry(self) -> TelemetryReading:
        raise NotImplementedError(
            "Modbus driver is planned for a later phase. Use MockPumpDriver."
        )

    def apply_command(self, command: Command) -> None:
        raise NotImplementedError(
            "Modbus driver is planned for a later phase. Use MockPumpDriver."
        )
