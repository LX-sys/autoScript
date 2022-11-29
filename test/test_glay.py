
import sys
from PyQt5.sip import delete
from commonHead.Qt.qtWidgets import QApplication,QGridLayout,QWidget,QPushButton

'''
    测试 QGridLayout 布局
'''

class TestGird(QWidget):
    def __init__(self):
        super(TestGird, self).__init__()
        self.resize(800,600)

        self.lay = QGridLayout(self)

        self.col_max = 5
        self.row,self.col = 0,-1

        a = QPushButton("A")
        a.setFixedSize(100, 30)
        self.lay.addWidget(a, 0, 0)

        b = QPushButton("B")
        b.setFixedSize(100,30)
        self.lay.addWidget(b,0,1)

        c = QPushButton("C")
        c.setFixedSize(100,30)
        self.lay.addWidget(c,0,2)

        self.lay.removeWidget(b)
        self.lay.addWidget(c,0,1)


        for i in range(self.lay.count()):
            print("->",self.lay.getItemPosition(i))


    def nextPos(self):
        if self.col < self.col_max-1:
            self.col += 1
        else:
            self.row+=1
            self.col=0
        return self.row,self.col

    def addBtn(self,text):
        b = QPushButton(text)
        b.setFixedSize(100,30)
        pos = self.nextPos()
        print("{} -> {}".format(text,pos))
        b.clicked.connect(lambda :self.btn_remove(text))
        self.lay.addWidget(b,*pos)


    def btn_remove(self,text):
        for i in range(self.lay.count()):
            item = self.lay.itemAt(i)
            if item:
                w = item.widget()
                if w.text() == text:
                    w.clicked.disconnect()
                    print(w.text(),self.lay.getItemPosition(i))
                    self.lay.removeItem(item)
                    delete(w)
        print("--------->")
        for i in range(self.lay.count()):
            print("->",self.lay.getItemPosition(i))
        print("=========>")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = TestGird()
    win.show()

    sys.exit(app.exec_())