import sys
from PyQt5.QtWidgets import QApplication

from src.local_interface.mainwindow import ThermostatWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ThermostatWindow()
    rec = QApplication.desktop().screenGeometry()
    if rec.width() < 600:
        window.showFullScreen()
    else:
        window.show()
    sys.exit(app.exec_())


