"""
Base layout script for all types of warnings.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import UI.Layouts.Image_assets.resources
from UI.Layouts.base_designer import add_widget_to_layout


class Ui_Dialog(object):

    def __init__(self):
        self.button_box = QtWidgets.QDialogButtonBox()
        self.label_2 = QtWidgets.QLabel()
        self.label = QtWidgets.QLabel()
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.vertical_layout = QtWidgets.QVBoxLayout()

    def setup_ui(self, dialog):
        dialog.setObjectName("Dialog")
        dialog.resize(504, 163)

        self.vertical_layout.setObjectName('verticalLayout')
        self.horizontal_layout.setObjectName("horizontalLayout")

        add_widget_to_layout(self.label, self.horizontal_layout, 'label')
        self.label.setPixmap(QtGui.QPixmap(":Image_assets/warning.png"))
        add_widget_to_layout(self.label_2, self.horizontal_layout, 'label_2')
        self.vertical_layout.addLayout(self.horizontal_layout)

        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        add_widget_to_layout(self.button_box, self.vertical_layout, 'button_box')

        self.retranslate_ui(dialog)
        self.button_box.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        dialog.setLayout(self.vertical_layout)

    def retranslate_ui(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Dialog", "Message"))
        self.label.setText(_translate("Dialog", ""))
        self.label_2.setText(_translate("Dialog", ""))
