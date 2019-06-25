from PyQt5.QtWidgets import QPushButton, QSpinBox, QTimeEdit, QWidget, QHBoxLayout

from src.local_interface.time_list import TimeList


class TimeElement(QHBoxLayout):
    def __init__(self, time_list: TimeList, index=-1):
        self.parent_time_list = time_list
        self.current_index = index

        # setup UI
        self.time_selection = QTimeEdit()
        self.temp_selection = QSpinBox()
        self.pb_minus = QPushButton()
        self.pb_plus = QPushButton()
        height = 40
        # set max height
        self.time_selection.setMaximumHeight(height)
        self.temp_selection.setMaximumHeight(height)
        self.pb_minus.setMaximumHeight(height)
        self.pb_plus.setMaximumHeight(height)
        # set min height
        self.time_selection.setMinimumHeight(height)
        self.temp_selection.setMinimumHeight(height)
        self.pb_minus.setMinimumHeight(height)
        self.pb_plus.setMinimumHeight(height)
        # set pb width
        self.pb_minus.setMaximumWidth(height)
        self.pb_plus.setMaximumWidth(height)
        # add elements
        self.addWidget(self.time_selection)
        self.addWidget(self.temp_selection)
        self.addWidget(self.pb_plus)
        self.addWidget(self.pb_minus)



