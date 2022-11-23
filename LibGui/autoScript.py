# -*- coding: utf-8 -*-


import os
from functools import partial
import sys
import math
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QStackedWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextBrowser,
    QGroupBox,
    QGridLayout,
    QCheckBox,
    QInputDialog
)
from bs4 import BeautifulSoup
from LibGui.loadBrowser import Browser
from LibGui.RendererWin import RendererWin
from core.writeCode import WriteCode
from LibGui.r_controls import GroupBox
'''
    自动写代码训练机 主界面
'''

class AutoScript(QStackedWidget):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)

        # 待渲染的标题
        '''
            渲染顺序
            div > 所有
        '''
        self.setWindowTitle("ACode")
        # 写代码类
        self.w_code = WriteCode()

        # 初始化 绘制窗口的时候,会调用渲染函数,需要阻止
        self.init_size_rander = False

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
#render{
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
border-radius:4px;
font: 10pt "等线";
}
#write_code_btn{
border:1px solid rgb(0, 232, 0);
color: rgb(255, 255, 255);
font: 10pt "等线";
border-radius:4px;
}
#render_btn:hover,#url_submit:hover,#write_code_btn:hover{
border-width:2px;
}
#box{
border:1px solid rgb(0, 170, 255);
}
#box #QCheckBox{
font: 9pt "等线";
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
        # self.render = QtWidgets.QWidget()
        self.render = RendererWin()
        self.render.setObjectName("render")
        self.area_draw.addWidget(self.render)
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
        self.code_win.append(code)
        # self.code_win.setText(code)  # 这个函数在mac运行没事,在win大概率会卡死

    # 代码区域
    def code_area(self):
        print(self.code_win)

    # 绘图区域
    def draw(self):
        print(self.area_draw)

    # 操作区域
    def operation(self):
        # url
        self.url_line = QLineEdit(self.page_op)
        self.url_line.setText("https://www.baidu.com/")
        self.url_line.setObjectName("url_line")
        self.url_line.setPlaceholderText("输入Url")
        self.url_line.setGeometry(10,10,250,30)
        self.url_submit = QPushButton("访问",self.page_op)
        self.url_submit.setObjectName("url_submit")
        self.url_submit.setGeometry(265,10,80,30)

        # 重新渲染按钮
        self.render_btn = QPushButton("重新渲染",self.page_op)
        self.render_btn.setObjectName("render_btn")
        self.render_btn.setGeometry(375,10,90,30)
        self.render_btn.clicked.connect(lambda :self.render.render_view(self.browser))

        # 生成自动化代码
        self.write_code_btn =QPushButton("生成代码",self.page_op)
        self.write_code_btn.setObjectName("write_code_btn")
        self.write_code_btn.setGeometry(490,10,90,30)
        self.write_code_btn.clicked.connect(self.w_code_event)

        # 标签操作区域
        self.box = GroupBox(self.page_op)
        self.box.setTitle("标签区")
        self.box.setFixedSize(600,150)
        self.box.setObjectName("box")
        self.box.move(10,45)
        self.box_glay = QGridLayout(self.box) # 在操作区内部添加盒子布局
        self.box_glay.setContentsMargins(1,1,1,1)
        self.box_glay.setSpacing(0)

        # 默认所有标签都勾选
        for xpath,check in self.render.render_dict.items():
            self.addXpathCheckBox(xpath,check)

    # 添加xpath 到操作区域
    def addXpathCheckBox(self,xpath:str,isChecked=False):
        xpath_box = QCheckBox()
        xpath_box.setText(xpath)
        if isChecked:
            xpath_box.setCheckState(Qt.Checked)
        xpath_box.stateChanged.connect(partial(self.render_state, xpath_box))
        self.box_glay.addWidget(xpath_box)

    # 从操作区移除xpath
    def delXpathCheckBox(self,xpath:str):
        for check in [self.box_glay.itemAt(i) for i in range(self.box_glay.count())]:
            w_check = check.widget()
            if isinstance(w_check,QCheckBox) and w_check.text() == xpath:
                w_check.stateChanged.disconnect()  # 断开信号连接
                self.box_glay.removeItem(check)  # 移除布局
                w_check.deleteLater()  # 删除对象

    # 生成代码事件
    def w_code_event(self):
        self.render.allControl()

    # 标签的渲染状态
    def render_state(self,obj:QCheckBox):
        label_name = obj.text()
        self.render.setControlRender(label_name,True if obj.checkState() > 0 else False)
        if self.init_size_rander: # 初始不渲染
            self.render.render_view(self.browser)


    def url_event(self):
        self.init_size_rander = True # 可以渲染

        self.url_submit.setText("访问中")
        self.browser.get(self.url_line.text())
        self.browser.show()

    # 下载html源码
    def down_html(self,html):
        self.url_submit.setText("访问完成")
        self.render.render_view(self.browser)  # 首次渲染

    # 接收所有label即属性,进行分析,生成代码
    def toptip_event(self,labels:list):
        # 逐句分析
        for l in labels:
            code = self.w_code.wCode(self.w_code.labelAnalysis(l))
            if code:
                self.writeCode(code)

    # 操作区右键信号事件
    def operation_right(self,model:str):
        if model == self.box.ADD:
            xpath,ok=QInputDialog.getText(None,"添加","输入xpath",QLineEdit.Normal,"")
            if ok and xpath:
                if xpath[:2] == "//":
                    xpath = xpath[2:]
                if self.render.addXpath(xpath):
                    self.addXpathCheckBox(xpath)

        if model == self.box.DEL:
            xpath, ok = QInputDialog.getText(None, "删除", "输入xpath", QLineEdit.Normal, "")
            if ok and xpath:
                if xpath[:2] == "//":
                    xpath = xpath[2:]
                if self.render.delXpath(xpath):
                    self.delXpathCheckBox(xpath)
                    # 移除完成之后,重新渲染一次
                    self.render.render_view(self.browser)

    def myEvent(self):
        self.url_submit.clicked.connect(self.url_event)
        self.browser.contented.connect(self.down_html)

        self.render.sendToptiped.connect(self.toptip_event)

        # 操作区右键信号
        self.box.rightkeyed.connect(self.operation_right)

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        if self.init_size_rander:
            self.render.render_view(self.browser)
        super(AutoScript, self).resizeEvent(e)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = AutoScript()
    win.show()

    sys.exit(app.exec_())
    