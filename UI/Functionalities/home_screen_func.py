import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from UI.Layouts.home_screen import Ui_MainWindow
import UI.Functionalities.navigation as nav
from UI.Functionalities.timetable_screen_func import TimeWindow
from UI.Layouts.load_error import Ui_Dialog
from Schedules import Schedules
from Managers.StorageManager import read_csv
from Managers.TimeZoneManager import all_timezones


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.gui_time = None

        self.current_tz_drop_down.addItems(all_timezones)
        self.target_tz_drop_down.addItems(all_timezones)

        self.convert.clicked.connect(self.open_next)

    def open_next(self) -> None:
        """Open timetable window, or give warning dialog if no
         csv data exists

        :return: None
        """
        Schedules.clear_used()
        read_timetable = read_csv()

        current_tz = str(self.current_tz_drop_down.currentText())
        target_tz = str(self.target_tz_drop_down.currentText())
        self.gui_time = TimeWindow(read_timetable, current_tz, target_tz, False)

        if not read_timetable:
            warn_dialog = WarnDialog()
            warn_dialog.exec_()
        else:
            self.gui_time.setFixedSize(self.gui_time.size())
            nav.navigator.rotate(self, self.gui_time)


class WarnDialog(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


app = QApplication(sys.argv)
gui_home = Window()
nav.start_application(app, gui_home)
