import sys
from core.Render.RendererWin import RendererWin
from LibGui.sorollWin import SorollWidget
from commonHead import (
    QApplication,
    QStackedWidget,
    QPushButton,
    QLineEdit,
    QTextBrowser,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSize
)

class AutoScriptUI(QStackedWidget):
    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)

        self.setWindowTitle("ACode")
        self.setupUi()

    def setupUi(self):
        self.setObjectName("st_win")
        self.resize(1235, 844)
        self.setStyleSheet('''
*{
background-color: rgb(33, 33, 33);
color:#fff;
}
#code_win{
border-left:2px solid #455A64;
background-color: #212121;
}
#render{
background-color:transparent;
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
        self.area_draw = QStackedWidget(self.widget)
        self.area_draw.setObjectName("area_draw")

        self.render = RendererWin()
        self.render.setObjectName("render")
        self.area_draw.addWidget(self.render)
        self.page_3 = QWidget()
        self.page_3.setObjectName("page_3")
        self.area_draw.addWidget(self.page_3)
        self.verticalLayout.addWidget(self.area_draw)
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

    # 操作区域
    def operation(self):
        # url
        self.url_line = QLineEdit(self.page_op)
        self.url_line.setText("https://www.baidu.com/")
        self.url_line.setObjectName("url_line")
        self.url_line.setPlaceholderText("输入Url")
        self.url_line.setGeometry(10,10,250,30)
        self.url_submit = QPushButton("访问",self.page_op)
        self.url_submit.setObjectName("url_submit")
        self.url_submit.setGeometry(265,10,80,30)

        # 重新渲染按钮
        self.render_btn = QPushButton("重新渲染",self.page_op)
        self.render_btn.setObjectName("render_btn")
        self.render_btn.setGeometry(375,10,90,30)

        # 生成自动化代码
        self.write_code_btn =QPushButton("生成代码",self.page_op)
        self.write_code_btn.setObjectName("write_code_btn")
        self.write_code_btn.setGeometry(490,10,90,30)

        # 标签操作区域
        self.box = SorollWidget(self.page_op)
        self.box.setTitle("标签区")
        self.box.setFixedSize(600,150)
        self.box.setObjectName("box")
        self.box.move(10,45)

from PyQt5.QtCore import QCoreApplication
if __name__ == '__main__':

    app = QApplication(sys.argv)

    win = AutoScriptUI()
    win.show()

    sys.exit(app.exec_())
