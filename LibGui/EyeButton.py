# -*- coding:utf-8 -*-
# @time:2022/11/3017:36
# @author:LX
# @file:EyeButton.py
# @software:PyCharm

from commonHead import (
    sys,
    QApplication,
    QWidget,
    QPushButton,
    QMouseEvent,
    pyqtSignal
)
'''
    鼠标按下去之后,松开立刻回弹
'''


class Eye(QPushButton):
    springback = pyqtSignal(bool)

    def __init__(self,*args,**kwargs):
        super(Eye, self).__init__(*args,**kwargs)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.springback.emit(True)
        super(Eye, self).mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self.springback.emit(False)
        super(Eye, self).mouseReleaseEvent(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Eye()
    win.show()

    sys.exit(app.exec_())