from PyQt5 import QtCore, QtWidgets

from UI.Layouts.base_designer import add_hard_code_loc_widget


def retranslate_ui(dialog):
    _translate = QtCore.QCoreApplication.translate
    dialog.setWindowTitle(_translate("Dialog", "Dialog"))


class Ui_Delete_Dialog(object):

    def __init__(self):
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_area = QtWidgets.QScrollArea()
        self.button_box = QtWidgets.QDialogButtonBox()

    def setup_ui(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(479, 300)

        add_hard_code_loc_widget(self.button_box, dialog, (160, 240, 171, 32), 'button_box')
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel
                                           | QtWidgets.QDialogButtonBox.Ok)

        add_hard_code_loc_widget(self.scroll_area, dialog, (10, 20, 461, 211), 'scroll_area')
        self.scroll_area.setWidgetResizable(True)

        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 459, 209))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout.setObjectName("verticalLayout")
        self.scroll_area.setWidget(self.scrollAreaWidgetContents)

        retranslate_ui(dialog)
        self.button_box.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)
