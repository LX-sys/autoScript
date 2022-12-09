from core.Render.RendererWin import RendererWin
from LibGui.sorollWin import SorollWidget
from LibGui.EyeButton import Eye
from commonHead import (
    sys,
    QApplication,
    QStackedWidget,
    QPushButton,
    QLineEdit,
    QTextBrowser,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSize,
    QSplitter,
    Qt,
    QResizeEvent
)
from LibGui.loadBrowser import Browser


# 主界面UI
class AutoScriptUI(QStackedWidget):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)

        # 初始化 绘制窗口的时候,会调用渲染函数,需要阻止
        self.init_size_rander = False

        self.browser = Browser()
        self.setWindowTitle("ACode")
        self.setupUi()

        # 窗口默认最大化
        self.showMaximized()

    def setupUi(self):
        self.setObjectName("st_win")
        # self.resize(1235, 844)
        self.setStyleSheet('''
*{
background-color: rgb(33, 33, 33);
color:#fff;
}
#code_win{
border-left:2px solid #455A64;
background-color: #212121;
}

#operation_area{
border-top:2px solid #009688;
background-color:transparent;
}
#url_submit{
border:1px solid #009688;
font: 10pt "等线";
color: rgb(255, 255, 255);
}
#render_btn{
background-color: rgb(62, 62, 62);
border:1px solid rgb(3, 158, 255);
color:rgb(255, 255, 255);
border-radius:4px;
font: 10pt "等线";
}
#write_code_btn{
border:1px solid rgb(0, 232, 0);
color: rgb(255, 255, 255);
font: 10pt "等线";
border-radius:4px;
}
#render_btn:hover,#url_submit:hover,#write_code_btn:hover{
border-width:2px;
}
/*#box{
border:1px solid rgb(0, 170, 255);
}
#box #QCheckBox{
font: 9pt "等线";
}*/
#area{
border:none;
}
        ''')
        self.page = QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout = QHBoxLayout(self.page)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QWidget(self.page)
        self.widget.setObjectName("widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        # # 渲染视图
        self.area_draw = QStackedWidget(self.widget)
        self.area_draw.setObjectName("area_draw")
        self.render = RendererWin()
        self.area_draw.addWidget(self.render)
        self.area_draw.addWidget(self.browser)
        self.verticalLayout.addWidget(self.area_draw)
        # -========================-

        self.operation_area = QStackedWidget(self.widget)
        self.operation_area.setMinimumSize(QSize(0, 211))
        self.operation_area.setMaximumSize(QSize(16777215, 211))
        self.operation_area.setObjectName("operation_area")
        self.page_op = QWidget()
        self.page_op.setObjectName("page_op")
        self.operation_area.addWidget(self.page_op)
        self.page_5 = QWidget()
        self.page_5.setObjectName("page_5")
        self.operation_area.addWidget(self.page_5)
        self.verticalLayout.addWidget(self.operation_area)
        self.horizontalLayout.addWidget(self.widget)

        self.code_win = QTextBrowser(self.page)
        self.code_win.setMinimumSize(QSize(501, 0))
        self.code_win.setMaximumSize(QSize(501, 16777215))
        self.code_win.setObjectName("code_win")
        self.horizontalLayout.addWidget(self.code_win)
        self.addWidget(self.page)

        self.area_draw.setCurrentIndex(0)
        self.setCurrentIndex(0)

        # ---
        self.operation()

    # 代码区域
    def code_area(self):
        pass

    # 绘图区域
    def draw(self):
        pass

    # 操作区域
    def operation(self):
        self.page_op.setStyleSheet('''
#op_right{
border-left:1px solid gray;
background-color:blue;
}
        ''')
        # 创建水平布局
        self.op_hlay = QSplitter(self.page_op)
        self.op_hlay.setOrientation(Qt.Horizontal)
        self.op_hlay.resize(self.page_op.size())
        # self.op_hlay.setOpaqueResize(True)
        # self.op_hlay = QHBoxLayout(self.page_op)
        # self.op_hlay.setContentsMargins(0,0,0,0)
        # self.op_hlay.setSpacing(0)
        self.op_left = QWidget()
        self.op_right= QWidget()
        # self.op_right.setMinimumWidth(400)
        self.op_left.setObjectName("op_left")
        self.op_right.setObjectName("op_right")
        self.op_hlay.addWidget(self.op_left)
        self.op_hlay.addWidget(self.op_right)

        # 在左边 创建上下布局
        self.opleft_vlay = QVBoxLayout(self.op_left)
        self.opleft_vlay.setContentsMargins(0,0,0,0)
        self.opleft_vlay.setSpacing(0)
        self.opl_up = QWidget()
        self.opl_up.setObjectName("opl_up")
        self.opl_up.setFixedHeight(50)
        self.opleft_vlay.addWidget(self.opl_up)

        # url
        self.url_line = QLineEdit(self.opl_up)
        self.url_line.setText("https://www.baidu.com/")
        self.url_line.setObjectName("url_line")
        self.url_line.setPlaceholderText("输入Url")
        self.url_line.setGeometry(2,10,250,30)
        self.url_submit = QPushButton("访问",self.opl_up)
        self.url_submit.setObjectName("url_submit")
        self.url_submit.setGeometry(265,10,80,30)

        # 重新渲染按钮
        self.render_btn = QPushButton("重新渲染",self.opl_up)
        self.render_btn.setObjectName("render_btn")
        self.render_btn.setGeometry(375,10,90,30)

        # 生成自动化代码
        self.write_code_btn =QPushButton("生成代码",self.opl_up)
        self.write_code_btn.setObjectName("write_code_btn")
        self.write_code_btn.setGeometry(490,10,90,30)

        # 眼睛
        self.eye_btn = Eye("眼睛",self.opl_up)
        self.eye_btn.setObjectName("eye_btn")
        self.eye_btn.setGeometry(600,10,50,30)

        # 标签操作区域
        self.box = SorollWidget()
        self.box.setTitle("标签区")
        self.box.setObjectName("box")
        self.opleft_vlay.addWidget(self.box)

    def resizeEvent(self, e:QResizeEvent) -> None:
        self.op_hlay.resize(e.size())  # 自动调节自动布局大小
        super(AutoScriptUI, self).resizeEvent(e)

if __name__ == '__main__':

    app = QApplication(sys.argv)

    win = AutoScriptUI()
    win.show()

    sys.exit(app.exec_())
