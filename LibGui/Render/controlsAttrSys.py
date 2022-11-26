


# 控件数据管理系统
class ControlsAttrSys:
    def __init__(self):
        self.all_attr = []  # type:list

    def setAllAttr(self, attr_list:list):
        self.all_attr = attr_list

    def setAttr(self,key,value):
        for allattr in self.all_attr:
            if key in allattr:
                allattr[key] = value

    def append(self,attr:dict):
        self.all_attr.append(attr)


    def clear(self):
        self.all_attr.clear()

    # 全部更新
    def allUpDate(self,attr_list:list):
        self.clear()
        self.setAllAttr(attr_list)