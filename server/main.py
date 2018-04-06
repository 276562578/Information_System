# -*- coding: utf-8 -*-
import bs4
import copy
import json
import re
import requests
import time
import sqlite3
from server.lib.sqliteHandler import SqliteHandler
from server.lib.localHandler import LocalHandler
import datetime

with open("config.json","r",encoding="utf-8") as f:
    config = json.load(f)
db_path = "./data.db"



if __name__ == '__main__':
    localHandler = LocalHandler(config)
    result=localHandler.getAll()
    dataHandler = SqliteHandler(db_path, result, config)
    dataHandler.saveAll()

