"""Build a driver from a device type string."""

from collections.abc import Callable
from typing import Any

from device.base import Driver
from device.mock.pump import MockPumpDriver

_FACTORIES: dict[str, Callable[..., Driver]] = {
    "mock_pump": MockPumpDriver,
}


def create_driver(device_type: str, **options: Any) -> Driver:
    """Return a driver for ``device_type``.

    This phase only knows ``mock_pump``. GPIO and Modbus are not registered.
    ``options`` are passed to the driver constructor (for example a fake clock).
    """

    try:
        factory = _FACTORIES[device_type]
    except KeyError:
        known = ", ".join(sorted(_FACTORIES))
        raise ValueError(
            f"Unknown device_type {device_type!r}. Known types: {known}."
        ) from None
    return factory(**options)
