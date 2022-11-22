# -*- coding:utf-8 -*-
# @time:2022/11/2217:40
# @author:LX
# @file:r_controls.py
# @software:PyCharm

import sys
from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication,QPushButton,QLineEdit,QWidget,QMenu,QComboBox


# 让所有渲染的控件都具有右键功能

class RQWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super(RQWidget, self).__init__(*args,**kwargs)
        self.resize(1200,800)

        # 注册右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menu_Event)



    def menu_Event(self,pos:QPoint):
        # 创建菜单
        menu = QMenu()

        copy_name = menu.addAction("复制名称")
        # 显示菜单
        menu.exec_(QCursor.pos())


class PushButton(QPushButton,RQWidget):
    def __init__(self,*args,**kwargs):
        super(PushButton, self).__init__(*args,**kwargs)


class LineEdit(QLineEdit,RQWidget):
    def __init__(self,*args,**kwargs):
        super(LineEdit, self).__init__(*args,**kwargs)


class ComboBox(QComboBox,RQWidget):
    def __init__(self,*args,**kwargs):
        super(ComboBox, self).__init__(*args,**kwargs)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = LineEdit()
    win.show()

    sys.exit(app.exec_())