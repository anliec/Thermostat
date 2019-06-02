from flask import Flask, render_template
from PyQt5.QtCore import pyqtSlot, QThread
import os

from src.core.thermostat import Thermostat


WEB_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(WEB_DIR_PATH, 'templates/')
print(TEMPLATE_PATH)

app = Flask(__name__, template_folder=TEMPLATE_PATH)
therm = None


class WebThermostat(QThread):
    def __init__(self, thermostat: Thermostat):
        super().__init__()
        global therm
        therm = thermostat

    def run(self) -> None:
        app.run(debug=False, host='0.0.0.0')


@app.route('/')
def index():
    return render_template("thermostat.html", temperature=therm.last_temperature, target=therm.temperature_target,
                           humidity=therm.last_humidity)


@app.route("/<device_name>/<action>")
def action(device_name, action):
    if device_name == "target":
        if action == "plus":
            therm.increment_target_temperature()
        elif action == "moins":
            therm.decrement_target_temperature()
    elif device_name == "status":
        if action == "off":
            therm.set_mode("off")
        if action == "ac":
            therm.set_mode("ac")
        if action == "heat":
            therm.set_mode("heat")

    return render_template("thermostat.html", temperature=therm.last_temperature, target=therm.temperature_target,
                           humidity=therm.last_humidity)


