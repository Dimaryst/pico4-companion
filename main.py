import sys
from PyQt5 import QtWidgets
from ui_module import MainInstaller

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainInstaller()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()