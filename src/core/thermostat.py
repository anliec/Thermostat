from PyQt5.QtCore import QTimer, pyqtSlot, QObject, pyqtSignal
import json

from src.core.serial_util import ArdiunoSerialInterface


class Thermostat(QObject):

    tick_event = pyqtSignal()
    target_temperature_changed = pyqtSignal()
    mode_changed = pyqtSignal()

    def __init__(self, temperature_target: float = 25, ms_update_interval: int = 2000, mode: str = "off",
                 skip_config_file: bool = False):
        super().__init__()
        self.arduino_com = ArdiunoSerialInterface()
        self.temperature_target = temperature_target
        self.last_temperature = temperature_target
        self.last_humidity = 0.0
        self.last_fan_enabled = False
        self.last_ac_enabled = False
        self.last_heat_enabled = False
        self.mode = "off"
        self.set_mode(mode)
        self.update_interval = ms_update_interval
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.setInterval(self.update_interval)
        self.timer.setSingleShot(False)
        self.config_file_path = "config.json"
        if not skip_config_file:
            self.load_config()
        # connections
        self.mode_changed.connect(self.save_config)
        self.target_temperature_changed.connect(self.save_config)

    @pyqtSlot()
    def save_config(self):
        config = {"temperature_target": self.temperature_target,
                  "mode": self.mode}
        with open(self.config_file_path, 'w') as f:
            json.dump(config, f)

    @pyqtSlot()
    def load_config(self):
        try:
            with open(self.config_file_path, 'r') as f:
                config = json.load(f)
            self.set_temperature_target(config["temperature_target"])
            self.set_mode(config["mode"])
        except FileNotFoundError:
            print("Unable to read config file: File Npt Found")
        except KeyError:
            print("config file is not correctly formatted")

    @pyqtSlot()
    def start(self):
        if not self.timer.isActive():
            self.tick()
            self.timer.start()

    @pyqtSlot()
    def tick(self):
        last_values = self.arduino_com.read_data()
        self.last_temperature = last_values["temperature"]
        self.last_humidity = last_values["humidity"]
        self.last_fan_enabled = last_values["relay1"] == 0 or last_values["relay2"] == 0
        self.last_ac_enabled = last_values["relay1"] == 0
        self.last_heat_enabled = last_values["relay2"] == 0
        self.update_status()
        self.tick_event.emit()

    @pyqtSlot()
    def update_status(self):
        if self.mode == "ac":
            if round(self.last_temperature) > round(self.temperature_target):
                self.arduino_com.write_relay1(True)
            elif round(self.last_temperature) < round(self.temperature_target):
                self.arduino_com.write_relay1(False)
            self.arduino_com.write_relay2(False)
        elif self.mode == "heat":
            if round(self.last_temperature) < round(self.temperature_target):
                self.arduino_com.write_relay2(True)
            elif round(self.last_temperature) > round(self.temperature_target):
                self.arduino_com.write_relay2(False)
            self.arduino_com.write_relay1(False)
        else:
            self.disable_all_relay()

    @pyqtSlot()
    def set_temperature_target(self, temperature_target: float):
        self.temperature_target = temperature_target
        self.update_status()
        self.target_temperature_changed.emit()

    @pyqtSlot()
    def increment_target_temperature(self):
        self.set_temperature_target(self.temperature_target + 1)

    @pyqtSlot()
    def decrement_target_temperature(self):
        self.set_temperature_target(self.temperature_target - 1)

    @pyqtSlot()
    def set_mode(self, mode: str):
        if mode not in ["ac", "off", "heat"]:
            raise ValueError("Expected state in {} but got {}".format(["ac", "off", "heat"], mode))
        self.mode = mode
        self.mode_changed.emit()
        if mode == "off":
            self.disable_all_relay()

    @pyqtSlot()
    def disable_all_relay(self):
        self.arduino_com.write_relay1(False)
        self.arduino_com.write_relay2(False)




