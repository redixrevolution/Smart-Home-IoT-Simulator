from typing import Literal
from IoTDevice import IoTDevice


class SmartLight(IoTDevice):
    """
    Smart Light simulator, an extension of IoT Device
    """

    def __init__(
        self, device_id: str, status: Literal["on", "off"] = "off", brightness: int = 0
    ):
        super().__init__(device_id, status)
        self.brightness = int(brightness)

    def set_brightness(self, brightness: int):
        """
        Sets the brightness of the smart light to the provided level
        - brightness: integer between 0 and 100 (inclusive)
        """
        self.brightness = int(brightness)

    def get_status(self):
        return f"SmartLight Status: {self.status.title()}"

    def get_label(self):
        """ Get label info in the format '<device_id> - <brightness>%' """
        return f"{self} - {self.brightness}%"
