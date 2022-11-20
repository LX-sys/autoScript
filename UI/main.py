# -*- coding: utf-8 -*-


import os
import sys
import math
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QStackedWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextBrowser
)
from bs4 import BeautifulSoup
from LibGui.loadBrowser import Browser
from LibGui.areaWin import AreaWin


class AutoScript(QStackedWidget):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.browser = Browser()
        self.setupUi()
        self.myEvent()
    
    def setupUi(self):
        self.setObjectName("st_win")
        self.resize(1235, 844)
        self.setStyleSheet('''
*{
background-color: rgb(33, 33, 33);
color:#fff;
}
#code_win{
border-left:2px solid #455A64;
background-color: #212121;
}
#page_area{
background-color:transparent;
}
#operation_area{
border-top:2px solid #009688;
background-color:transparent;
}
#url_submit,#testbtn{
border:1px solid #009688;
}
        ''')
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.page)
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.page)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.area_draw = QtWidgets.QStackedWidget(self.widget)
        self.area_draw.setObjectName("area_draw")
        # self.page_area = QtWidgets.QWidget()
        self.page_area = AreaWin()
        self.page_area.setObjectName("page_area")
        self.area_draw.addWidget(self.page_area)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.area_draw.addWidget(self.page_3)
        self.verticalLayout.addWidget(self.area_draw)
        self.operation_area = QtWidgets.QStackedWidget(self.widget)
        self.operation_area.setMinimumSize(QtCore.QSize(0, 211))
        self.operation_area.setMaximumSize(QtCore.QSize(16777215, 211))
        self.operation_area.setObjectName("operation_area")
        self.page_op = QtWidgets.QWidget()
        self.page_op.setObjectName("page_op")
        self.operation_area.addWidget(self.page_op)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.operation_area.addWidget(self.page_5)
        self.verticalLayout.addWidget(self.operation_area)
        self.horizontalLayout.addWidget(self.widget)
        # self.code_win = QtWidgets.QWidget(self.page)
        self.code_win = QTextBrowser(self.page)
        self.code_win.setMinimumSize(QtCore.QSize(501, 0))
        self.code_win.setMaximumSize(QtCore.QSize(501, 16777215))
        self.code_win.setObjectName("code_win")
        self.horizontalLayout.addWidget(self.code_win)
        self.addWidget(self.page)

        self.retranslateUi()
        self.area_draw.setCurrentIndex(0)
        self.addWidget(self.browser)
        self.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        # ---
        self.code_area()
        self.draw()
        self.operation()

    def writeCode(self,code:str):
        # self.code_win.append(code)
        self.code_win.setText(code)

    # 代码区域
    def code_area(self):
        print(self.code_win)

    # 绘图区域
    def draw(self):
        print(self.area_draw)

    # 操作区域
    def operation(self):
        print(self.operation_area)
        # url
        self.url_line = QLineEdit(self.page_op)
        self.url_line.setText("https://www.baidu.com/")
        self.url_line.setObjectName("url_line")
        self.url_line.setPlaceholderText("Url")
        self.url_line.setGeometry(10,10,250,30)
        self.url_submit = QPushButton("访问",self.page_op)
        self.url_submit.setObjectName("url_submit")
        self.url_submit.setGeometry(265,10,40,30)

        # test按钮
        self.testbtn = QPushButton("input",self.page_op)
        self.testbtn.setObjectName("testbtn")
        self.testbtn.setGeometry(330,10,40,30)

        self.testbtn.clicked.connect(self.test_event)

    def test_event(self):

        def call(x:list,pa):
            for con in x:
                rect = con["rect"]
                print(rect)
                pa.drawLine(rect["w"],rect["h"],abs(rect["x"]), abs(rect["y"]))
            self.setCurrentIndex(1)


        self.browser.xpath("//input",lambda x:call(x,self.page_area))


    def url_event(self):
        self.browser.get(self.url_line.text())

    # 下载html源码
    def down_html(self,html):
        self.writeCode(html)
        self.bs4_html = BeautifulSoup(html, "html.parser")


    def myEvent(self):
        self.url_submit.clicked.connect(self.url_event)
        self.browser.contented.connect(self.down_html)



    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "StackedWidget"))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = AutoScript()
    win.show()

    sys.exit(app.exec_())
    