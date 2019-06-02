from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot, QTimer
import time

from src.core.thermostat import Thermostat
from ui.ui_main_window import Ui_MainWindow
from src.web_interface.web_interface import WebThermostat


class ThermostatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # setup thermostat
        self.thermostat = Thermostat()
        self.thermostat.tick_event.connect(self.update_from_arduino)
        self.thermostat.target_temperature_changed.connect(self.update_from_arduino)
        self.thermostat.start()
        self.on_termostat_status_changed()
        # setup clock
        self.clock_timer = QTimer()
        self.clock_timer.setSingleShot(False)
        self.clock_timer.setInterval(1000)
        self.update_clock()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start()
        # setup web interface
        self.web = WebThermostat(self.thermostat)
        self.web.start()
        # connections
        self.ui.pb_up.pressed.connect(self.on_up_target_button_clicked)
        self.ui.pb_down.pressed.connect(self.on_down_target_button_clicked)
        self.ui.pb_ac.clicked.connect(self.on_ac_boutton_clicked)
        self.ui.pb_off.clicked.connect(self.on_off_button_clicked)
        self.ui.pb_heat.clicked.connect(self.on_heat_button_clicked)
        self.thermostat.mode_changed.connect(self.on_termostat_status_changed)

    @pyqtSlot(int)
    def update_temp_display(self, value: int):
        self.ui.lb_temp.setText("{}°C".format(value))

    @pyqtSlot(int)
    def update_humidity_display(self, value: int):
        self.ui.lb_humidity.setText("{:02d}%".format(value))

    @pyqtSlot(int)
    def update_target_temp_display(self, value: int):
        self.ui.lb_temp_target.setText("{}°C".format(value))

    def update_status_icons(self, fan_status: bool, ac_status: bool, heat_status: bool):
        self.ui.lb_status_ac.setVisible(ac_status)
        self.ui.lb_status_hot.setVisible(heat_status)
        self.ui.lb_status_vent.setVisible(fan_status)

    @pyqtSlot()
    def update_from_arduino(self):
        self.update_temp_display(int(self.thermostat.last_temperature))
        self.update_humidity_display(int(self.thermostat.last_humidity))
        self.update_target_temp_display(int(self.thermostat.temperature_target))
        self.update_status_icons(self.thermostat.last_fan_enabled,
                                 self.thermostat.last_ac_enabled,
                                 self.thermostat.last_heat_enabled)

    def on_up_target_button_clicked(self):
        t = self.thermostat.temperature_target
        self.thermostat.set_temperature_target(t + 1.0)

    def on_down_target_button_clicked(self):
        t = self.thermostat.temperature_target
        self.thermostat.set_temperature_target(t - 1.0)

    def on_ac_boutton_clicked(self):
        self.update_termostat_status("ac")

    def on_heat_button_clicked(self):
        self.update_termostat_status("heat")

    def on_off_button_clicked(self):
        self.update_termostat_status("off")

    def update_termostat_status(self, mode: str):
        assert mode in ["ac", "off", "heat"]
        self.thermostat.set_mode(mode)

    def on_termostat_status_changed(self):
        mode = self.thermostat.mode
        self.ui.pb_ac.setChecked(mode == "ac")
        self.ui.pb_off.setChecked(mode == "off")
        self.ui.pb_heat.setChecked(mode == "heat")

    @pyqtSlot()
    def update_clock(self):
        time_string = time.strftime("%A %d %B %H:%M:%S")
        # time_string = time.strftime("%c")
        self.ui.lb_time.setText(time_string)


