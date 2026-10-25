"""GPIO drivers are reserved for a later phase. Nothing here talks to hardware."""

from device.base import Driver
from device.types import Command, TelemetryReading


class GpioPumpDriver(Driver):
    """Placeholder for a Raspberry Pi float-switch and relay driver.

    The next phase will implement this. Calling either method raises
    ``NotImplementedError``.
    """

    def read_telemetry(self) -> TelemetryReading:
        raise NotImplementedError(
            "GPIO driver is planned for a later phase. Use MockPumpDriver."
        )

    def apply_command(self, command: Command) -> None:
        raise NotImplementedError(
            "GPIO driver is planned for a later phase. Use MockPumpDriver."
        )
