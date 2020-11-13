import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from UI.home_screen import Ui_MainWindow
from UI.timetable_screen_func import TimeWindow
from UI.load_error import Ui_Dialog
from Managers.StorageManager import read_csv
from Managers.TimeZoneManager import all_timezones


def open_dialog() -> None:
    """Pass csv data to timetable window, or give warning dialog if no
     such data exists

    :return: None
    """
    read_timetable = read_csv()
    if not read_timetable:
        warn_dialog = WarnDialog()
        warn_dialog.exec_()
    else:
        gui_time.update_from_csv(read_timetable)
        gui_home.hide()
        gui_time.setFixedSize(gui_time.size())
        gui_time.show()


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.current_tz_drop_down.addItems(all_timezones)
        self.target_tz_drop_down.addItems(all_timezones)

        self.convert.clicked.connect(open_dialog)


class WarnDialog(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


app = QApplication(sys.argv)
gui_home = Window()
gui_time = TimeWindow()
gui_home.show()
sys.exit(app.exec_())
