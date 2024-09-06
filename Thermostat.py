from typing import Literal
from IoTDevice import IoTDevice


class Thermostat(IoTDevice):
    """
    Thermostat simulator, an extension of IoT Device
    """

    def __init__(
        self,
        device_id: str,
        status: Literal["on", "off"] = "off",
        temperature: float = 0.0,
    ):
        super().__init__(device_id, status)
        self.temperature = float(temperature)

    def set_temperature(self, temperature: float):
        """
        Sets the temperature of the thermostat to the given temperature in °C
        - temperature: float between 0 to 100 (inclusive)
        """
        self.temperature = float(temperature)

    def get_status(self):
        return f"Thermostat Status: {self.status.title()}"

    def get_label(self):
        """Get label info in the format '<device_id> - <temperature>°C'"""
        return f"{self} - {self.temperature}°C"
