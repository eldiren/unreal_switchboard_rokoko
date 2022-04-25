import requests

from switchboard.devices.device_base import Device
from switchboard.switchboard_logging import LOGGER
from switchboard.devices.device_widget_base import AddDeviceDialog, DeviceWidget
from switchboard.config import IntSetting

from PySide2 import QtWidgets, QtGui, QtCore

class AddRokokoDeviceDialog(AddDeviceDialog):
    def __init__(self, existing_devices, parent=None):
        super().__init__(device_type="Rokoko", existing_devices=existing_devices, parent=parent)

        # Create QTWidgets to add to the form
        self.port_text_field = QtWidgets.QLineEdit(self)

        # Append the new options to the QTWidgets.QFormLayout object defined in the parent class
        self.form_layout.addRow("Port", self.port_text_field)

class DeviceRokoko(Device):
    add_device_dialog = AddRokokoDeviceDialog

    setting_rokoko_port = IntSetting(
        "rokoko_port", "Rokoko Port", 14053)
    
    def __init__(self, name, ip_address, **kwargs):
        super().__init__(name, ip_address, **kwargs)

        self._slate = 'slate'
        self._take = 1

    
    def record_start(self, slate, take, description):
        """
        Called by switchboard_dialog when recording was started, will start
        recording in Rokoko.
        """
        if self.is_disconnected or not self.trigger_start:
            return

        self.set_slate(slate)
        self.set_take(take)

        self.start_rokoko_record()

    def record_stop(self):
        """
        Called by switchboard_dialog when recording was stopped, will stop
        recording in Rokoko.
        """
        if self.is_disconnected or not self.trigger_stop:
            return

        self.stop_rokoko_record()

    def start_rokoko_record(self):
        LOGGER.warning(f"Started recording...")

    def stop_rokoko_record():
        LOGGER.warning("Stopped recording")


class DeviceWidgetRokoko(DeviceWidget):
    def __init__(self, name, device_hash, ip_address, icons, parent=None):
        super().__init__(name, device_hash, ip_address, icons, parent=parent)

