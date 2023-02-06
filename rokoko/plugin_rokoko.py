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
    
    def __init__(self, name, address, **kwargs):
        super().__init__(name, address, **kwargs)

        self._slate = 'slate'
        self._take = 1

    def set_slate(self, value):
        self._slate = value

    def set_take(self, value):
        self._take = value

    def record_start(self, slate, take, description):
        """
        Called by switchboard_dialog when recording was started, will start
        recording in Rokoko.
        """
        if self.is_disconnected or not self.is_recording_device:
            LOGGER.debug("Rokoko disconnected...")
            return

        try:
            self.set_slate(slate)
            self.set_take(take)
            cmd_url = f"http://{self.address}:{self.setting_rokoko_port.get_value()}/v1/1234/recording/start"
    
            res = requests.post(url = cmd_url, json = {'filename': f"slate_{self._slate}_take_{self._take}"})

            LOGGER.debug(res.json())
        except Exception as ex:
            LOGGER.debug(f"{type(ex).__name__} {ex.args}")

    def record_stop(self):
        """
        Called by switchboard_dialog when recording was stopped, will stop
        recording in Rokoko.
        """
        cmd_url = f"http://{self.address}:{self.setting_rokoko_port.get_value()}/v1/1234/recording/stop"

        res = requests.post(cmd_url)

        LOGGER.debug(res.json())


class DeviceWidgetRokoko(DeviceWidget):
    def __init__(self, name, device_hash, ip_address, icons, parent=None):
        super().__init__(name, device_hash, ip_address, icons, parent=parent)
    
    def _add_control_buttons(self):
        super()._add_control_buttons()

        self.connect_button = self.add_control_button(
            ':/icons/images/icon_connect.png',
            icon_hover=':/icons/images/icon_connect_hover.png',
            icon_disabled=':/icons/images/icon_connect_disabled.png',
            icon_on=':/icons/images/icon_connected.png',
            icon_hover_on=':/icons/images/icon_connected_hover.png',
            icon_disabled_on=':/icons/images/icon_connected_disabled.png',
            tool_tip='Connect/Disconnect from listener')

        self.connect_button.clicked.connect(self.connect_button_clicked)

    def connect_button_clicked(self):
        if self.connect_button.isChecked():
            self._connect()
        else:
            self._disconnect()

    def _connect(self):
        # Make sure the button is in the correct state
        self.connect_button.setChecked(True)

        # Emit Signal to Switchboard
        self.signal_device_widget_connect.emit(self)

    def _disconnect(self):
        # Make sure the button is in the correct state
        self.connect_button.setChecked(False)

        # Emit Signal to Switchboard
        self.signal_device_widget_disconnect.emit(self)
