
from core.controlsAttr import ControlsStyle as Cs
from LibGui.r_controls import *

# 控件工厂
class ControlFactory:
    def __init__(self):
        pass

    def createControl(self,parent,name,all_attr:dict,style:str=None,text:str=None):
        rect = all_attr["rect"]
        w,h,x,y = rect["w"],rect["h"],rect["x"],rect["y"]

        # 合成提示
        top = "<{}".format(all_attr["tagName"].lower())
        for k,v in all_attr.items():
            if k in ["tagName","text","rect"]:
                continue
            else:
                top += ' {}=\"{}\"'.format(k, v)
        top += " </{}>".format(all_attr["tagName"].lower())

        if name == "QPushButton":
            temp = PushButton()
            temp.setObjectName("QPushButton")
            if text:
                temp.setText(text.strip().replace("\n",""))
            else:
                temp.setText("按钮")
        elif name == "DIV_QPushButton":
            temp = PushButton()
            temp.setObjectName("DIV_QPushButton")
            if text:
                temp.setText(text.strip().replace("\n",""))
            else:
                temp.setText("Div")
        elif name == "QLineEdit":
            temp = LineEdit()
            temp.setObjectName("QLineEdit")
            if text:
                temp.setPlaceholderText(text.strip().replace("\n",""))
            else:
                temp.setPlaceholderText("input")
        elif name == "A_QLineEdit":
            temp = LineEdit()
            temp.setObjectName("A_QLineEdit")
            if text:
                temp.setPlaceholderText(text.strip().replace("\n", ""))
            else:
                temp.setPlaceholderText("A_label")
        elif name == "QComboBox":
            temp = ComboBox()
            temp.setObjectName("QComboBox")
            items = [l.strip().replace("\n","") for l in text.split("\n")]
            new_itmes =[]
            for l in items:  # 去除空元素
                if l:
                    new_itmes.append(l)
            temp.addItems(new_itmes)
        temp.setParent(parent)
        temp.setToolTip(top)
        temp.setStyleSheet(style)
        temp.resize(w,h)
        temp.move(x,y)
        temp.show()
        return temp

    def button(self,parent,all_attr:dict,text:str=None):
        style = Cs.CStyle[Ct.Button]
        return self.createControl(parent,"QPushButton",all_attr,style,text)

    def input(self,parent,all_attr:dict,text:str=None):
        style = Cs.CStyle[Ct.Input]
        return self.createControl(parent,"QLineEdit",all_attr,style,text)

    def a(self,parent,all_attr:dict,text:str=None):
        style = Cs.CStyle[Ct.A]
        return self.createControl(parent,"A_QLineEdit",all_attr,style,text)

    def select(self,parent,all_attr:dict,text):
        style = Cs.CStyle[Ct.Select]
        return self.createControl(parent,"QComboBox",all_attr,style,text)

    def div(self,parent,all_attr:dict,text):
        style = Cs.CStyle[Ct.Div]
        return self.createControl(parent,"DIV_QPushButton",all_attr,style,text)