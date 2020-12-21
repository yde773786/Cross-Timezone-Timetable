import sys
from typing import List

from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QMainWindow, QLabel, QAction, QMenu, QDialog, QWidget
from PyQt5 import QtCore
import datetime
import UI.Functionalities.bridge as nav
from UI.Layouts.timetable_screen import Ui_MainWindow
from UI.Layouts.add_schedule_dialog import Ui_Dialog
from Managers.TimeZoneManager import ALL_DAYS
from Schedules import Schedules, ConflictingScheduleError, EndBeforeStartError


def close_application():
    sys.exit()


class AddSchedule(QDialog, Ui_Dialog):

    def __init__(self, timetable: List[Schedules]):
        super().__init__()
        self.setupUi(self)
        self.int_input = QIntValidator()

        self.day_week.addItems(ALL_DAYS)
        self.start_hour.setValidator(self.int_input)
        self.start_min.setValidator(self.int_input)
        self.end_hour.setValidator(self.int_input)
        self.end_min.setValidator(self.int_input)
        self.timetable = timetable
        self.buttonBox.accepted.connect(self.add_new)

    def add_new(self):
        try:
            start_time = datetime.time(int(self.start_hour.text()),
                                       int(self.start_min.text()))

            end_time = datetime.time(int(self.end_hour.text()),
                                       int(self.end_min.text()))

            insert = Schedules(self.name_schedule.text(),
                               ALL_DAYS[self.day_week.currentText()],
                               start_time, end_time, False)

            self.timetable.append(insert)
            self.close()

        except ValueError:
            self.error_dialog.setText('ERROR: Input is not a valid time as per '
                                      'a 24h schedule.')
        except ConflictingScheduleError:
            self.error_dialog.setText('ERROR: Input has scheduling conflicts with '
                                      'existing timetable.')
        except EndBeforeStartError:
            self.error_dialog.setText('ERROR: The end time cannot be before the start time.')


def create_menu_button(menu_button_msg: str, menu_bar: QWidget) -> QMenu:
    """Adds a menu button of the name given by menu_button_msg that will be
    displayed on the menu

    :return: new QMenu
    """
    return menu_bar.addMenu('&' + menu_button_msg)


class TimeWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, timetable):
        super().__init__()
        self.setupUi(self)
        self.read_timetable = timetable

        navigate = create_menu_button('Navigate', self.menubar)
        navigate.addAction(self.create_menu_functionality('Go Back', 'Ctrl+B',
                                                          self.home_application))

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

        edit = create_menu_button('Edit Timetable', self.menubar)

        edit.addAction(self.create_menu_functionality('Add Schedule', 'Ctrl+A', self.add_new_schedule))
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

    def add_new_schedule(self):
        add_schedule = AddSchedule(self.read_timetable)
        add_schedule.exec_()
        self.map_timetable()

    def add_schedule_existing(self):
        pass

    def remove_schedule(self):
        pass
