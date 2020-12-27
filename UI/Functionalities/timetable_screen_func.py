import sys
from typing import List

from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QMainWindow, QLabel, QAction, QMenu, QDialog, QWidget, QCheckBox
from PyQt5 import QtCore, QtGui
import datetime
import UI.Functionalities.bridge as nav
from Managers.ColorManager import rotate_to_color
from UI.Layouts.timetable_screen import Ui_MainWindow
from UI.Layouts.add_schedule_dialog import Ui_Add_Dialog
from UI.Layouts.delete_schedule_dialog import Ui_Delete_Dialog
from Managers.TimeZoneManager import ALL_DAYS
from Managers.StorageManager import read_csv, write_csv
from Schedules import Schedules, ConflictingScheduleError, EndBeforeStartError

DRAWN_LABELS = []


def clear_canvas():
    for mapped in DRAWN_LABELS:
        mapped.close()


def close_application():
    sys.exit()


class AddSchedule(QDialog, Ui_Add_Dialog):

    def __init__(self, timetable: List[Schedules]):
        super().__init__()
        self.setup_ui(self)
        self.int_input = QIntValidator()

        self.day_week.addItems(ALL_DAYS)
        self.start_hour.setValidator(self.int_input)
        self.start_min.setValidator(self.int_input)
        self.end_hour.setValidator(self.int_input)
        self.end_min.setValidator(self.int_input)
        self.timetable = timetable
        self.button_box.accepted.connect(self.add_new)
        self.error_dialog.setStyleSheet('QLabel {color: #FF0000;}')

    def add_new(self) -> None:
        try:
            start_time = datetime.time(int(self.start_hour.text()),
                                       int(self.start_min.text()))

            end_time = datetime.time(int(self.end_hour.text()),
                                     int(self.end_min.text()))

            name = self.name_schedule.text()
            has_same_name = False
            color = ()

            for schedule in self.timetable:
                if schedule.name == name:
                    color = schedule.color
                    has_same_name = True
                    break

            if has_same_name:
                insert = Schedules(name,
                                   ALL_DAYS[self.day_week.currentText()],
                                   start_time, end_time, False, color)
            else:
                insert = Schedules(name,
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


class DeleteSchedule(QDialog, Ui_Delete_Dialog):

    def __init__(self, timetable: List[Schedules]):
        super().__init__()
        self.setup_ui(self)

        self.timetable = timetable
        self.delete_schedule = {}
        self.generate_delete_options()
        self.button_box.accepted.connect(self.delete_checked)

    def generate_delete_options(self) -> None:

        day_index = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        for schedule in self.timetable:
            check_text = schedule.name + ': ' + day_index[schedule.day] + ', ' \
                         + str(schedule.start_time)[:-3] + ' to ' \
                         + str(schedule.end_time)[:-3]

            self.delete_schedule[schedule] = QCheckBox(check_text)
            self.verticalLayout.addWidget(self.delete_schedule[schedule])

    def delete_checked(self) -> None:
        for schedule in self.delete_schedule:
            if self.delete_schedule[schedule].isChecked():
                self.timetable.remove(schedule)
                Schedules.clear_slot(schedule)

        self.close()


def create_menu_button(menu_button_msg: str, menu_bar: QWidget) -> QMenu:
    """Adds a menu button of the name given by menu_button_msg that will be
    displayed on the menu

    :return: new QMenu
    """
    return menu_bar.addMenu(' &' + menu_button_msg)


class TimeWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, timetable):
        super().__init__()
        self.setup_ui(self)
        self.read_timetable = timetable

        self.day_height = self.label_18.frameGeometry().height()

        self.menu_bar.setNativeMenuBar(False)

        navigate = create_menu_button('Navigate', self.menu_bar)
        navigate.addAction(self.create_menu_functionality('Go Back', 'Ctrl+B',
                                                          self.home_application))

    def map_timetable(self) -> None:
        """Plots the Schedules appropriately on the TimeWindow

        :return: None
        """

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
        graphed_schedule.setFont(QFont('Arial', 7))
        graphed_schedule.setAlignment(QtCore.Qt.AlignCenter)
        graphed_schedule.setStyleSheet('background-color: rgb{}'.format(str(schedule.color)))

        start_loc = (schedule.start_time.hour * 60 + schedule.start_time.minute) / 60
        end_loc = (schedule.end_time.hour * 60 + schedule.end_time.minute) / 60

        duration = (end_loc - start_loc)
        upper_border = self.day_height + self.menu_bar.frameGeometry().height() - 3
        unit_size = (self.TOTAL_HEIGHT - upper_border) / 24

        graphed_schedule.resize(self.TOTAL_WIDTH / 8, unit_size * duration)

        graphed_schedule.move((self.TOTAL_WIDTH / 8) * (schedule.day + 1), upper_border + unit_size
                              * start_loc)
        graphed_schedule.show()

        DRAWN_LABELS.append(graphed_schedule)

    def create_menu_functionality(self, action_msg: str, short_cut: str,
                                  function_connect) -> QAction:
        """Assigns a function to a new QAction with a name provided by action_msg
        and corresponding shortcut

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
        DRAWN_LABELS.clear()
        Schedules.clear_used()
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

    def __init__(self):
        super(EditableTimeWindow, self).__init__([])

        self.save_flag = True

        edit = create_menu_button('Edit Timetable', self.menu_bar)
        save = create_menu_button('Save Timetable', self.menu_bar)

        edit.addAction(self.create_menu_functionality('Add Schedule', 'Ctrl+A',
                                                      self.add_new_schedule))
        edit.addAction(self.create_menu_functionality('Delete Schedule', 'Ctrl+D',
                                                      self.remove_schedule))
        edit.addAction(self.create_menu_functionality('Edit saved timetable', 'Ctrl+L',
                                                      self.load_timetable))
        save.addAction(self.create_menu_functionality('Save Timetable', 'Ctrl+S',
                                                      self.save_timetable))

    def add_new_schedule(self):
        prev = self.read_timetable[:]
        add_schedule = AddSchedule(self.read_timetable)
        add_schedule.exec_()
        after = self.read_timetable[:]

        if prev != after:
            self.save_flag = False

        self.map_timetable()

    def remove_schedule(self):
        if not self.read_timetable:
            warn_dialog = nav.WarnDialog(nav.DELETE_WARNING)
            warn_dialog.exec_()
        else:
            prev = self.read_timetable[:]
            delete_schedule = DeleteSchedule(self.read_timetable)
            delete_schedule.exec_()
            after = self.read_timetable[:]

            if prev != after:
                self.save_flag = False

            clear_canvas()
            self.map_timetable()

    def load_timetable(self):
        prev_slots = Schedules.used_slot
        Schedules.clear_used()
        csv_timetable = read_csv()

        if csv_timetable:
            if self.read_timetable:
                warn_dialog = nav.WarnDialog(nav.DATA_LOSS_WARNING, add_choice_buttons=True)
                if warn_dialog.exec_():
                    self.read_timetable = csv_timetable
                    clear_canvas()
                    self.map_timetable()
                    rotate_to_color(self.read_timetable[-1].color)
                else:
                    Schedules.used_slot = prev_slots
            else:
                self.read_timetable = csv_timetable
                clear_canvas()
                self.map_timetable()
                rotate_to_color(self.read_timetable[-1].color)
        else:
            Schedules.used_slot = prev_slots
            warn_dialog = nav.WarnDialog(nav.LOAD_WARNING)
            warn_dialog.exec_()

    def save_timetable(self):
        self.save_flag = True
        write_csv(self.read_timetable)

    def home_application(self):
        if not self.save_flag:
            warn_dialog = nav.WarnDialog(nav.NOT_SAVED_WARNING, add_choice_buttons=True)
            if warn_dialog.exec_():
                super(EditableTimeWindow, self).home_application()
        else:
            super(EditableTimeWindow, self).home_application()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if not self.save_flag:
            warn_dialog = nav.WarnDialog(nav.NOT_SAVED_WARNING, add_choice_buttons=True)
            if warn_dialog.exec_():
                super(EditableTimeWindow, self).closeEvent(a0)
        else:
            super(EditableTimeWindow, self).closeEvent(a0)
