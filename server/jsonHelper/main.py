# -*- coding: utf-8 -*-
import time
from PyQt5 import QtWidgets
import sys
from util import MyInterface,Util



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myShow = MyInterface()
    sys.exit(app.exec_())