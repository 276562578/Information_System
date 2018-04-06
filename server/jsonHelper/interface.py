# -*- coding:utf-8 -*-
import json

from server.jsonHelper.jsonHelper import Ui_Form as uiJsonHelper
from PyQt5 import QtWidgets, QtGui, QtCore


class MyInterface(uiJsonHelper):
    def __init__(self, config_path):
        self.config_path = config_path
        with open(self.config_path, "r") as f:
            self.config = json.load(f)

        self.window = QtWidgets.QWidget()
        self.setupUi(self.window)
        self.window.show()

        self.initItemListWidget()

    def initItemListWidget(self):
        # color_grey_qbrush_object = QtGui.QBrush(QtGui.QColor(111,111,111))
        if self.listWidget.count() != 0:
            print("not empty")
            self.listWidget.clear()

        for index, item in enumerate(self.config["itemlist"]):
            print(item)
            self.listWidget.insertItem(index, item)
            if item in self.config["itemactivelist"]:
                self.listWidget.item(index).setForeground(QtCore.Qt.green)
            else:
                self.listWidget.item(index).setForeground(QtCore.Qt.darkGray)
        self.listWidget.sortItems()

    def enableItem(self):
        itemName = self.listWidget.currentItem().text()
        if itemName not in self.config["itemactivelist"]:
            self.config["itemactivelist"].append(itemName)
            self.listWidget.currentItem().setForeground(QtCore.Qt.green)
            with open(self.config_path, "w") as f:
                f.write(json.dumps(self.config))

    def disableItem(self):
        itemName = self.listWidget.currentItem().text()
        if itemName in self.config["itemactivelist"]:
            self.config["itemactivelist"].remove(itemName)
            self.listWidget.currentItem().setForeground(QtCore.Qt.darkGray)
            with open(self.config_path, "w") as f:
                f.write(json.dumps(self.config))

    def saveNewItemConfig(self):
        def refill(self):
            pass

        def check(self):
            boolean = True
            if self.lineEdit.text() == "":
                boolean = False
            elif self.lineEdit_2.text() == "http://":
                boolean = False
            elif self.lineEdit_3.text() == "":
                boolean = False
            return boolean

        def obtainList(widget):
            result = []
            for m in range(3):
                if widget.item(m, 0) == None:
                    break
                elif widget.item(m, 0) == "":
                    break
                else:
                    result.append({"tag": widget.item(m, 0).text(),
                                   "class": widget.item(m, 1).text(),
                                   "id": widget.item(m, 2).text(),
                                   "index": int(widget.item(m, 3).text())})
            return result

        def readyForSave(self):
            if check(self) == True:
                if self.lineEdit.text() not in self.config["itemlist"]:
                    self.config["itemlist"].append(self.lineEdit.text())
                # info part
                info_url = {"type": self.comboBox.currentText(),
                            "url": self.lineEdit_2.text()}
                info = {"url": info_url,
                        "displayName": self.lineEdit_3.text(),
                        "name": self.lineEdit.text(),
                        "classification": self.comboBox_2.currentText()}

                # handler part

                # handler filter0 part
                filter0 = {"blacklist": self.lineEdit_4.text().split("|"),
                          "whitelist": self.lineEdit_5.text().split("|"),
                          "importance": self.lineEdit_6.text().split("|")}

                # handler preset part
                if self.radioButton.isChecked() == True:
                    preset_method = "GET"
                elif self.radioButton_2.isChecked() == True:
                    preset_method = "POST"
                else:
                    preset_method = "GET"
                preset = {"method": preset_method,
                          "header": json.loads(self.lineEdit_7.text()),
                          "data": json.loads(self.lineEdit_8.text())}

                # handler obtain part
                obtain = {"type": self.comboBox_4.currentText(),
                          "contentlist": obtainList(self.tableWidget),
                          "content": obtainList(self.tableWidget_2),
                          "date": obtainList(self.tableWidget_3),
                          "url": obtainList(self.tableWidget_4),
                          "dateParse": self.comboBox_3.currentText(),
                          "host": self.lineEdit_9.text()}

                # handler storage part
                storage = {"db": "",
                           "table": info["name"],
                           "field": self.lineEdit_10.text().split("|")}
                handler = {"filter": filter0,
                           "preset": preset,
                           "obtain": obtain,
                           "storage": storage}

                self.config["item"][info["name"]] = {"info": info,
                                                     "handler": handler}


                return self.config
            else:
                refill(self)
                return self.config

        self.config = readyForSave(self)
        with open(self.config_path, "w") as f:
            f.write(json.dumps(self.config))
        # refresh itemlist
        self.initItemListWidget()
