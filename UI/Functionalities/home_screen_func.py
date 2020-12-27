import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI.Layouts.home_screen import Ui_MainWindow
import UI.Functionalities.bridge as nav
from UI.Functionalities.timetable_screen_func import ReadOnlyTimeWindow, EditableTimeWindow
from Schedules import Schedules
from Managers.StorageManager import read_csv
from Managers.TimeZoneManager import ALL_TIMEZONES


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setup_ui(self)
        self.gui_time = None

        self.current_tz_drop_down.addItems(ALL_TIMEZONES)
        self.target_tz_drop_down.addItems(ALL_TIMEZONES)

        self.convert.clicked.connect(self.open_next_ro)
        self.create.clicked.connect(self.open_next_w)

    def open_next_ro(self) -> None:
        """Open timetable window (read-only), or give warning dialog if no
         csv data exists

        :return: None
        """
        Schedules.clear_used()
        read_timetable = read_csv()

        current_tz = str(self.current_tz_drop_down.currentText())
        target_tz = str(self.target_tz_drop_down.currentText())
        self.gui_time = ReadOnlyTimeWindow(read_timetable, current_tz, target_tz)

        if not read_timetable:
            warn_dialog = nav.WarnDialog(nav.LOAD_WARNING)
            warn_dialog.exec_()
        else:
            self.gui_time.setFixedSize(self.gui_time.size())
            nav.navigator.rotate(self, self.gui_time)

    def open_next_w(self) -> None:
        """Open timetable window (write)

        :return: None
        """
        self.gui_time = EditableTimeWindow()
        self.gui_time.setFixedSize(self.gui_time.size())
        nav.navigator.rotate(self, self.gui_time)


def run() -> None:
    """Runs the application from home layout

    :return: None
    """
    app = QApplication(sys.argv)
    gui_home = Window()
    nav.start_application(app, gui_home)
