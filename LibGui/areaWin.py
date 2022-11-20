# -*- coding:utf-8 -*-
# @time:2022/11/1917:52
# @author:LX
# @file:areaWin.py
# @software:PyCharm

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit


# 绘制区域
class AreaWin(QWidget):
    def  __init__(self,*args,**kwargs):
        super(AreaWin, self).__init__(*args,**kwargs)

        self.resize(1200,800)
        self.setObjectName("AreaWin")
        self.setStyleSheet('''
*{
color:#fff;
}
#AreaWin{
background-color: rgb(33, 33, 33);
}
QPushButton{
border:1px solid rgb(35, 105, 255);
}
QPushButton:hover{
border-width:2px;
}
QLineEdit{
border:1px solid rgb(131, 131, 0);
background-color:transparent;
}
QLineEdit:hover{
border-width:2px;
}
        ''')

        # self.drawButton("text",30,40)
        # self.drawLine(550,44,633, 222)
        print(self.desktopSize())

    # 获取屏幕大小
    def desktopSize(self):
        d_size = QApplication.desktop().size()
        count = QApplication.desktop().screenCount()
        return d_size.width()//count,d_size.height()

    def drawButton(self,text,h,w,x,y):
        t = QPushButton(text,self)
        t.resize(h,w)
        t.move(x,y)

    def drawLine(self,w,h, x, y):
        t = QLineEdit(self)
        t.resize(w,h)
        t.setStyleSheet('''
border:1px solid rgb(131, 131, 0);
background-color:transparent;
        ''')
        t.setPlaceholderText("input")
        t.move(x, y)
        t.show()
        print("绘制完成")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = AreaWin()
    win.show()

    sys.exit(app.exec_())