# -*- coding:utf-8 -*-
# @time:2022/11/2911:04
# @author:LX
# @file:sorollWin.py
# @software:PyCharm
from PyQt5.sip import delete
from commonHead import (
    re,
    sys,
    partial,
    QApplication,
    QScrollArea,
    QVBoxLayout,
    QGroupBox,
    QGridLayout,
    QPushButton,
    QWidget,
    QFrame,
    QMenu,
    QCheckBox,
    pyqtSignal,
    QPoint,
    Qt,
    QCursor
)

from LibGui.customize.fflayout import FFLayout
from LibGui.r_controls import RQWidgetABC
# from LibGui.r_controls import GroupBox

'''
    QGroupBox,QScrollArea 组合控件
'''

class SorollWidget(QGroupBox,RQWidgetABC):
    rightkeyed = pyqtSignal(str)
    ADD = "add"
    DEL = "del"

    def __init__(self,*args,**kwargs):
       super(SorollWidget, self).__init__(*args,**kwargs)

       self.resize(800,600)
       self.setObjectName("sorollw")
       self.setStyleSheet('''
#area{
border:none;
}
/*#area_body{
background-color:red;
}*/
QPushButton{
background-color:red;
}
       ''')

       self.row_max = 5  # 一行最多 5个
       self.row, self.col = 0, -1

       self.vlay = QVBoxLayout(self)
       self.vlay.setContentsMargins(0,0,0,0)
       self.vlay.setSpacing(0)

       self.area = QScrollArea()
       self.area.setObjectName("area")
       self.area.setWidgetResizable(True)
       self.area_body = QWidget()
       self.area_body.setObjectName("area_body")
       self.area.setWidget(self.area_body)
       self.vlay.addWidget(self.area)

       self.glay = FFLayout(self.area_body)
       self.glay.setContentsMargins(0,0,0,0)
       self.glay.setSpacing(3)

    # 添加xpath 到操作区域
    def addXpathCheckBox(self,xpath:str,isChecked=False,call=None):
        '''
        :param xpath:
        :param isChecked:
        :param call: 回调函数
        :return:
        '''
        xpath = re.sub("^//","",xpath) #  显示的时候,不需要//

        xpath_box = QCheckBox()
        xpath_box.setText(xpath)
        if isChecked:
            xpath_box.setCheckState(Qt.Checked)
        xpath_box.stateChanged.connect(partial(call, xpath_box))

        self.glay.addWidget(xpath_box)

    def menu_Event(self,pos:QPoint):
        # 创建菜单
        menu = QMenu()

        add_xpath = menu.addAction("添加xpath")
        del_xapth = menu.addAction("移除xpath")

        add_xpath.triggered.connect(lambda :self.rightkeyed.emit(self.ADD))
        del_xapth.triggered.connect(lambda :self.rightkeyed.emit(self.DEL))
        # 显示菜单
        menu.exec_(QCursor.pos())

    # 从操作区移除xpath
    def delXpathCheckBox(self, xpath: str):
        '''
        :param xpath:
        :return:
        '''
        xpath = re.sub("^//", "", xpath)  # 删除的时候,也不需要//

        for w_check in self.glay.allWidget():
            if isinstance(w_check, QCheckBox) and w_check.text() == xpath:
                w_check.stateChanged.disconnect()  # 断开信号连接
                self.glay.removeWidget(w_check)  # 移除布局
                delete(w_check)  # 销毁对象
                break  # 跳出 ,一定要有这句话



if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = SorollWidget()
    win.show()

    sys.exit(app.exec_())