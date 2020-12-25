import sys
from PyQt5.QtWidgets import QDialog
from UI.Layouts.load_error import Ui_Dialog

"""
bridge.py is a script that contains all functionalities that are common to the home window and the time windows.
This includes the navigator class to go back and forth windows, and the common Load error warning dialog.
"""

LOAD_WARNING = "There is no timetable that you have stored.\n " \
               "Please create one instead"

DELETE_WARNING = "There are no schedules to be deleted from timetable"

DATA_LOSS_WARNING = "The data on timetable being edited currently will be \n " \
                    "overwritten. Do you wish to continue?"

NOT_SAVED_WARNING = "Changes have been made to timetable that haven't been saved.\n "\
                    "will be lost. Do you wish to continue?"


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

    def __init__(self, message: str, add_choice_buttons=False):
        super().__init__()

        self.setupUi(self)
        self.approved = False
        self.label_2.setText(message)

        if not add_choice_buttons:
            self.buttonBox.close()
        self.buttonBox.accepted.connect(self.make_true)

    def make_true(self):
        self.approved = True
        self.close()

    def exec_(self) -> bool:
        super(WarnDialog, self).exec_()
        return self.approved
