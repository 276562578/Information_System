# -*- coding:utf-8 -*-
from server.lib.webHandler import WebHandler
from server.lib.filterHandler import FilterHandler
class LocalHandler():
    def __init__(self, config):
        self.config=config

    def getAll(self):
        result = {}
        print("Items need to get as following: ",self.config["itemactivelist"])
        for item in self.config["itemactivelist"]:
            result[item]=self.getLast(self.config["item"][item])
        return result


    def getLast(self,item):
        webhandler = WebHandler(item)
        r = webhandler.request()
        result = webhandler.results(r)


        f=FilterHandler(item)

        importance=f.importance(result)
        self.push(importance)

        result=f.filter(result)
        return result

    def push(self,importance):
        if len(importance) > 0:
            pass
        pass

    def save(self):
        pass