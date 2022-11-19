# -*- coding: utf-8 -*-


import os
import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class AutoScript(QStackedWidget):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.setupUi()
    
    def setupUi(self):
        self.setObjectName("st_win")
        self.resize(1235, 844)
        self.setStyleSheet('''
*{
background-color: rgb(33, 33, 33);
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
        self.page_area = QtWidgets.QWidget()
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
        self.code_win = QtWidgets.QWidget(self.page)
        self.code_win.setMinimumSize(QtCore.QSize(501, 0))
        self.code_win.setMaximumSize(QtCore.QSize(501, 16777215))
        self.code_win.setObjectName("code_win")
        self.horizontalLayout.addWidget(self.code_win)
        self.addWidget(self.page)

        self.retranslateUi()
        self.area_draw.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    # 代码区域
    def code_area(self):
        print(self.code_win)

    # 绘图区域
    def draw(self):
        print(self.area_draw)

    # 操作区域
    def operation(self):
        print(self.operation_area)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "StackedWidget"))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = AutoScript()
    win.show()

    sys.exit(app.exec_())
    