from typing import Literal
from IoTDevice import IoTDevice


class SecurityCamera(IoTDevice):
    """
    Security Camera simulator, an extension of IoT Device
    """

    def __init__(
        self,
        device_id: str,
        status: Literal["on", "off"] = "off",
        security_status: str = "NoMotion",
    ):
        super().__init__(device_id, status)
        self.security_status = security_status

    def set_security_status(
        self, security_status: Literal["MotionDetected", "NoMotion"]
    ):
        """
        Set security status to either "MotionDetected" or "NoMotion"
        """
        self.security_status = security_status

    def get_status(self):
        return f"SecurityCamera Status: {self.status.title()}"

    def get_label(self):
        """Get label info in the format '<device_id> - Motion: <YES|NO>'"""
        _motion = "YES" if self.motion_detected() else "NO"
        return f"{self} - Motion: {_motion}"

    def motion_detected(self):
        """
        Check if the security camera has detected some motion
        """
        return self.security_status == "MotionDetected"
