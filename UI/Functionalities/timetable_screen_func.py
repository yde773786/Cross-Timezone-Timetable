import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QAction, QMenu, QDialog
from PyQt5 import QtCore
import UI.Functionalities.bridge as nav
from UI.Layouts.timetable_screen import Ui_MainWindow
from UI.Layouts.add_timetable_dialog import Ui_Dialog
from Schedules import Schedules


def close_application():
    sys.exit()


class AddSchedule(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class TimeWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, timetable):
        super().__init__()
        self.setupUi(self)
        self.read_timetable = timetable

        navigate = self.create_menu_button('Navigate')
        navigate.addAction(self.create_menu_functionality('Go Back', 'Ctrl+B', self.home_application))

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

    def create_menu_button(self, menu_button_msg: str) -> QMenu:
        """Adds a menu button of the name given by menu_button_msg that will be displayed on the menu

        :return: new QMenu
        """
        return self.menubar.addMenu('&' + menu_button_msg)

    def create_menu_functionality(self, action_msg: str, short_cut: str, function_connect) -> QAction:
        """Assigns a function to a new QAction with a name provided by action_msg and corresponding shortcut

        :return: QAction required
        """
        functionality = QAction(action_msg, self)
        functionality.setShortcut(short_cut)
        functionality.triggered.connect(function_connect)

        return functionality

    def home_application(self):
        """Navigate to home

        :return: None
        """
        nav.navigator.rotate(self, nav.navigator.temporary_win)


class ReadOnlyTimeWindow(TimeWindow):

    def __init__(self, timetable, current_tz, target_tz):
        super(ReadOnlyTimeWindow, self).__init__(timetable)
        self.current_tz = current_tz
        self.target_tz = target_tz

        self.map_timetable()

    def map_timetable(self) -> None:
        """Shifts timetable before mapping it

        :return: None
        """
        shifted_timetable = []
        for schedule in self.read_timetable:
            shifted_timetable += schedule.shift_schedules(self.current_tz, self.target_tz)

        self.read_timetable = shifted_timetable
        super(ReadOnlyTimeWindow, self).map_timetable()


class EditableTimeWindow(TimeWindow):

    def __init__(self, timetable):
        super(EditableTimeWindow, self).__init__(timetable)

        edit = self.create_menu_button('Edit Timetable')
        edit.addAction(self.create_menu_functionality('Add Schedule', 'Ctrl+A', self.add_schedule))
        edit.addAction(self.create_menu_functionality('Delete Schedule', 'Ctrl+D', self.remove_schedule))
        edit.addAction(self.create_menu_functionality('Edit saved timetable', 'Ctrl+L', self.map_timetable))

        self.empty_layout()

    def map_timetable(self) -> None:
        """maps as parent function does, but displays error dialog if
        there is no value in csv file.

        :return: None
        """
        if not self.read_timetable:
            warn_dialog = nav.WarnDialog()
            warn_dialog.exec_()
        else:
            super(EditableTimeWindow, self).map_timetable()

    def add_schedule(self):
        add_schedule = AddSchedule()
        add_schedule.exec_()

    def remove_schedule(self):
        pass
