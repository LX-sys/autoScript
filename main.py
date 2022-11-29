
import sys
from PyQt5.QtWidgets import QApplication
from core.autoScript import AutoScript

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = AutoScript()
    win.show()

    sys.exit(app.exec_())