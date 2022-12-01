# -*- coding:utf-8 -*-
# @time:2022/11/3016:28
# @author:LX
# @file:test_brower.py
# @software:PyCharm


import sys
from PyQt5.QtWidgets import QWidget,QApplication
from PyQt5.QtGui import QMouseEvent

class TestSt(QWidget):
    def __init__(self):
        super(TestSt, self).__init__()
        self.resize(800,600)


    def mousePressEvent(self, e: QMouseEvent) -> None:
        # 这里自己判断鼠标的按键
        self.close()
        super(TestSt, self).mousePressEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = TestSt()
    win.show()

    sys.exit(app.exec_())