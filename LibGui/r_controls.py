# -*- coding:utf-8 -*-
# @time:2022/11/2217:40
# @author:LX
# @file:r_controls.py
# @software:PyCharm

import re
import sys
from functools import partial
from PyQt5.sip import delete
from PyQt5.QtCore import Qt,QPoint,pyqtSignal
from PyQt5.QtGui import QCursor
from core.controlsAttr import ControlsType as Ct
from commonHead.Qt.qtWidgets import (
    QApplication,
    QPushButton,
    QLineEdit,
    QWidget,
    QMenu,
    QGroupBox,
    QCheckBox,
    QGridLayout,
    QComboBox
)
# 让所有渲染的控件都具有右键功能的基类
class RQWidgetABC(QWidget):
    def __init__(self,*args,**kwargs):
        super(RQWidgetABC, self).__init__(*args,**kwargs)
        self.resize(1200,800)

        # 注册右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menu_Event)

    def menu_Event(self,pos:QPoint):
        pass


# 标签类
class LabelWidget(RQWidgetABC):
    def __init__(self,*args,**kwargs):
        super(LabelWidget, self).__init__(*args,**kwargs)

    def menu_Event(self,pos:QPoint):
        # 创建菜单
        menu = QMenu()

        keep_controls = menu.addAction("保留控件")
        del_controls = menu.addAction("销毁控件")
        it_type = menu.addAction("标记为其他类型")
        it=QMenu()
        it.addAction(Ct.Input)
        it.addAction(Ct.Button)
        it.addAction(Ct.A)
        it.addAction(Ct.Select)
        it.addAction(Ct.Div)
        it_type.setMenu(it)
        # 显示菜单
        menu.exec_(QCursor.pos())


class PushButton(QPushButton,LabelWidget):
    def __init__(self,*args,**kwargs):
        super(PushButton, self).__init__(*args,**kwargs)


class LineEdit(QLineEdit,LabelWidget):
    def __init__(self,*args,**kwargs):
        super(LineEdit, self).__init__(*args,**kwargs)


class ComboBox(QComboBox,LabelWidget):
    def __init__(self,*args,**kwargs):
        super(ComboBox, self).__init__(*args,**kwargs)


# -------------------------------------
class GroupBox(QGroupBox,RQWidgetABC):
    rightkeyed = pyqtSignal(str)
    ADD = "add"
    DEL = "del"

    def __init__(self,*args,**kwargs):
        super(GroupBox, self).__init__(*args,**kwargs)
        self.resize(100,100)
        self.row_max = 5  # 一行最多 5个
        self.row,self.col = 0,-1

        self.box_glay = QGridLayout(self) # 在操作区内部添加盒子布局
        self.box_glay.setContentsMargins(1,1,1,1)
        self.box_glay.setSpacing(0)

    # 位置
    def getNextPos(self)->tuple:
        if self.col < self.row_max-1:
            self.col += 1
        else:
            self.row+=1
            self.col = 0
        return self.row, self.col

    # 添加xpath 到操作区域
    def addXpathCheckBox(self,xpath:str,isChecked=False,call=None):
        '''
        :param xpath:
        :param isChecked:
        :param call: 回调函数
        :return:
        '''
        xpath = re.sub("^//","",xpath) #  显示的时候,不需要//

        xpath_box = QCheckBox()
        xpath_box.setText(xpath)
        if isChecked:
            xpath_box.setCheckState(Qt.Checked)
        xpath_box.stateChanged.connect(partial(call, xpath_box))
        pos = self.getNextPos()
        print(pos,xpath)
        self.box_glay.addWidget(xpath_box,*pos)

    # 整理布局
    def arrangeLayout(self):
        print(self.box_glay.count())
        print([self.box_glay.itemAt(i) for i in range(self.box_glay.count())])
        for i in range(self.box_glay.count()):
            print(self.box_glay.getItemPosition(i))
        print(self.row, self.col)

        row = self.row*self.row_max
        col = self.col

    # 从操作区移除xpath
    def delXpathCheckBox(self,xpath:str):
        '''
        :param xpath:
        :return:
        '''
        xpath = re.sub("^//", "", xpath)  # 删除的时候,也不需要//
        del_i = None
        for i in range(self.box_glay.count()):
            # print(i)
            item = self.box_glay.itemAt(i)
            if item is None:
                continue

            w_check = item.widget()

            if isinstance(w_check, QCheckBox) and w_check.text() == xpath:
                w_check.stateChanged.disconnect()  # 断开信号连接
                self.box_glay.removeItem(item)  # 移除item
                delete(w_check)  # 删除对象
                del_i = i
                break
            # elif flag:
            #     r,c,_,_ = self.box_glay.getItemPosition(i)
            #     print(r,c)
            #     self.box_glay.addWidget(w_check,r,c)
                # print(w_check,w_check.text(),self.box_glay.getItemPosition(i))
        for i in range(del_i+1,self.box_glay.count()):
            print("ii",i)
            item = self.box_glay.itemAt(i)
            self.box_glay.addWidget(item.widget(),0,3)
            # print(i,self.box_glay.getItemPosition(i))

        # if self.col > 0:
        #     self.col-=1
        # else:
        #     self.row-=1
        #     if self.row < 0:
        #         self.row = 0
        #     self.col = self.row_max-1

        for i in range(self.box_glay.count()):
            print("->",self.box_glay.getItemPosition(i),self.box_glay.itemAt(i).widget().text())


    def menu_Event(self,pos:QPoint):
        # 创建菜单
        menu = QMenu()

        add_xpath = menu.addAction("添加xpath")
        del_xapth = menu.addAction("移除xpath")

        add_xpath.triggered.connect(lambda :self.rightkeyed.emit(self.ADD))
        del_xapth.triggered.connect(lambda :self.rightkeyed.emit(self.DEL))
        # 显示菜单
        menu.exec_(QCursor.pos())

# ----------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = GroupBox()
    win.show()

    sys.exit(app.exec_())