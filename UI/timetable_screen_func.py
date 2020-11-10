from PyQt5.QtWidgets import QMainWindow
from UI.timetable_screen import Ui_MainWindow


class TimeWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)