from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5 import QtCore
from UI.timetable_screen import Ui_MainWindow
from typing import List
from Schedules import Schedules


class TimeWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.read_timetable = []
        self.map_timetable()

    def update_from_csv(self, schedules: List[Schedules]):
        self.read_timetable = schedules

    def map_timetable(self):
        for x in range(24):
            for y in range(7):
                empty_label = QLabel('')
                empty_label.setAlignment(QtCore.Qt.AlignCenter)
                empty_label.setStyleSheet("border: 1px solid black;")
                self.timetable_sandbox.addWidget(empty_label, x, y)

        # dimension analyzer (Remove in future commits)
        # btn = QLabel('MAT137', self)
        # btn.setStyleSheet("background-color: lightgreen")
        # btn.resize(802/8, (625/25)*2.75)
        # btn.move((802/8)*6, 23 + (625/25) * 6)
