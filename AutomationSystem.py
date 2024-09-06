import random
from datetime import datetime
from SmartLight import SmartLight
from Thermostat import Thermostat
from SecurityCamera import SecurityCamera


class AutomationSystem:
    """
    A central automation system,  responsible for managing and controlling all devices
    """

    def __init__(self, status="OFF"):
        self.devices = []
        self.status = status

    def toggle_automation_status(self) -> str:
        """
        Toggle the automation status between 'ON' and 'OFF'
        and return the status
        """
        if self.status == "ON":
            self.status = "OFF"
        elif self.status == "OFF":
            self.status = "ON"

        return self.status

    def discover_devices(self):
        """
        Simulate discovering devices and adding them to the system
        """
        light = SmartLight(
            device_id="Living Room Light",
            brightness=random.randint(1, 100),
            status="on",
        )  # discover light, set random brightness
        thermostat = Thermostat(
            device_id="Living Room Thermostat",
            temperature=random.randint(10, 30), # range between 10 and 30°C
            status="on",
        )  # discover thermostat, set random temperature
        camera = SecurityCamera(
            device_id="Front Door Camera",
            security_status=random.choice(["MotionDetected", "NoMotion"]),
            status="on",
        )  # discover security camera

        self.devices.extend(
            [light, thermostat, camera]
        )  # add the devices to the system

    def trigger_automation_rules(self):
        """
        Simulate automation tasks, e.g., activating lights when motion is detected
        """
        for device in self.devices:
            if (
                isinstance(device, SecurityCamera)
                and device.is_on()
                and device.motion_detected()
            ):
                # Activate lights when motion is detected
                for index, light in enumerate(self.devices):
                    if isinstance(light, SmartLight):
                        light.turn_on()
                        light.set_brightness(100)
                        self.log_sensor_data(index)

    def log_sensor_data(self, index: int):
        """
        Log the sensor data of a device in a file
        - index: int, the index of the device in the system
        """
        with open("sensor_data.txt", "a") as file:
            device = self.devices[index]

            if isinstance(device, SmartLight):
                log = self.get_timestamped_log(
                    f"{device} brightness set to {device.brightness}%"
                )
                file.write(log)
            elif isinstance(device, Thermostat):
                log = self.get_timestamped_log(
                    f"{device} temperature set to {device.temperature}°C"
                )
                file.write(log)
            elif isinstance(device, SecurityCamera):
                log = self.get_timestamped_log(
                    f"{device} security status set to {device.security_status}"
                )
                file.write(log)

    def update_device_states(self):
        """
        Randomization mechanism to simulate changing device states
        and properties over time
        """
        if self.status != "ON":
            return
        
        # choose two random devices to update
        # devices = random.choice(self.devices)

        for index, device in enumerate(self.devices):
            if isinstance(device, SmartLight):
                device.set_brightness(random.randint(10, 80)) # 10 - 80% brightness
            elif isinstance(device, Thermostat):
                device.set_temperature(random.randint(20, 30)) # range between 20 and 30°C
            elif isinstance(device, SecurityCamera):
                device.set_security_status(
                    random.choice(["MotionDetected", "NoMotion"])
                )
            self.log_sensor_data(index)

    def gather_sensor_data(self):
        """
        Gather sensor data from all devices in the system and store it in a file
        """
        for index, device in enumerate(self.devices):
            self.log_sensor_data(index)

    def get_timestamped_log(self, text: str, end="\n") -> str:
        """
        Get timestamped log information, in a properly formatted manner
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = "[%s] %s%s" % (timestamp, text, end)
        return log
