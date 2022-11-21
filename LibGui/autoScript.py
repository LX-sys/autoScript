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

        # 待渲染的标题
        self.render_labels = ["input","a","button","select"]

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
#url_submit{
border:1px solid #009688;
font: 10pt "等线";
color: rgb(255, 255, 255);
}
#render_btn{
background-color: rgb(62, 62, 62);
border:1px solid rgb(3, 158, 255);
color:rgb(255, 255, 255);
border-radius:5px;
font: 10pt "等线";
}
#render_btn:hover,#url_submit:hover{
border-width:2px;
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
        pass
        # print(code)
        # self.code_win.append(code)
        # self.code_win.setText(code)  # 这个函数在mac运行没事,在win大概率会卡死

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
        self.url_submit.setGeometry(265,10,80,30)

        # 重新渲染按钮
        self.render_btn = QPushButton("重新渲染",self.page_op)
        self.render_btn.setObjectName("render_btn")
        self.render_btn.setGeometry(375,10,100,30)

        self.render_btn.clicked.connect(self.render_view)

    # 等比例缩放
    def scale(self,rect:dict):
        '''
        1920, 1080
        734, 633

        {'h': 44, 'w': 550, 'x': 633, 'y': 259.1875}
        {'h': 44, 'w': 108, 'x': 1179, 'y': 259.1875}
        :return:
        '''
        browser_w = self.browser.size().width()
        browser_h = self.browser.size().height()
        page_area_w = self.page_area.size().width()
        page_area_h = self.page_area.size().height()

        w_minification = round(page_area_w/browser_w,2)
        h_minification = round(page_area_h/browser_h,2)
        # print(w_minification,h_minification)
        return {"w":round(rect["w"]*w_minification,2),
                "h": round(rect["h"] * h_minification, 2),
                "x": round(rect["x"] * w_minification, 2),
                "y": round(rect["y"] * h_minification, 2)
                }

    # 渲染视图
    def render_view(self):
        self.page_area.delControl()

        # 绘制控件
        def call(x:list,pa):
            for all_attr in x:
                rect = all_attr["rect"]
                all_attr["rect"] = self.scale(rect) # 缩放,修改参数
                pa.autoCreate(all_attr)
                print(all_attr)

        # 渲染
        for label in self.render_labels:
            label = "//"+label
            self.browser.xpath(label,lambda x:call(x,self.page_area))


    def url_event(self):
        self.url_submit.setText("访问中")
        self.browser.get(self.url_line.text())
        self.browser.show()

    # 下载html源码
    def down_html(self,html):
        self.url_submit.setText("访问完成")
        # self.writeCode(html)
        # self.bs4_html = BeautifulSoup(html, "html.parser")
        self.render_view()


    def myEvent(self):
        self.url_submit.clicked.connect(self.url_event)
        self.browser.contented.connect(self.down_html)

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        print(e.size())
        self.render_view()
        super(AutoScript, self).resizeEvent(e)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "StackedWidget"))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = AutoScript()
    win.show()

    sys.exit(app.exec_())
    