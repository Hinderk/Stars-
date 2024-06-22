
from PyQt5 import QtGui, QtCore
from pathlib import Path

import os


BaseDirectory = Path(__file__).resolve().parent


def LoadFonts(Directory):
    FontDB = QtGui.QFontDatabase()
    Path = os.fspath(BaseDirectory / Directory)
    for Font in QtCore.QDir(Path).entryInfoList(["*.ttf"]):
        FontDB.addApplicationFont(Font.absoluteFilePath())
