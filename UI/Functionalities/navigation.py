import sys


class navigator:
    temporary_win = None

    @classmethod
    def rotate(cls, current_win: object, destination_win: object):
        """Rotate windows in order to simulate a 'go back' navigation

        :param current_win: current window
        :param destination_win: previous window
        :return: None
        """
        cls.temporary_win = current_win
        current_win.hide()
        destination_win.show()


def start_application(application_starter: object, start_win: object):
    start_win.show()
    sys.exit(application_starter.exec_())
