from AutomationSystem import AutomationSystem
from MonitoringDashboard import MonitoringDashboard


if __name__ == "__main__":
    # Create an instance of the AutomationSystem
    automation_system = AutomationSystem(status="ON")

    # Discover devices and execute automation tasks
    automation_system.discover_devices()
    automation_system.trigger_automation_rules()

    # Create and start the monitoring dashboard
    dashboard = MonitoringDashboard(automation_system)
    dashboard.start()
