import sys

from PyQt5.QtWidgets import QDialog

from UI.Layouts.load_error import Ui_Dialog

"""
bridge.py is a script that contains all functionalities that are common to the home window and the time windows.
This includes the navigator class to go back and forth windows, and the common Load error warning dialog.
"""


class navigator:
    temporary_win = None

    @classmethod
    def rotate(cls, current_win: object, destination_win: object) -> None:
        """Rotate windows in order to simulate a 'go back' navigation

        :param current_win: current window
        :param destination_win: previous window
        :return: None
        """
        cls.temporary_win = current_win
        current_win.close()
        destination_win.show()


def start_application(application_starter: object, start_win: object) -> None:
    """Starting the ctztt application

    :param application_starter: the QApplication that is to be started
    :param start_win: The home window to be shown
    :return: None
    """
    start_win.show()
    sys.exit(application_starter.exec_())


class WarnDialog(QDialog, Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
