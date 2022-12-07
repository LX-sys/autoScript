# -*- coding:utf-8 -*-
# @time:2022/11/1917:52
# @author:LX
# @file:RendererWin.py
# @software:PyCharm

import sys
from PyQt5.sip import delete
from core.controlsAttr import ControlsType as Ct
from PyQt5.QtCore import QSize,pyqtSignal,QPoint,Qt
from PyQt5.QtGui import QMouseEvent,QPainter,QColor,QPaintEvent,QPen
from commonHead.Qt.qtWidgets import (
    QApplication,
    QWidget,
    QFrame
)
from .controlFactory import ControlFactory
from .controlsAttrSys import ControlsAttrSys


# 绘制区域(渲染)
'''
    这里需要继承QFrame,QWidget会导致浏览器在QStackedWidget会透视
'''
class RendererWin(QFrame):
    sendToptiped = pyqtSignal(list)  # 发送view上所有显示的标记即属性
    # 被框选中后的颜色
    Select_Color = "background-color: qlineargradient(spread:pad, x1: 0, y1: 0, x2: 1, y2: 1, stop: 0.585227 rgba(98, 192, 255, 80));"

    def  __init__(self,*args,**kwargs):
        super(RendererWin, self).__init__(*args,**kwargs)
        # 控件渲染字典
        '''
            这个字典决定  该控件是否被渲染出来
        '''
        self.render_dict = {"div":False,
                            "a":False,
                            "input":True,
                            "button":True,
                            "select":True}

        self.resize(1200,800)

        # 这四条属性,用于绘制选择区域
        self.LeftDown = False
        self.s_pos = QPoint(0,0)
        self.e_pos = QPoint(0,0)
        self.show_border = False  # 是否显示线框

        # 渲染出控件数据管理系统
        self.c_attr_sys = ControlsAttrSys()

        self.setObjectName("RendererWin")
        self.setStyleSheet('''
*{
color:#fff;
}
#RendererWin{
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

        self.control_factory = ControlFactory()
        attr = {
            "tagName":"button",
            "id":"test",
            "rect":{"w":100,"h":30,"x":50,"y":50},
            "text":"测试"
        }
        self.autoCreate(attr)
        # print(self.desktopSize())
        # self.detectionControls(0,0,0,0)

    # 添加标签
    def addXpath(self,xpath_str,isChecked=False):
        if xpath_str not in self.render_dict:
            self.render_dict[xpath_str] = isChecked
            return True
        return False

    # 移除Xpath
    def delXpath(self,xpath_str):
        if xpath_str in self.render_dict:
            del self.render_dict[xpath_str]
            return True
        return False

    # 通过属性来验证控件的可视类型
    def getVerifyControlType(self,rect:dict):
        final_type = None
        # input标签检测
        if rect["tagName"].lower() == "input":
            final_type = "input"
            if rect.get("type") != None:
                if  rect.get("type") == "submit" \
                    or rect.get("type") == "button" \
                    or rect.get("onclick"):
                    final_type = "button"
        # a标签检测
        if rect["tagName"].lower() == "a":
            final_type = "a"
            if rect.get("onclick"):
                final_type = "button"
            if rect.get("class"):
                if "btn" in rect.get("class").lower():
                    final_type = "button"

        if rect["tagName"].lower() == "button":
            final_type = "button"

        if rect["tagName"].lower() == "label":
            pass

        if rect["tagName"].lower() == "select":
            final_type = "select"

        if rect["tagName"].lower() == "div":
            final_type = "div"

        # print(final_type)
        return final_type

    # 单独设置某个标签是否渲染
    def setControlRender(self,label_name,v:bool):
        if "div" in label_name.lower():  # div特殊对待
            label_name = "div"

        if self.render_dict.get(label_name,None) is not None:
            self.render_dict[label_name] = v

    # 自动创建
    def autoCreate(self,all_attr):
        # 保存属性
        self.c_attr_sys.append(all_attr)

        final_type = self.getVerifyControlType(all_attr) # 验证控件类型

        if final_type == Ct.Input and self.render_dict[final_type]:
            self.control_factory.input(self, all_attr, text=all_attr.get("placeholder", None))
        elif final_type == Ct.Button and self.render_dict[final_type]:
            value = all_attr.get("value", None)
            text = all_attr.get("text", None)
            self.control_factory.button(self, all_attr, text=value if value else text)
        elif final_type == Ct.A and self.render_dict[final_type]:
            self.control_factory.a(self, all_attr, text=all_attr.get("text", None))
        elif final_type == Ct.Select and self.render_dict[final_type]:
            self.control_factory.select(self,all_attr,text=all_attr.get("text", None))
        elif final_type == Ct.Div and self.render_dict[final_type]:
            self.control_factory.div(self, all_attr, text=all_attr.get("text", None))

        # print(final_type,"绘制完成")

    # 返回所有控件
    def __control(self):
        children_c = self.children()

        if not children_c:
            return []
        return children_c

    # 销毁所有控件
    def delAllControl(self):
        for c in self.__control():
            delete(c)

    # 隐藏控件
    def hideControl(self,name):
        for c in self.__control():
            if c.objectName() == name:
                c.hide()

    # 计算view剩余的控件
    def allControl(self):
        temp_list = []
        for c in self.__control():
            '''
                在这里可以获取, 真实代码需要的操作
                比如: 
                    标签是input,但是真实情况是要当按钮来操作,那么这里就能获取到按钮
            '''
            temp_list.append(c.toolTip())

        # 发送 toptip
        self.sendToptiped.emit(temp_list)

    # 等比例缩放
    def scale(self,browser_size:QSize, rect: dict):
        '''

        :param browser_size: 浏览器大小
        :param rect: 元素的 宽高,位置
        :return:
        '''
        if browser_size is None:
            browser_w,browser_h = self.desktopSize()
        else:
            browser_w,browser_h = browser_size.width(),browser_size.height()
        page_area_w = self.width()
        page_area_h = self.height()

        w_minification = round(page_area_w / browser_w, 2)
        h_minification = round(page_area_h / browser_h, 2)
        return {"w": int(rect["w"] * w_minification),
                "h": int(rect["h"] * h_minification),
                "x": int(rect["x"] * w_minification),
                "y": int(rect["y"] * h_minification)
                }

    # 获取屏幕大小
    def desktopSize(self):
        d_size = QApplication.desktop().size()
        count = QApplication.desktop().screenCount()
        return d_size.width()//count,d_size.height()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.LeftButton: # 鼠标左键按下
            self.LeftDown = True
            self.s_pos = e.pos()
        super(RendererWin, self).mousePressEvent(e)

    # 检测框选范围内的渲染控件
    def detectionControls(self):
        if self.s_pos.x() > self.e_pos.x() and self.s_pos.y() > self.e_pos.y():
            self.s_pos,self.e_pos = self.e_pos,self.s_pos

        x, y = self.s_pos.x(), self.s_pos.y()
        w, h = self.e_pos.x() - x, self.e_pos.y() - y

        for c in self.__control():
            tx,ty = c.pos().x(),c.pos().y()
            old_style = c.styleSheet()  # 还原样式
            if tx > x and tx< w+x and ty > y and ty <h+y:
                style = c.styleSheet()
                # .... 其他操作

                # ....
                if self.Select_Color not in style:
                    style += self.Select_Color
                c.setStyleSheet(style)
            else:
                if self.Select_Color in old_style:
                    old_style = old_style.replace(self.Select_Color,"")
                c.setStyleSheet(old_style)

        if self.show_border is False:
            self.update()

    # 渲染视图
    def render_view(self,browser,is_del=True):
        if not browser.url().toString():
            return

        if is_del:
            self.delAllControl()

        self.c_attr_sys.clear()

        # 绘制控件
        def call(x:list):
            for all_attr in x:
                all_attr["rect"] = self.scale(browser.size(),all_attr["rect"]) # 缩放,修改参数
                self.autoCreate(all_attr)
        # 渲染
        for _xpath,check in self.render_dict.items():
            if self.render_dict.get("div" if "div" in _xpath else _xpath,None):# 先判断控件是否需要渲染
                _xpath = "//"+_xpath
                if check:
                    browser.xpath(_xpath,lambda x:call(x))

    def mouseReleaseEvent(self, e:QMouseEvent) -> None:
        self.LeftDown = False
        # 鼠标左键弹起时检测
        self.detectionControls()
        super(RendererWin, self).mouseReleaseEvent(e)

    def paintEvent(self, e: QPaintEvent) -> None:
        if self.LeftDown:
            painter = QPainter()
            painter.begin(self)
            open_ = QPen()
            open_.setColor(QColor(182, 182, 182))
            open_.setStyle(Qt.DashDotLine)
            painter.setPen(open_)
            x,y = self.s_pos.x(),self.s_pos.y()
            w,h = self.e_pos.x()-x,self.e_pos.y()-y
            painter.drawRect(x,y,w,h)
            painter.end()

    def mouseMoveEvent(self, e:QMouseEvent) -> None:
        if self.LeftDown:
            self.e_pos = e.pos()
            self.update()
        super(RendererWin, self).mouseMoveEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = RendererWin()
    win.show()

    sys.exit(app.exec_())