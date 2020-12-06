import sys
from typing import List
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI.Layouts.home_screen import Ui_MainWindow
import UI.Functionalities.bridge as nav
from UI.Functionalities.timetable_screen_func import ReadOnlyTimeWindow, EditableTimeWindow
from Schedules import Schedules
from Managers.StorageManager import read_csv
from Managers.TimeZoneManager import all_timezones


def clear_and_read() -> List[object]:
    """Every time a click event for either converting or creating is registered,
        The previous list of schedules need to be removed and new ones to be read.

    :return: list of new scheduled
    """
    Schedules.clear_used()
    return read_csv()


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.gui_time = None

        self.current_tz_drop_down.addItems(all_timezones)
        self.target_tz_drop_down.addItems(all_timezones)

        self.convert.clicked.connect(self.open_next_ro)
        self.create.clicked.connect(self.open_next_w)

    def open_next_ro(self) -> None:
        """Open timetable window (read-only), or give warning dialog if no
         csv data exists

        :return: None
        """
        read_timetable = clear_and_read()

        current_tz = str(self.current_tz_drop_down.currentText())
        target_tz = str(self.target_tz_drop_down.currentText())
        self.gui_time = ReadOnlyTimeWindow(read_timetable, current_tz, target_tz)

        if not read_timetable:
            warn_dialog = nav.WarnDialog()
            warn_dialog.exec_()
        else:
            self.gui_time.setFixedSize(self.gui_time.size())
            nav.navigator.rotate(self, self.gui_time)

    def open_next_w(self) -> None:
        """Open timetable window (write)

        :return: None
        """
        read_timetable = clear_and_read()

        self.gui_time = EditableTimeWindow(read_timetable)
        self.gui_time.setFixedSize(self.gui_time.size())
        nav.navigator.rotate(self, self.gui_time)


app = QApplication(sys.argv)
gui_home = Window()
nav.start_application(app, gui_home)
