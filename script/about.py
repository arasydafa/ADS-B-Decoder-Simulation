import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.uic.properties import QtCore


class AboutWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(AboutWindow, self).__init__(*args, **kwargs)
        uic.loadUi("../ui/about.ui", self)
        self.componentui()
        self.initui()

    def componentui(self):
        # Window Styling
        self.setWindowIcon(QtGui.QIcon("../assets/sideas.png"))

        # Back Button Styling
        self.buttonBack.setStyleSheet("color : #003566;"
                                      "background:transparent;"
                                      "color: #003566;"
                                      "border : 0;")
        self.buttonBack.setIcon(QIcon("../assets/back-arrow.png"))
        self.buttonBack.setIconSize(QtCore.QSize(40, 40))


    def initui(self):
        self.buttonBack.clicked.connect(self.menuwindow)

    def menuwindow(self):
        from menu import MenuWindow

        self.menuOpen = MenuWindow(self)
        self.close()
        self.menuOpen.showMaximized()

    @staticmethod
    def raise_error():
        assert False


def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook
    window = AboutWindow()
    window.showMaximized()
    app.exec_()
