import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5 import QtCore
import UI.Functionalities.navigation as nav
from UI.Layouts.timetable_screen import Ui_MainWindow
from Schedules import Schedules


def close_application():
    sys.exit()


class TimeWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, timetable, current_tz, target_tz, is_editable):
        super().__init__()
        self.setupUi(self)
        self.read_timetable = timetable

        if not is_editable:
            self.current_tz = current_tz
            self.target_tz = target_tz
            self.menuhi.setTitle('')
            self.menuSave.setTitle('Navigate')
            self.actionDelete_Schedule.setVisible(False)
            self.actionAdd_Schedule.setVisible(False)
            self.actionLoad_Schedule.setVisible(False)
            self.actionSave_and_Exit.setText('Exit')
            self.actionSave_and_Return.setText('Return')

            self.actionSave_and_Exit.setShortcut('Ctrl+W')
            self.actionSave_and_Exit.triggered.connect(close_application)

            self.actionSave_and_Return.setShortcut('Ctrl+B')
            self.actionSave_and_Return.triggered.connect(self.home_application)

            shifted_timetable = []
            for schedule in self.read_timetable:
                shifted_timetable += schedule.shift_schedules(self.current_tz, self.target_tz)

            self.read_timetable = shifted_timetable
            self.map_timetable()

        else:
            self.empty_layout()
            self.actionLoad_Schedule.triggered.connect(self.map_timetable)

    def empty_layout(self) -> None:
        """Create an empty timetable window

        :return: None
        """
        for x in range(24):
            for y in range(7):
                empty_label = QLabel('')
                empty_label.setAlignment(QtCore.Qt.AlignCenter)
                empty_label.setStyleSheet("border: 1px solid black;")
                self.timetable_sandbox.addWidget(empty_label, x, y)

    def map_timetable(self) -> None:
        """Plots the Schedules appropriately on the TimeWindow

        :return: None
        """
        self.empty_layout()

        if self.read_timetable is not None:
            for schedule in self.read_timetable:
                self.map_schedule(schedule)

    def map_schedule(self, schedule: Schedules) -> None:
        """Takes in a specific schedule and places it on the TimeWindow

        :param schedule: the schedule to be placed
        :return: None
        """
        graphed_schedule = QLabel(schedule.name + '\n'
                                  + str(schedule.start_time)[:5] + '-'
                                  + str(schedule.end_time)[:5], self)
        graphed_schedule.setFont(QFont('Arial', 10))
        graphed_schedule.setAlignment(QtCore.Qt.AlignCenter)
        graphed_schedule.setStyleSheet('background-color: rgb{}'.format(str(schedule.color)))
        duration = (schedule.end_time.hour * 60 + schedule.end_time.minute
                    - schedule.start_time.hour * 60 - schedule.start_time.minute) / 60

        graphed_schedule.resize(802 / 8, (625 / 25) * duration)

        start_loc = (schedule.start_time.hour * 60 + schedule.start_time.minute) / 60
        graphed_schedule.move((802 / 8) * (schedule.day + 1), 48 + (625 / 25) * start_loc)
        graphed_schedule.show()

    def home_application(self):
        """Navigate to home

        :return: None
        """
        nav.navigator.rotate(self, nav.navigator.temporary_win)


