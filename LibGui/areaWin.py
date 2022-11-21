# -*- coding:utf-8 -*-
# @time:2022/11/1917:52
# @author:LX
# @file:areaWin.py
# @software:PyCharm


import sys
from PyQt5.sip import delete
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QComboBox
)


# 控件工厂
class ControlFactory:
    def __init__(self):
        pass

    def createControl(self,parent,name,rect:dict,style:str=None,text:str=None):
        w,h,x,y = rect["w"],rect["h"],rect["x"],rect["y"]

        if name == "QPushButton":
            temp = QPushButton()
            temp.setObjectName("QPushButton")
            if text:
                temp.setText(text.strip().replace("\n",""))
            else:
                temp.setText("按钮")
        elif name == "DIV_QPushButton":
            temp = QPushButton()
            temp.setObjectName("DIV_QPushButton")
            if text:
                temp.setText(text.strip().replace("\n",""))
            else:
                temp.setText("Div")
        elif name == "QLineEdit":
            temp = QLineEdit()
            temp.setObjectName("QLineEdit")
            if text:
                temp.setPlaceholderText(text.strip().replace("\n",""))
            else:
                temp.setPlaceholderText("input")
        elif name == "A_QLineEdit":
            temp = QLineEdit()
            temp.setObjectName("A_QLineEdit")
            if text:
                temp.setPlaceholderText(text.strip().replace("\n", ""))
            else:
                temp.setPlaceholderText("A_label")
        elif name == "QComboBox":
            temp = QComboBox()
            temp.setObjectName("QComboBox")
            items = [l.strip().replace("\n","") for l in text.split("\n")]
            new_itmes =[]
            for l in items:  # 去除空元素
                if l:
                    new_itmes.append(l)
            temp.addItems(new_itmes)
        temp.setParent(parent)
        temp.setStyleSheet(style)
        temp.resize(w,h)
        temp.move(x,y)
        temp.show()
        return temp

    def button(self,parent,rect:dict,text:str=None):
        style = '''
border:1px solid rgb(85, 170, 0);
background-color:transparent;
        '''
        return self.createControl(parent,"QPushButton",rect,style,text)

    def input(self,parent,rect:dict,text:str=None):
        style='''
border:1px solid rgb(131, 131, 0);
background-color:transparent;
        '''
        return self.createControl(parent,"QLineEdit",rect,style,text)

    def a(self,parent,rect:dict,text:str=None):
        style='''
border:1px solid rgb(5, 134, 255);
border-top:none;
border-left:none;
border-right:none;
background-color:transparent;
        '''
        return self.createControl(parent,"A_QLineEdit",rect,style,text)

    def select(self,parent,rect:dict,text):
        style='''
border:1px solid rgb(170, 170, 255);
color: rgb(255, 255, 255);
        '''
        return self.createControl(parent,"QComboBox",rect,style,text)

    def div(self,parent,rect:dict,text):
        style='''
border:2px dotted rgb(225, 112, 169);
        '''
        return self.createControl(parent,"DIV_QPushButton",rect,style,text)


# 绘制区域(渲染)
class AreaWin(QWidget):
    def  __init__(self,*args,**kwargs):
        super(AreaWin, self).__init__(*args,**kwargs)

        # 控件渲染字典
        '''
            这个字典决定  该控件是否被渲染出来
        '''
        self.render_dict = {"div":True,
                            "a":True,
                            "input":True,
                            "button":True,
                            "select":True}

        self.resize(1200,800)
        self.setObjectName("AreaWin")
        self.setStyleSheet('''
*{
color:#fff;
}
#AreaWin{
background-color: rgb(33, 33, 33);
}
QPushButton{
border:1px solid rgb(35, 105, 255);
}
QPushButton:hover{
border-width:2px;
}
QLineEdit{
border:1px solid rgb(131, 131, 0);
background-color:transparent;
}
QLineEdit:hover{
border-width:2px;
}
        ''')

        self.control_factory = ControlFactory()
        # print(self.desktopSize())

    # 通过属性来验证控件的可视类型
    def getVerifyControlType(self,rect:dict):
        final_type = None
        # input标签检测
        if rect["tagName"].lower() == "input":
            final_type = "input"
            if rect.get("type") != None:
                if  rect.get("type") == "submit" \
                    or rect.get("type") == "button" \
                    or rect.get("onclick"):
                    final_type = "button"
        # a标签检测
        if rect["tagName"].lower() == "a":
            final_type = "a"
            if rect.get("onclick"):
                final_type = "button"

        if rect["tagName"].lower() == "button":
            final_type = "button"

        if rect["tagName"].lower() == "label":
            pass

        if rect["tagName"].lower() == "select":
            final_type = "select"

        if rect["tagName"].lower() == "div":
            final_type = "div"

        # print(final_type)
        return final_type

    # 单独设置某个标签是否渲染
    def setControlRender(self,label_name,v:bool):
        if "div" in label_name.lower():  # div特殊对待
            label_name = "div"

        if self.render_dict.get(label_name,None) is not None:
            self.render_dict[label_name] = v

    # 自动创建
    def autoCreate(self,all_attr):
        rect = all_attr["rect"]
        final_type = self.getVerifyControlType(all_attr) # 验证控件类型

        if final_type == "input" and self.render_dict[final_type]:
            self.control_factory.input(self, rect, text=all_attr.get("placeholder", None))
        elif final_type == "button" and self.render_dict[final_type]:
            value = all_attr.get("value", None)
            text = all_attr.get("text", None)
            self.control_factory.button(self, rect, text=value if value else text)
        elif final_type == "a" and self.render_dict[final_type]:
            self.control_factory.a(self, rect, text=all_attr.get("text", None))
        elif final_type == "select" and self.render_dict[final_type]:
            self.control_factory.select(self,rect,text=all_attr.get("text", None))
        elif final_type == "div" and self.render_dict[final_type]:
            self.control_factory.div(self, rect, text=all_attr.get("text", None))

        # print(final_type,"绘制完成")

    # 销毁所有控件
    def delControl(self):
        children_c = self.children()
        if not children_c:
            return

        for c in children_c:
            delete(c)
        print("销毁所有控件完成")

    # 隐藏控件
    def hideControl(self,name):
        children_c = self.children()

        if not children_c:
            return

        for c in children_c:
            if c.objectName() == name:
                c.hide()


    # 获取屏幕大小
    def desktopSize(self):
        d_size = QApplication.desktop().size()
        count = QApplication.desktop().screenCount()
        return d_size.width()//count,d_size.height()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = AreaWin()
    win.show()

    sys.exit(app.exec_())