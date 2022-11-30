# -*- coding:utf-8 -*-
# @time:2022/11/3016:28
# @author:LX
# @file:test_brower.py
# @software:PyCharm


from commonHead import (
    sys,
    QApplication,
    QStackedWidget,
    QWidget
)
from LibGui.loadBrowser import Browser
from core.Render.RendererWin import RendererWin

class TestSt(QStackedWidget):
    def __init__(self):
        super(TestSt, self).__init__()
        self.resize(800,600)

        self.setStyleSheet('''
#frist{
background-color:red;
}
        ''')

        self.frist = RendererWin()
        self.b = Browser()
        # self.frist.setObjectName("frist")
        self.addWidget(self.frist)
        self.addWidget(self.b)

        self.b.get("https://www.baidu.com/")
        self.b.show()

        self.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = TestSt()
    win.show()

    sys.exit(app.exec_())