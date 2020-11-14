from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5 import QtCore
from UI.Layouts.timetable_screen import Ui_MainWindow
from Schedules import Schedules


class TimeWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, timetable, current_tz, target_tz):
        super().__init__()
        self.setupUi(self)
        self.read_timetable = timetable
        self.current_tz = current_tz
        self.target_tz = target_tz
        self.map_timetable()

    def map_timetable(self) -> None:
        """Plots the Schedules appropriately on the TimeWindow

        :return: None
        """
        for x in range(24):
            for y in range(7):
                empty_label = QLabel('')
                empty_label.setAlignment(QtCore.Qt.AlignCenter)
                empty_label.setStyleSheet("border: 1px solid black;")
                self.timetable_sandbox.addWidget(empty_label, x, y)

        shifted_timetable = []
        for schedule in self.read_timetable:
            shifted_timetable += schedule.shift_schedules(self.current_tz, self.target_tz)

        for schedule in shifted_timetable:
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

