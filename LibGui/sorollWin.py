# -*- coding:utf-8 -*-
# @time:2022/11/2911:04
# @author:LX
# @file:sorollWin.py
# @software:PyCharm

import re
import sys
from functools import partial
from PyQt5.sip import delete
from commonHead.Qt.qtCore import pyqtSignal,QPoint,Qt
from PyQt5.QtGui import QCursor
from commonHead.Qt.qtWidgets import (
    QApplication,
    QScrollArea,
    QVBoxLayout,
    QGroupBox,
    QGridLayout,
    QPushButton,
    QWidget,
    QMenu,
    QCheckBox
)
from LibGui.r_controls import RQWidgetABC
from LibGui.r_controls import GroupBox

'''
    QGroupBox,QScrollArea 组合控件
'''

class SorollWidget(QGroupBox,RQWidgetABC):
    rightkeyed = pyqtSignal(str)
    ADD = "add"
    DEL = "del"

    def __init__(self,*args,**kwargs):
       super(SorollWidget, self).__init__(*args,**kwargs)
       self.resize(800,600)

       self.row_max = 5  # 一行最多 5个
       self.row, self.col = 0, -1

       self.vlay = QVBoxLayout(self)
       self.vlay.setContentsMargins(0,0,0,0)
       self.vlay.setSpacing(0)

       self.area = QScrollArea()
       self.area.setWidgetResizable(True)
       self.area_body = QWidget()
       self.area.setWidget(self.area_body)
       self.vlay.addWidget(self.area)

       self.glay = QGridLayout(self.area_body)
       self.glay.setContentsMargins(0,0,0,0)
       self.glay.setSpacing(6)


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
        self.glay.addWidget(xpath_box,*pos)

    def menu_Event(self,pos:QPoint):
        # 创建菜单
        menu = QMenu()

        add_xpath = menu.addAction("添加xpath")
        del_xapth = menu.addAction("移除xpath")

        add_xpath.triggered.connect(lambda :self.rightkeyed.emit(self.ADD))
        del_xapth.triggered.connect(lambda :self.rightkeyed.emit(self.DEL))
        # 显示菜单
        menu.exec_(QCursor.pos())

        # 从操作区移除xpath

    def delXpathCheckBox(self, xpath: str):
        '''
        :param xpath:
        :return:
        '''
        xpath = re.sub("^//", "", xpath)  # 删除的时候,也不需要//
        del_i = None
        for i in range(self.glay.count()):
            # print(i)
            item = self.glay.itemAt(i)
            if item is None:
                continue

            w_check = item.widget()

            if isinstance(w_check, QCheckBox) and w_check.text() == xpath:
                w_check.stateChanged.disconnect()  # 断开信号连接
                self.glay.removeItem(item)  # 移除item
                delete(w_check)  # 删除对象
                del_i = i
                break
            # elif flag:
            #     r,c,_,_ = self.box_glay.getItemPosition(i)
            #     print(r,c)
            #     self.box_glay.addWidget(w_check,r,c)
            # print(w_check,w_check.text(),self.box_glay.getItemPosition(i))
        for i in range(del_i + 1, self.glay.count()):
            print("ii", i)
            item = self.glay.itemAt(i)
            self.glay.addWidget(item.widget(), 0, 3)
            # print(i,self.box_glay.getItemPosition(i))

        # if self.col > 0:
        #     self.col-=1
        # else:
        #     self.row-=1
        #     if self.row < 0:
        #         self.row = 0
        #     self.col = self.row_max-1

        for i in range(self.glay.count()):
            print("->", self.glay.getItemPosition(i), self.glay.itemAt(i).widget().text())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = SorollWidget()
    win.show()

    sys.exit(app.exec_())