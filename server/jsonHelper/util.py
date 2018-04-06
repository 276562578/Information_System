# -*- coding: utf-8 -*-
import hashlib
import json
import threading
import subprocess

import time
from PyQt5 import QtWidgets, QtCore
from interface import Ui_Form as uiInterface
from chooseLauncherFile import Ui_Form as uiChooseLauncherFile
# from chooseDownloadSource import Ui_Dialog as uiChooseDownloadSourceDialog
import socket, sys, os, requests, getpass

MOD_DEFAULT_DIR = ".minecraft/mods/"
SERVER_HOST = "http://123.206.45.145:23333/"
EXEC_FILE = ""
CLIENT_VERSION = 0.1

class MyChooseLauncherFile(uiChooseLauncherFile):
    def confirm(self, item):
        EXEC_FILE = item.text()


class MyInterface(uiInterface):
    def __init__(self):
        self.upgrade_list = {}
        self.window = QtWidgets.QWidget()
        self.setupUi(self.window)

        self.progressBar.setValue(0)
        self.pushButton.setEnabled(False)

        self.threads = QtCore.QThread()
        self.threads.run = self.init
        self.threads.start()

        self.window.show()

    def init(self):
        self.util = Util(self)
        self.util.checkVersion()
        self.util.detectLauncher()
        self.label.setText("Version: " + str(CLIENT_VERSION))
        self.syncToServer()

    def chooseLauncherFile(self):
        self.chooseLauncherWindow = QtWidgets.QWidget()
        self.chooseLauncherUi=MyChooseLauncherFile()
        self.chooseLauncherUi.setupUi(self.chooseLauncherWindow)
        self.chooseLauncherWindow.show()

    def syncToServer(self):
        local_mod_list = {}
        self.showInConsole("校验本地文件")
        for relpath, dirs, files in os.walk(MOD_DEFAULT_DIR):
            for i in files:
                f = open(MOD_DEFAULT_DIR + i, "rb").read()
                local_mod_list[i] = hashlib.md5(f).hexdigest()
        self.showInConsole("获取更新列表......			")
        # try:
        r = requests.post(SERVER_HOST + "checkVersion", json.dumps(local_mod_list))
        upgrade_list = json.loads(r.text)
        self.upgrade_list = upgrade_list
        self.showInConsole("获取更新列表					Success!")
        if len(self.upgrade_list) == 0:
            self.showInConsole("没有可更新的mod")
            self.pushButton.setEnabled(True)

        else:
            self.showInConsole("有 " + str(len(self.upgrade_list)) + " 个mod需要更新")
            self.chooseDownloadSource()

    def chooseDownloadSource(self):
        self.downloadFromServer()
        pass

    def downloadFromServer(self):
        for i in self.upgrade_list:
            if os.path.exists(MOD_DEFAULT_DIR + i):
                self.showInConsole(u"移除过期mod：" + i)
                os.remove(MOD_DEFAULT_DIR + i)
            self.showInConsole(u"下载mod：" + i)
            r = requests.post(SERVER_HOST + "getMod", json.dumps({"name": i}))
            f = open(MOD_DEFAULT_DIR + r.headers['name'], "wb")
            f.write(r.content)
            f.close()
            self.showInConsole(i + u"下载完成！")
        self.showInConsole(r.headers['name'] + u"下载完成")
        self.pushButton.setEnabled(True)


    def start(self):
        subprocess.Popen(EXEC_FILE)
        sys.exit()

    def showInConsole(self, string):
        self.textEdit.append(string)


class Util():
    def __init__(self, interface):
        self.interface = interface

    def detectLauncher(self):
        global EXEC_FILE, MOD_DEFAULT_DIR
        file_list = os.listdir("./")
        if "MinecraftLauncher.exe" in file_list:
            self.interface.showInConsole("欢迎您，正版用户")
            EXEC_FILE = "MinecraftLauncher.exe"
            MOD_DEFAULT_DIR = "C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/mods/"
        elif "HMCL" in file_list:
            EXEC_FILE = "HMCL"
            MOD_DEFAULT_DIR = ".minecraft/mods/"
        else:
            self.interface.chooseLauncherFile()
        # else:
        #     for i in file_list:
        #         if "HMCL" in i:
        #             if "exe" in i:
        #                 EXEC_FILE = i
        #                 MOD_DEFAULT_DIR = ".minecraft/mods/"

    def checkVersion(self):
        check_url = SERVER_HOST + "versionCheck"
        main_url = SERVER_HOST + "JLU-MC.exe"
        version = requests.get(check_url).content
        version = json.loads(version)
        if version["version"] > CLIENT_VERSION:
            self.interface.showInConsole("发现客户端新版本，更新ing")
            with open("JLU-MC_update.exe", "wb") as f:
                new_file = requests.get(main_url).content
                f.write(new_file)

            with open("JLU-MC_update.exe", "rb") as f:
                md5 = hashlib.md5(f.read()).hexdigest()
                if md5 == version["md5"]:
                    subprocess.Popen("updater.exe")
                    sys.exit()
                else:
                    self.checkVersion()

    def chooseLauncherFile(self):
        self.interface.chooseLauncherFileWindow = QtWidgets.QWidget()
        self.interface.chooseLauncherFileUi = MyChooseLauncherFile()
        self.interface.chooseLauncherFileUi.setupUi(self.interface.chooseLauncherFileWindow)
        self.interface.chooseLauncherFileWindow.show()
        # self.ui.listWidget.addItems(os.listdir("."))
