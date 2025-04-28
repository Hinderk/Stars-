
from PyQt6 import QtGui, QtCore
from pathlib import Path

import os


base_directory = Path(__file__).resolve().parent


def load_fonts(directory):
    font_db = QtGui.QFontDatabase()
    path = os.fspath(base_directory / directory)
    for font in QtCore.QDir(path).entryInfoList(["*.ttf"]):
        font_db.addApplicationFont(font.absoluteFilePath())
