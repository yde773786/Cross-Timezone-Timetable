"""
Add schedule dialog construction.
"""

from PyQt5 import QtCore, QtWidgets
from UI.Layouts.base_designer import add_hard_code_loc_widget


class Ui_Add_Dialog(object):

    def __init__(self):
        self.start_min = QtWidgets.QLineEdit()
        self.error_dialog = QtWidgets.QLabel()
        self.end_min = QtWidgets.QLineEdit()
        self.end_hour = QtWidgets.QLineEdit()
        self.start_hour = QtWidgets.QLineEdit()
        self.name_schedule = QtWidgets.QLineEdit()
        self.day_week = QtWidgets.QComboBox()
        self.label_7 = QtWidgets.QLabel()
        self.label_6 = QtWidgets.QLabel()
        self.label_5 = QtWidgets.QLabel()
        self.label_4 = QtWidgets.QLabel()
        self.label_3 = QtWidgets.QLabel()
        self.label_2 = QtWidgets.QLabel()
        self.label = QtWidgets.QLabel()
        self.button_box = QtWidgets.QDialogButtonBox()

    def setup_ui(self, dialog) -> None:
        dialog.setObjectName("dialog")
        dialog.resize(596, 324)

        self.button_box.setParent(dialog)
        add_hard_code_loc_widget(self.button_box, dialog, (230, 230, 171, 32), 'button box')
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel |
                                           QtWidgets.QDialogButtonBox.Ok)

        add_hard_code_loc_widget(self.label, dialog, (250, 20, 111, 20), 'label')
        add_hard_code_loc_widget(self.label_2, dialog, (130, 180, 101, 31), "label_2")
        add_hard_code_loc_widget(self.label_3, dialog, (130, 70, 141, 31), "label_3")
        add_hard_code_loc_widget(self.label_4, dialog, (130, 130, 101, 31), "label_4")
        add_hard_code_loc_widget(self.label_5, dialog, (340, 130, 20, 21), "label_5")
        add_hard_code_loc_widget(self.label_6, dialog, (390, 130, 20, 21), "label_6")
        add_hard_code_loc_widget(self.label_7, dialog, (450, 130, 20, 21), "label_7")
        add_hard_code_loc_widget(self.day_week, dialog, (330, 180, 131, 26), "day_week")
        add_hard_code_loc_widget(self.name_schedule, dialog, (330, 70, 131, 26), "name_schedule")

        self.name_schedule.setAlignment(QtCore.Qt.AlignCenter)

        add_hard_code_loc_widget(self.start_hour, dialog, (300, 130, 31, 26), 'start_hour')
        self.start_hour.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.start_hour.setAlignment(QtCore.Qt.AlignCenter)

        add_hard_code_loc_widget(self.start_min, dialog, (350, 130, 31, 26), 'start_min')
        self.start_min.setAlignment(QtCore.Qt.AlignCenter)

        add_hard_code_loc_widget(self.end_hour, dialog, (410, 130, 31, 26), 'end hour')
        self.end_hour.setAlignment(QtCore.Qt.AlignCenter)

        add_hard_code_loc_widget(self.end_min, dialog, (460, 130, 31, 26), 'end_min')
        self.end_min.setGeometry(QtCore.QRect(460, 130, 31, 26))
        self.end_min.setAlignment(QtCore.Qt.AlignCenter)
        self.end_min.setObjectName("end_min")

        add_hard_code_loc_widget(self.error_dialog, dialog, (20, 270, 561, 31), 'error_dialog')
        self.error_dialog.setText("")
        self.error_dialog.setAlignment(QtCore.Qt.AlignCenter)

        self.retranslate_ui(dialog)
        self.button_box.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, dialog) -> None:
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Add Schedule"))
        self.label.setText(_translate("dialog", "Add Schedule"))
        self.label_2.setText(_translate("dialog", "Day of Week"))
        self.label_3.setText(_translate("dialog", "Name of Schedule:"))
        self.label_4.setText(_translate("dialog", "Timing:"))
        self.label_5.setText(_translate("dialog", ":"))
        self.label_6.setText(_translate("dialog", "to"))
        self.label_7.setText(_translate("dialog", ":"))
