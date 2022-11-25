# -*- coding:utf-8 -*-
# @time:2022/11/2217:40
# @author:LX
# @file:r_controls.py
# @software:PyCharm

import sys
from functools import partial
from PyQt5.sip import delete
from PyQt5.QtCore import Qt,QPoint,pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication,QPushButton,QLineEdit,QWidget,QMenu,QComboBox,QGroupBox,QCheckBox
from core.controlsAttr import ControlsType as Ct

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

    # 位置
    def getNextPos(self)->tuple:
        self.col+=1
        if self.col < self.row_max:
            print(self.row,self.col)
            return self.row,self.col
        else:
            print("==")
            self.row+=1
            self.col = 0
            return self.row, self.col

    # 添加xpath 到操作区域
    def addXpathCheckBox(self,box_glay,xpath:str,isChecked=False,call=None):
        '''
        :param box_glay:布局容器
        :param xpath:
        :param isChecked:
        :param call: 回调函数
        :return:
        '''
        xpath_box = QCheckBox()
        xpath_box.setText(xpath)
        if isChecked:
            xpath_box.setCheckState(Qt.Checked)
        xpath_box.stateChanged.connect(partial(call, xpath_box))
        box_glay.addWidget(xpath_box,*self.getNextPos())

    # 从操作区移除xpath
    def delXpathCheckBox(self,box_glay,xpath:str):
        '''

        :param box_glay: 布局容器
        :param xpath:
        :return:
        '''
        flag = False
        for check in [box_glay.itemAt(i) for i in range(box_glay.count())]:
            w_check = check.widget()
            if isinstance(w_check,QCheckBox) and w_check.text() == xpath:
                w_check.stateChanged.disconnect()  # 断开信号连接
                box_glay.removeItem(check)  # 移除布局
                delete(w_check) # 删除对象
                flag = True
            elif flag:
                print(w_check,w_check.text())
                # w_check.deleteLater()
        # if self.col >-1:
        #     self.col-=1  # 位置-1
        #     if self.col == -1:
        #         self.row-=1
        #         self.col = 4


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