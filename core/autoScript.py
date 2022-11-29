# -*- coding: utf-8 -*-



import sys
from PyQt5.QtGui import QResizeEvent
from commonHead.Qt.qtWidgets import (
    QApplication,
    QLineEdit,
    QCheckBox,
    QInputDialog
)
from LibGui.loadBrowser import Browser
from core.writeCode import WriteCode
from LibGui.UI.autoScriptUI import AutoScriptUI

'''
    自动写代码训练机 主界面
'''

class AutoScript(AutoScriptUI):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)

        # 初始化 绘制窗口的时候,会调用渲染函数,需要阻止
        self.init_size_rander = False

        # 写代码类
        self.w_code = WriteCode()
        self.browser = Browser()

        self.addWidget(self.browser)
        self.myEvent()

        self.Init()

    def Init(self):
        # 默认所有标签都勾选
        for xpath, check in self.render.render_dict.items():
            self.box.addXpathCheckBox(xpath, check, self.render_state)

    def writeCode(self,code:str):
        self.code_win.append(code)
        # self.code_win.setText(code)  # 这个函数在mac运行没事,在win大概率会卡死

    # 代码区域
    def code_area(self):
        print(self.code_win)

    # 绘图区域
    def draw(self):
        print(self.area_draw)

    # 生成代码事件
    def w_code_event(self):
        self.render.allControl()

    # 标签的渲染状态
    def render_state(self,obj:QCheckBox):
        label_name = obj.text()
        self.render.setControlRender(label_name,True if obj.checkState() > 0 else False)
        if self.init_size_rander: # 初始不渲染
            self.render.render_view(self.browser)

    def url_event(self):
        self.init_size_rander = True # 可以渲染

        self.url_submit.setText("访问中")
        self.browser.get(self.url_line.text())
        self.browser.show()

    # 下载html源码
    def down_html(self,html):
        self.url_submit.setText("访问完成")
        self.render.render_view(self.browser)  # 首次渲染

    # 接收所有label即属性,进行分析,生成代码
    def toptip_event(self,labels:list):
        # 逐句分析
        for l in labels:
            code = self.w_code.wCode(self.w_code.labelAnalysis(l))
            if code:
                self.writeCode(code)

    # 操作区右键信号事件
    def operation_right(self,model:str):

        xpath, ok = QInputDialog.getText(None, "添加/删除", "输入xpath", QLineEdit.Normal, "")

        if ok and xpath:
            if model == self.box.ADD:
                if self.render.addXpath(xpath):
                    self.box.addXpathCheckBox(xpath,False,self.render_state)

            if model == self.box.DEL:
                if self.render.delXpath(xpath):
                    self.box.delXpathCheckBox(xpath)
                    # 移除完成之后,重新渲染一次
                    self.render.render_view(self.browser)

    def myEvent(self):
        # 生成代码事件
        self.write_code_btn.clicked.connect(self.w_code_event)

        # 重绘窗口
        self.render_btn.clicked.connect(lambda: self.render.render_view(self.browser))

        # 访问url
        self.url_submit.clicked.connect(self.url_event)
        self.browser.contented.connect(self.down_html) # 浏览器加载完成事件

        self.render.sendToptiped.connect(self.toptip_event)

        # 操作区右键信号
        self.box.rightkeyed.connect(self.operation_right)

    def resizeEvent(self, e: QResizeEvent) -> None:
        if self.init_size_rander:
            self.render.render_view(self.browser)
        super(AutoScript, self).resizeEvent(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = AutoScript()
    win.show()

    sys.exit(app.exec_())
    