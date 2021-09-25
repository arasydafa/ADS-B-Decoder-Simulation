import sys
from PyQt5 import QtWidgets, uic, QtGui


class HomeWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(HomeWindow, self).__init__(*args, **kwargs)
        uic.loadUi("../ui/home.ui", self)
        self.componentui()
        self.initui()

    def componentui(self):
        # Window Styling
        self.setWindowIcon(QtGui.QIcon("../assets/sideas.png"))

        # Button Styling
        self.buttonStart.setStyleSheet("color : #FFE921;"
                                       "background-color: #370202;"
                                       "border-radius: 15px;")

    def initui(self):
        self.buttonStart.clicked.connect(self.decoderwindow)

    def decoderwindow(self):
        from decoder import DecoderWindow

        self.decoderOpen = DecoderWindow(self)
        self.close()
        self.decoderOpen.showMaximized()

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
    window = HomeWindow()
    window.showMaximized()
    app.exec_()
