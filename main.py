import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, QTime, QDate
import time


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("guiadsb.ui", self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.showtime)
        self.timer.start(1000)

        self.showtime()
        self.showdate()

    def showtime(self):
        currentTime = QTime.currentTime()
        stringTime = currentTime.toString('hh:mm:ss')
        self.timeLabel.setText(stringTime)

    def showdate(self):
        currentDate = QDate.currentDate()
        stringDate = currentDate.toString('dddd, dd MMMM yyyy')
        self.dateLabel.setText(stringDate)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
