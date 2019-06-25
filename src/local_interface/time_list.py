from PyQt5.QtWidgets import QVBoxLayout

from src.local_interface.time_element import TimeElement


class TimeList(QVBoxLayout):
    def __init__(self):
        self.time_slot_list = [TimeElement()]

    def update_list_dsiplay(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)


    def duplicate_time_splot(self, index: int):
        new = TimeElement()
        old = self.time_slot_list[index]
        new.temp_selection.setValue(old.temp_selection.value())
        new.time_selection.setValue(old.time_selection.value())
        self.time_slot_list.insert(index, new)
        self.reconnect_plus_minus()

    def remove_time_slot(self, index):
        self.time_slot_list.pop(index)
        self.reconnect_plus_minus()

    def reconnect_plus_minus(self):
        for i, t in enumerate(self.time_slot_list):
            t.pb_plus.disconnect()
            t.pb_minus.disconnect()
            t.pb_plus.clicked.connect(lambda: self.duplicate_time_splot(i))





