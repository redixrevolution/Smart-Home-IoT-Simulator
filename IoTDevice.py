from typing import Literal


class Status:
    """
    Interface class representing the status of a device
    """
    ON = "on"
    OFF = "off"


class IoTDevice:
    def __init__(self, device_id: str, status: Literal['on', 'off']):
        """
        - device_id: str -> The unique identifier of the device
        - status: Status.ON | Status.OFF -> Whether the device is switched on or off
        """
        self.device_id = device_id
        self.status = status or Status.OFF

    def turn_on(self) -> None:
        """ 
        Turn the device on
        """
        self.status = Status.ON

    def turn_off(self) -> None:
        """
        Turn the device off
        """
        self.status = Status.OFF

    def toggle_on_off(self) -> None:
        """
        Toggle the device between on and off
        """
        if self.status == Status.ON:
            self.status = Status.OFF
        elif self.status == Status.OFF:
            self.status = Status.ON

    def is_on(self) -> bool:
        """
        Check if a device is on
        """
        return self.status == Status.ON
    
    def __repr__(self):
        """ 
        Representation format of the IoTDevice (e.g. output when printed)
        """
        return f"{self.device_id}"

