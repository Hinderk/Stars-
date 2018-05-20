
from PyQt5 import QtCore

from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSpacerItem



class Square(QWidget):
    """Helper widget to keep contained widgets square."""
    def __init__(self, widget, parent):
        super().__init__(parent)
        self.aspect_ratio = widget.size().width() / widget.size().height()
        self.setLayout(QBoxLayout(QBoxLayout.LeftToRight, self))
        #  add spacer, then widget, then spacer
        self.layout().addItem(QSpacerItem(0, 0))
        self.layout().addWidget(widget)
        self.layout().addItem(QSpacerItem(0, 0))


    def resizeEvent(self, e):
        """Create the proper stretch values to keep the contents square."""
        w = e.size().width()
        h = e.size().height()
        if w / h > self.aspect_ratio:  # too wide
            self.layout().setDirection(QBoxLayout.LeftToRight)
            widget_stretch = h * self.aspect_ratio
            outer_stretch = (w - widget_stretch) / 2 + 0.5
        else:  # too tall
            self.layout().setDirection(QBoxLayout.TopToBottom)
            widget_stretch = w / self.aspect_ratio
            outer_stretch = (h - widget_stretch) / 2 + 0.5
        self.layout().setStretch(0, outer_stretch)
        self.layout().setStretch(1, widget_stretch)
        self.layout().setStretch(2, outer_stretch)