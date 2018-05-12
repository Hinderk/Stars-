"""This module is the launcher for the graphical user interface."""

import sys
from PyQt5.QtWidgets import QApplication

from client import Client


if __name__ == '__main__':

    app = QApplication(sys.argv)
    stars = Client()
    stars.show()
    sys.exit(app.exec_())
