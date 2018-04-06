# -*- coding:utf-8 -*-
from PyQt5 import QtWidgets
import sys
from server.jsonHelper.interface import MyInterface

config_path = "../config.json"

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myShow = MyInterface(config_path)
    sys.exit(app.exec_())
