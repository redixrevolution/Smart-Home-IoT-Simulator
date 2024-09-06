import time
import threading
import random
import tkinter as tk
from AutomationSystem import AutomationSystem, SmartLight, Thermostat, SecurityCamera


class Colors:
    """
    Class to hold custom color constants
    """

    def rgb_to_hex(r: int, g: int, b: int):
        """Converts RGB to hexadecimal color string"""
        return f"#{r:02x}{g:02x}{b:02x}"

    GRAY = rgb_to_hex(182, 182, 182)
    BLACK = rgb_to_hex(0, 0, 0)
    WHITE = rgb_to_hex(255, 255, 255)


class MonitoringDashboard:
    """
    GUI for monitoring and controlling the smart home system
    """

    def __init__(self, automation_system: AutomationSystem):
        self.root = tk.Tk()
        self.root.configure(bg=Colors.GRAY)
        self.root.title("Smart Home IoT Simulator")

        self.automation_system = automation_system
        self.device_labels = []
        self.scales = {}
        self.create_dashboard()

    def create_label(self, text: str):
        """Create a Label widget and set defaults for consistency"""
        return tk.Label(self.root, text=text, bg=Colors.GRAY, fg=Colors.BLACK)

    def create_button(self, text: str):
        """Create a Button widget and set defaults for consistency"""
        return tk.Button(self.root, text=text, bg=Colors.WHITE, fg=Colors.BLACK)

    def create_text(self, text=""):
        """Create a Text widget and set defaults for consistency"""
        textfield = tk.Text(
            self.root, width=50, height=8, bg=Colors.WHITE, fg=Colors.BLACK
        )
        textfield.insert(tk.END, text)
        textfield.config(state="disabled")
        return textfield

    def create_scale(self, range: tuple[float, float], command, default: float):
        """Create a Scale widget (slider) and set defaults for consistency"""
        scale = tk.Scale(
            self.root,
            from_=range[0],
            to=range[1],
            orient=tk.HORIZONTAL,
            bg=Colors.GRAY,
            troughcolor=Colors.WHITE,
            variable=tk.IntVar(value=default),
        )
        scale.bind("<ButtonRelease-1>", lambda e: command(scale.get()))
        return scale

    def create_dashboard(self):
        """
        Setup the GUI elements on the monitoring dashboard
        """
        btn_toggle_automation = self.create_button("Toggle Automation ON/OFF")
        btn_toggle_automation.config(command=self.toggle_automation)
        btn_toggle_automation.pack()

        _status = f"Automation Status: {self.automation_system.status}"
        self.lbl_automation_status = self.create_label(_status)
        self.lbl_automation_status.config(font=("Arial", 14))
        self.lbl_automation_status.pack()

        self.entry_devices_status = self.create_text(self.get_all_devices_status())
        self.entry_devices_status.pack(pady=(0, 8))

        for index, device in enumerate(self.automation_system.devices):
            if isinstance(device, SmartLight):
                label1 = self.create_label(f"{device} Brightness")
                middle = self.create_scale(
                    range=(0, 100),
                    command=lambda value, index=index: self.update_value(index, value),
                    default=device.brightness,
                )
                self.scales[index] = middle
            elif isinstance(device, Thermostat):
                label1 = self.create_label(f"{device} Temperature")
                middle = self.create_scale(
                    range=(0, 50),
                    command=lambda value, index=index: self.update_value(index, value),
                    default=device.temperature,
                )
                self.scales[index] = middle
            elif isinstance(device, SecurityCamera):
                label1 = self.create_label(f"{device} Motion Detection")
                middle = self.create_button("Random Detect Motion")
                middle.config(
                    command=lambda index=index: self.update_value(
                        index, value=random.choice(["MotionDetected", "NoMotion"])
                    )
                )

            toggle_btn = self.create_button("Toggle ON/OFF")
            toggle_btn.config(command=lambda i=index: self.toggle_device_on_off(i))
            label2 = self.create_label(device.get_label())

            label1.pack()
            middle.pack()
            toggle_btn.pack()
            label2.pack(pady=(0, 4))

            self.device_labels.append(label2)

        _rule = "Automation Rule: Turn on lights when motion is detected"
        lbl_automation_rule = self.create_label(_rule)
        lbl_automation_rule.pack(pady=(8, 8))

        lbl_events = self.create_label("Brightness Events")
        lbl_events.pack()

        self.entry_events = self.create_text()
        self.entry_events.config(width=75)
        self.entry_events.pack()

    def toggle_automation(self):
        """Toggle the automation status on the dashboard"""
        status = self.automation_system.toggle_automation_status()
        self.lbl_automation_status.config(text=f"Automation Status: {status}")

    def get_all_devices_status(self) -> str:
        """Get the status (On/Off) of every device in the system as a string"""
        return "\n".join(
            device.get_status() for device in self.automation_system.devices
        )

    def update_value(self, index: int, value=0):
        """
        Update the property value of a device, update the GUI
        and log the value in a file
        """
        device = self.automation_system.devices[index]

        if isinstance(device, SmartLight):
            self.automation_system.devices[index].set_brightness(value)
            # update brightness  events Text field
            self.entry_events.config(state="normal")
            log = self.automation_system.get_timestamped_log(
                f"{device} brightness set to {device.brightness}%"
            )
            self.entry_events.insert(tk.END, log)
            self.entry_events.config(state="disabled")
        elif isinstance(device, Thermostat):
            self.automation_system.devices[index].set_temperature(value)
        elif isinstance(device, SecurityCamera):
            self.automation_system.devices[index].set_security_status(value)

        self.automation_system.log_sensor_data(index)  # store data in file
        self.device_labels[index].config(text=device.get_label())  # update GUI

    def toggle_device_on_off(self, index: int):
        """Toggle a device between On and Off"""
        self.automation_system.devices[index].toggle_on_off()

        self.entry_devices_status.config(state="normal")
        self.entry_devices_status.replace("1.0", tk.END, self.get_all_devices_status())
        self.entry_devices_status.config(state="disabled")

    def update_gui_state(self):
        """
        Change the GUI to reflect the automatically updated device states and properties
        """
        for index, device in enumerate(self.automation_system.devices):
            # update GUI labels
            self.device_labels[index].config(text=device.get_label())

            if isinstance(device, SmartLight):
                self.scales[index].config(variable=tk.IntVar(value=device.brightness))
                # update brightness events Text field
                self.entry_events.config(state="normal")
                log = self.automation_system.get_timestamped_log(
                    f"{device} brightness set to {device.brightness}%"
                )
                self.entry_events.insert(tk.END, log)
                self.entry_events.config(state="disabled")
            elif isinstance(device, Thermostat):
                self.scales[index].config(variable=tk.IntVar(value=device.temperature))

            self.entry_devices_status.config(state="normal")
            self.entry_devices_status.replace("1.0", tk.END, self.get_all_devices_status())
            self.entry_devices_status.config(state="disabled")

    def run_automation_loop(self):
        """
        Loop that runs periodically to trigger automation rules and
        update device and GUI states
        """
        while True:
            if self.automation_system.status != "ON":
                time.sleep(1)
                continue

            if not self.root:  # exit when the user quits
                break

            # update device states every 3 seconds
            self.root.after(3000, self.automation_system.update_device_states)
            # trigger automation rules every 4 seconds
            self.root.after(2000, self.automation_system.trigger_automation_rules)

            self.root.after(2000, self.update_gui_state)
            time.sleep(4)

    def start(self):
        """
        Start the monitoring dashboard and automation loop
        """
        automation_loop = threading.Thread(target=self.run_automation_loop)
        automation_loop.start()

        self.root.mainloop()
        self.root = None
