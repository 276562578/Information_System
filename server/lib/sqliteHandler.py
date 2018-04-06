# -*- coding:utf-8 -*-
import datetime
import sqlite3


class SqliteHandler():
    def __init__(self, db_path, result, config):
        self.config=config
        self.con = sqlite3.connect(db_path)
        self.itemList = result

    def generateSql(self, item, field):
        sql = "INSERT or ignore INTO new ("
        for i in field:
            sql += i + ","
        sql = sql[0:-1] + ",addtime,isRead,belong) values ("
        for i in range(len(field) + 2):
            sql += "?,"
        sql = sql +"\""+ item +"\")"
        return sql

    def saveItem(self, item, result, field):
        value = []
        for i in range(len(result)):
            addtime = datetime.datetime.now()
            if len(field) == 2:
                value.append((result[i][field[0]], result[i][field[1]], addtime, 0))
            elif len(field) == 3:
                value.append((result[i][field[0]], result[i][field[1]], result[i][field[2]], addtime, 0))
            elif len(field) == 4:
                value.append(
                    (result[i][field[0]], result[i][field[1]], result[i][field[2]], result[i][field[3]], addtime, 0))
            elif len(field) == 5:
                value.append((result[i][field[0]], result[i][field[1]], result[i][field[2]], result[i][field[3]],
                              result[i][field[4]], addtime, 0))
        sql = self.generateSql(item, field)
        self.con.executemany(sql, value)

    def saveAll(self):
        for item in self.itemList:
            field = self.config["item"][item]["handler"]["storage"]["field"]
            self.saveItem(item, self.itemList[item], field)

    def __del__(self):
        self.con.commit()
        self.con.close()

    def getField(self, item):
        field = self.itemList
        return field