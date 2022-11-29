# -*- coding:utf-8 -*-
# @time:2022/11/2217:40
# @author:LX
# @file:r_controls.py
# @software:PyCharm
from core.controlsAttr import ControlsType as Ct
from commonHead import (
    re,
    sys,
    QApplication,
    QPushButton,
    QLineEdit,
    QWidget,
    QMenu,
    QGroupBox,
    QCheckBox,
    QGridLayout,
    QComboBox,
    QCursor,
    Qt,
    QPoint,
    pyqtSignal
)
# 让所有渲染的控件都具有右键功能的基类
class RQWidgetABC(QWidget):
    def __init__(self,*args,**kwargs):
        super(RQWidgetABC, self).__init__(*args,**kwargs)
        self.resize(1200,800)

        # 注册右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menu_Event)

    def menu_Event(self,pos:QPoint):
        pass


# 标签类
class LabelWidget(RQWidgetABC):
    def __init__(self,*args,**kwargs):
        super(LabelWidget, self).__init__(*args,**kwargs)

    def menu_Event(self,pos:QPoint):
        # 创建菜单
        menu = QMenu()

        keep_controls = menu.addAction("保留控件")
        del_controls = menu.addAction("销毁控件")
        it_type = menu.addAction("标记为其他类型")
        it=QMenu()
        it.addAction(Ct.Input)
        it.addAction(Ct.Button)
        it.addAction(Ct.A)
        it.addAction(Ct.Select)
        it.addAction(Ct.Div)
        it_type.setMenu(it)
        # 显示菜单
        menu.exec_(QCursor.pos())


class PushButton(QPushButton,LabelWidget):
    def __init__(self,*args,**kwargs):
        super(PushButton, self).__init__(*args,**kwargs)


class LineEdit(QLineEdit,LabelWidget):
    def __init__(self,*args,**kwargs):
        super(LineEdit, self).__init__(*args,**kwargs)


class ComboBox(QComboBox,LabelWidget):
    def __init__(self,*args,**kwargs):
        super(ComboBox, self).__init__(*args,**kwargs)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ComboBox()
    win.show()

    sys.exit(app.exec_())