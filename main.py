from commonHead import sys,QApplication
from core.autoScript import AutoScript

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = AutoScript()
    win.show()

    sys.exit(app.exec_())