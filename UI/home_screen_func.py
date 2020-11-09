import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI.home_screen import Ui_MainWindow
from Managers.TimeZoneManager import all_timezones


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.current_tz_drop_down.addItems(all_timezones)
        self.target_tz_drop_down.addItems(all_timezones)


app = QApplication(sys.argv)
Gui = Window()
Gui.show()
sys.exit(app.exec_())
