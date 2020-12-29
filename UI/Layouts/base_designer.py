"""
Common design features to layouts.
"""

from typing import Tuple

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLayout


def add_hard_code_loc_widget(widget: QWidget, parent: QWidget,
                             geometry: Tuple[int, int, int, int], name: str) -> None:
    """Adds a widget that has been hard coded a specific location on the layout,
    (hard codings are done specifically for QDialogs)

    :param parent: Parent Layout
    :param widget: The widget being inserted
    :param geometry: Concrete location and size
    :param name: Name of widget
    :return: None
    """
    widget.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))
    widget.setObjectName(name)
    widget.setParent(parent)


def add_widget_to_layout(widget: QWidget, layout: QLayout, name: str) -> None:
    """Adds a widget that belongs to a spacific layout

    :param widget: The widget being inserted
    :param layout: Layout to which widget is inserted
    :param name: Name of widget
    :return: None
    """
    widget.setObjectName(name)
    layout.addWidget(widget)
