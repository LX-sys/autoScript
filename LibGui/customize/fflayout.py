# -*- coding:utf-8 -*-
# @time:2022/12/814:08
# @author:LX
# @file:fflayout.py
# @software:PyCharm

from commonHead import (
    sys,
    QApplication,
    QWidget,
    QPushButton,
    QResizeEvent,
    QGridLayout,
    QWidgetItem
)
from PyQt5.sip import delete
from functools import partial


# 流式布局
class FFLayout(QGridLayout):
    def __init__(self,*args,**kwargs):
        super(FFLayout, self).__init__(*args,**kwargs)

        self.col_max = 5
        self.row,self.col = 0,0

    # 设置一行最多几个
    def setColMaxNumber(self,number:int):
        self.col_max = number

    def addWidget(self, w: QWidget,*args) -> None:
        if self.col > self.col_max:
            self.row += 1
            self.col = 0
        super(FFLayout, self).addWidget(w,self.row,self.col)
        self.col += 1
    
    def removeWidget(self, w: QWidget) -> None:
        super(FFLayout, self).removeWidget(w)
        self.againLayout()

    def allWidgetItem(self)->[QWidgetItem]:
        return [self.itemAt(i) for i in range(self.count())]

    def allWidget(self)->[QWidget]:
        return [w.widget() for w in self.allWidgetItem()]

    # 将所有控件重新布局(这个方法是流式布局最暴力的解法)
    def againLayout(self):
        self.row,self.col = 0,0
        for w in self.allWidget():
            self.addWidget(w)


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super(Test, self).__init__(*args,**kwargs)
        self.resize(600,300)
        
        self.ll = []
        self.f = FFLayout(self)

        for i in range(15):
            b = QPushButton("dsa_{}".format(i))
            b.clicked.connect(partial(self.d_event,b))
            self.ll.append(b)
            self.f.addWidget(b)

    def d_event(self,b:QPushButton):
        print("b=",b.text())

        c =None
        for i in self.ll:
            if i.text() == b.text():
                c = i
                break
        p = self.ll.pop(self.ll.index(c))
        self.f.removeWidget(p)
        delete(p)




if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    sys.exit(app.exec_())