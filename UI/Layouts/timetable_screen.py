from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from Managers.TimeZoneManager import ALL_DAYS

DAY_NAMES = [day[:3] for day in ALL_DAYS]
TOTAL_HEIGHT = 683
TOTAL_WIDTH = 1000
MENU_HEIGHT = 30
MARGIN = 5


class Ui_MainWindow(object):

    def __init__(self):

        self.action_save_and_exit = QtWidgets.QAction()
        self.action_save_and_return = QtWidgets.QAction()
        self.action_delete_schedule = QtWidgets.QAction()
        self.action_add_schedule = QtWidgets.QAction()
        self.menu_bar = QtWidgets.QMenuBar()
        self.central_widget = QtWidgets.QWidget()
        self.timetable_canvas = QtWidgets.QGridLayout(self.central_widget)
        self.temp = QLabel()

    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(TOTAL_WIDTH, TOTAL_HEIGHT)
        self.menu_bar.setParent(main_window)
        self.menu_bar.setFixedHeight(MENU_HEIGHT)
        self.central_widget.setObjectName("centralwidget")
        self.central_widget.setParent(main_window)
        self.timetable_canvas.setContentsMargins(MARGIN, MARGIN, MARGIN, MARGIN)
        self.timetable_canvas.setSpacing(0)
        self.timetable_canvas.setObjectName("gridLayout")

        for x in range(25):
            for y in range(8):
                if x == 0 and y != 0:
                    empty_label = QLabel(DAY_NAMES[y - 1])
                    empty_label.setAlignment(QtCore.Qt.AlignCenter)

                elif y == 0 and x != 0:
                    time = str(x - 1) + ':' + '00'
                    empty_label = QLabel(time)
                    empty_label.setAlignment(QtCore.Qt.AlignTop and QtCore.Qt.AlignRight)

                else:
                    empty_label = QLabel('')

                empty_label.setStyleSheet("border: 1px solid black;")
                font = QtGui.QFont()
                font.setFamily("FreeMono")
                font.setPointSize(10)
                empty_label.setFont(font)

                self.timetable_canvas.addWidget(empty_label, x, y)

        main_window.setCentralWidget(self.central_widget)
        self.menu_bar.setObjectName("menubar")
        main_window.setMenuBar(self.menu_bar)

        self.action_add_schedule.setObjectName("actionAdd_Schedule")
        self.action_add_schedule.setParent(main_window)
        self.action_delete_schedule.setObjectName("actionDelete_Schedule")
        self.action_delete_schedule.setParent(main_window)
        self.action_save_and_return.setObjectName("actionSave_and_Return")
        self.action_save_and_return.setParent(main_window)
        self.action_save_and_exit.setObjectName("actionSave_and_Exit")
        self.action_save_and_exit.setParent(main_window)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.action_add_schedule.setText(_translate("MainWindow", "Add Schedule"))
        self.action_delete_schedule.setText(_translate("MainWindow", "Delete Schedule"))
        self.action_save_and_return.setText(_translate("MainWindow", "Save and Continue"))
        self.action_save_and_exit.setText(_translate("MainWindow", "Save and Return"))
