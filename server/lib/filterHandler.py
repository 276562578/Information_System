# -*- coding:utf-8 -*-

class FilterHandler():
    def __init__(self,item):
        self.config=item


    def filter(self,result,model=0):
        # model 0 is white and black
        # 1 is the other part after black white
        result = self.whiteFilter(result)
        result = self.blackFilter(result)
        return result

    def whiteFilter(self,result):
        filter=self.config["handler"]["filter"]["whitelist"]
        if "" in filter:
            return result
        else:
            new_result = []
            for index,item in enumerate(result):
                for keyword in filter:
                    if keyword in item["title"]:
                        new_result.append(item)
            return new_result

    def blackFilter(self,result):
        filter = self.config["handler"]["filter"]["blacklist"]
        if "" in filter:
            return result
        else:
            new_result = result.copy()
            for index,item in enumerate(result):
                for keyword in filter:
                    if keyword in item["title"]:
                        new_result.remove(item)
            return new_result

    def importance(self,result):
        filter = self.config["handler"]["filter"]["importance"]
        if "" in filter:
            return []
        else:
            importance=[]
            for index,item in enumerate(result):
                for keyword in filter:
                    if keyword in item["title"]:
                        importance.append(item)
            return importance