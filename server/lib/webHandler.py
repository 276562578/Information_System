# -*- coding:utf-8 -*-
import copy
import json

import bs4
import datetime

import re
import requests


class WebHandler():
    def __init__(self, item):
        self.item = item
        self.r = None

    def request(self):
        preset = self.item["handler"]["preset"]
        method, header, data = preset["method"], preset["header"], preset["data"]
        url = self.getUrl(self.item["info"]["url"])

        # generate request
        if method == "GET":
            if header == {}:
                self.r = requests.get(url)
            elif header != {}:
                self.r = requests.get(url, headers=header)
        elif method == "POST":
            self.r = requests.post(url, data, headers=header)
        return self.r

    def results(self, r):
        obtain = self.item["handler"]["obtain"]
        soup = bs4.BeautifulSoup(r.content,"html5lib")
        if obtain["type"] == "page":
            # find config of content from the page
            contentlist = self.getContentList(obtain["contentlist"], soup)
            # find each content(often title) from config
            content = self.getContent(obtain["content"], contentlist)
            # find each date from config
            date = self.getContent(obtain["date"], contentlist)
            # find each url from config
            url = self.getContent(obtain["url"], contentlist)
            return self.generateResult("tag", content, content, url, date)
        elif obtain["type"] == "json":
            json = self.getJson(obtain["pattern"], soup)
            contentlist = json[obtain["contentlist"]]
            content = self.getJsonContent(obtain["content"], contentlist)
            date = self.getJsonContent(obtain["date"], contentlist)
            url = self.getJsonContent(obtain["url"], contentlist)
            return self.generateResult("str", content, content, url, date)

    def getUrl(self, url):
        if url["type"] == "static":
            return url["url"]
        elif url["type"] == "dynamic":
            soup = bs4.BeautifulSoup(requests.get(url["url"]).content)
            contentlist = self.getContentList(url["contentlist"], soup)
            content = self.getContent(url["content"], contentlist)
            directUrl = url["host"] + content[url["indexOfContent"]].attrs["href"]
            return directUrl

    def getContentList(self, rulelist, page):
        rule0 = rulelist[0]
        if rule0["class"] == "":
            contentlist = page.find_all(rule0["tag"], id=rule0["id"])
        elif rule0["id"] == "":
            contentlist = page.find_all(rule0["tag"], class_=rule0["class"])
        else:
            contentlist = page.find_all(rule0["tag"])

        if len(rulelist) > 1:
            rulelist.pop(0)
            for rule in rulelist:
                for q, p in enumerate(contentlist):
                    if rule["id"] != "":
                        contentlist[q] = p.find_all(rule["tag"], id=rule["id"])[rule["index"]]
                    elif rule["class"] != "":
                        contentlist[q] = p.find_all(rule["tag"], class_=rule["class"])[rule["index"]]
                    else:
                        contentlist[q] = p.find_all(rule["tag"])[rule["index"]]
            return contentlist
        else:
            return contentlist

    def getContent(self, rulelist, contentlist):
        """This contentlist represent a config containing each item tag, not the container config.
        The function can get not only content, but more field such as title, date, author, classification."""
        content = copy.copy(contentlist)

        for rule in rulelist:
            for q, p in enumerate(content):
                if rule["id"] != "":
                    content[q] = p.find_all(rule["tag"], id=rule["id"])[rule["index"]]
                elif rule["class"] != "":
                    content[q] = p.find_all(rule["tag"], class_=rule["class"])[rule["index"]]
                else:
                    content[q] = p.find_all(rule["tag"])[rule["index"]]
        return content

    def getJson(self, pattern, page):
        pageStr = str(page)
        raw = re.findall(pattern, pageStr)[0]
        jsonStr = re.findall("\{.+\}", raw)[0]
        return json.loads(jsonStr)

    def getJsonContent(self, rulelist, contentlist):
        content = copy.copy(contentlist)
        for i in rulelist:
            for m in range(len(content)):
                content[m] = content[m][i]
        return content

    def generateResult(self, type, contentlist, title, url, date):
        obtain = self.item["handler"]["obtain"]
        result = []
        if type == "tag":
            for i in range(len(contentlist)):
                result.append({})
                result[i]["title"] = title[i].text.strip()
                result[i]["url"] = obtain["host"] + url[i].attrs["href"]
                result[i]["writtenDate"] = self.dateFormat(date[i].text.strip(), obtain["dateParse"])
        elif type == "str":
            for i in range(len(contentlist)):
                result.append({})
                result[i]["title"] = title[i]
                result[i]["url"] = obtain["host"] + url[i]
                result[i]["writtenDate"] = self.dateFormat(date[i], obtain["dateParse"])
        return result

    def dateFormat(self, date, format):
        if format == "":
            dateNew = datetime.datetime.fromtimestamp(date)
            return dateNew
        else:
            dateNew = datetime.datetime.strptime(date, format)
            return dateNew
