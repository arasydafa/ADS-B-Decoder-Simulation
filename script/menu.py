import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.uic.properties import QtCore


class MenuWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MenuWindow, self).__init__(*args, **kwargs)
        uic.loadUi("../ui/menu.ui", self)
        self.componentui()
        self.initui()

    def componentui(self):
        # Window Styling
        self.setWindowIcon(QtGui.QIcon("../assets/sideas.png"))

        # Button About Styling
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(90)
        shadow.setOffset(5)
        self.buttonAbout.setGraphicsEffect(shadow)

        # Button Simulation Styling
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(90)
        shadow.setOffset(5)
        self.buttonSimulation.setGraphicsEffect(shadow)

        # Back Button Styling
        self.buttonBack.setStyleSheet("color : #003566;"
                                      "background:transparent;"
                                      "color: #003566;"
                                      "border : 0;")
        self.buttonBack.setIcon(QIcon("../assets/back-arrow.png"))
        self.buttonBack.setIconSize(QtCore.QSize(40, 40))

    def initui(self):
        self.buttonAbout.clicked.connect(self.aboutwindow)
        self.buttonSimulation.clicked.connect(self.simulationwindow)
        self.buttonBack.clicked.connect(self.homewindow)

    def aboutwindow(self):
        from about import AboutWindow

        self.aboutOpen = AboutWindow(self)
        self.close()
        self.aboutOpen.showMaximized()

    def simulationwindow(self):
        from decoder import DecoderWindow

        self.decoderOpen = DecoderWindow(self)
        self.close()
        self.decoderOpen.showMaximized()

    def homewindow(self):
        from home import HomeWindow

        self.homeOpen = HomeWindow(self)
        self.close()
        self.homeOpen.showMaximized()

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
    window = MenuWindow()
    window.showMaximized()
    app.exec_()
