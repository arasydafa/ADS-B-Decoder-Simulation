import string
import sys
import pyModeS as pms
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import QTimer, QTime, QDate, pyqtSlot


class DecoderWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(DecoderWindow, self).__init__(*args, **kwargs)
        uic.loadUi("../ui/decoder.ui", self)
        self.timer = QTimer()
        self.componentui()
        self.initui()

    def componentui(self):
        # Window Styling
        self.setWindowIcon(QtGui.QIcon("../assets/sideas.png"))

        # Button Decode Styling
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setOffset(3)
        self.buttonDecode.setGraphicsEffect(shadow)
        self.buttonDecode.setStyleSheet("background-color : #003566;"
                                        "color : #ffffff;"
                                        "border : 5px black;")

        # Text Box Decode Styling
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setOffset(3)
        self.textBoxDecode.setGraphicsEffect(shadow)

        # Status Bar Styling
        self.statusBar().showMessage("Copyright © 2021. All right reserved.")
        self.statusBar().setStyleSheet("background-color : #F5CC00;"
                                       "font-family : Roboto;"
                                       "font-size : 20px;"
                                       "font-style : bold;")

        # Back Button Styling
        self.buttonBack.setStyleSheet("color : #003566;"
                                      "background:transparent;"
                                      "color: #003566;"
                                      "border : 0;")
        self.buttonBack.setIcon(QIcon("../assets/back-arrow.png"))
        self.buttonBack.setIconSize(QtCore.QSize(40, 40))

    def initui(self):
        self.timer.timeout.connect(self.showtime)
        self.timer.start(1000)

        self.showtime()
        self.showdate()

        self.buttonDecode.clicked.connect(self.decode_onclick)
        self.textBoxDecode.returnPressed.connect(self.decode_onclick)
        self.buttonBack.clicked.connect(self.menuwindow)

        self.radioTc1_4.clicked.connect(self.radiostate)
        self.radioTc5_8.toggled.connect(self.radiostate)
        self.radioTc9_18.toggled.connect(self.radiostate)
        self.radioTc19.toggled.connect(self.radiostate)
        self.radioTc20_22.toggled.connect(self.radiostate)
        self.radioTc23_27.toggled.connect(self.radiostate)
        self.radioTc28.toggled.connect(self.radiostate)
        self.radioTc29.toggled.connect(self.radiostate)
        self.radioTc31.toggled.connect(self.radiostate)

    def showtime(self):
        currentTime = QTime.currentTime()
        stringTime = currentTime.toString('hh:mm:ss')
        self.labelTime.setText(stringTime)

    def showdate(self):
        currentDate = QDate.currentDate()
        stringDate = currentDate.toString('dddd, dd MMMM yyyy')
        self.labelDate.setText(stringDate)

    def menuwindow(self):
        from menu import MenuWindow

        self.menuOpen = MenuWindow(self)
        self.close()
        self.menuOpen.showMaximized()

    @pyqtSlot()
    def radiostate(self):
        if self.radioTc1_4.isChecked():
            self.textBoxDecode.setText("8D76CE88204C9072CB48209A504D")
            # self.radioTc5_8.toggled.connect(self.decode_onclick)

        elif self.radioTc5_8.isChecked():
            self.textBoxDecode.setText("8C7C1474381DA443C6450A369656")

        elif self.radioTc9_18.isChecked():
            self.textBoxDecode.setText("8D89611348DB01C6EA41C4C7B8BF")

        elif self.radioTc19.isChecked():
            self.textBoxDecode.setText("8D7C7181991060866808026F519B")

        elif self.radioTc20_22.isChecked():
            self.textBoxDecode.setText("8D7C7181991060866808026F519B")  # Belum pasti

        elif self.radioTc23_27.isChecked():
            self.textBoxDecode.setText("8D7C431FBF59D00000000069B618")

        elif self.radioTc28.isChecked():
            self.textBoxDecode.setText("8D7C7181E1050B00000000C13340")

        elif self.radioTc29.isChecked():
            self.textBoxDecode.setText("8DA8BBE7EA0BD870013F082BC5C5")

        elif self.radioTc31.isChecked():
            self.textBoxDecode.setText("8D7C7181F80000060049A8F9E70F")

    def decode_onclick(self):
        textBoxDecodeValue = self.textBoxDecode.text()
        # QMessageBox.question(self, 'Decoder', f"Pesan : {textBoxDecodeValue}", QMessageBox.Ok, QMessageBox.Ok)

        # Common
        message = textBoxDecodeValue
        dataFrame = pms.df(message)
        lengthBit = len(pms.hex2bin(message))
        typeCode = pms.adsb.typecode(message)
        icao = pms.icao(message)

        # Conditional
        cekHex = all(c in string.hexdigits for c in message)

        # if lengthBit != 12 or cekHex == False:
        #     QMessageBox.about(self, "Title", "Message", QMessageBox.Ok)

        # Binary
        adsbBinary = pms.hex2bin(message)
        dataFrameBinary = pms.hex2bin(message)[:5]
        transponderBinary = pms.hex2bin(message)[5:8]
        icaoBinary = pms.hex2bin(message)[8:32]
        messageBinary = pms.hex2bin(message)[37:88]
        parityBinary = pms.hex2bin(message)[89:112]

        self.textBoxDecode.setText(message)

        # Type Code 1-4
        if 1 <= typeCode <= 4:
            callSign = pms.adsb.callsign(message)

            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Aircraft Identification and Category\n"
                                     f"ICAO\t\t\t : {icao}\n"
                                     f"Call Sign \t\t : {callSign} \n"
                                     f"Vertical Status \t\t : Airborne\n\n"
                                     f"\t\t\t\t| DF       | CA   | ICAO                                             | ME                                                                                                           | PI                                                |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {dataFrameBinary} | {transponderBinary} | {icaoBinary} | {messageBinary} | {parityBinary} |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {len(dataFrameBinary)}         | {len(transponderBinary)}     | {len(icaoBinary)}                                                  | {len(messageBinary)}                                                                                                             | {len(parityBinary)}                                                |\n"
                                     f"")

        # Type Code 5-8
        if 5 <= typeCode <= 8:
            cprFormat = pms.adsb.oe_flag(message)
            cprLat = pms.bin2int(adsbBinary[54:71])
            cprLon = pms.bin2int(adsbBinary[71:88])
            velocity = pms.adsb.surface_velocity(message)

            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Surface position\n"
                                     f"ICAO\t\t\t : {icao}\n"
                                     f"CPR Format\t\t : {'Odd' if cprFormat else 'Even'}\n"
                                     f"CPR Latitude\t\t : {cprLat} - {cprLat / 131072.0}\n"
                                     f"CPR Longitude\t\t : {cprLon} - {cprLon / 131072.0}\n"
                                     f"Speed\t\t\t : {velocity[0]} knots\n"
                                     f"Track\t\t\t : {velocity[1]} degrees\n"
                                     f"Vertical Status \t\t : Airborne\n\n"
                                     f"\t\t\t\t| DF       | CA   | ICAO                                             | ME                                                                                                           | PI                                                |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {dataFrameBinary} | {transponderBinary} | {icaoBinary} | {messageBinary} | {parityBinary} |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {len(dataFrameBinary)}         | {len(transponderBinary)}     | {len(icaoBinary)}                                                  | {len(messageBinary)}                                                                                                             | {len(parityBinary)}                                                |\n"
                                     f"")

        if 9 <= typeCode <= 18:
            cprFormat = pms.adsb.oe_flag(message)
            cprLat = pms.bin2int(adsbBinary[54:71])
            cprLon = pms.bin2int(adsbBinary[71:88])
            altitude = pms.adsb.altitude(message)

            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Airborne position (with barometric altitude)\n"
                                     f"ICAO\t\t\t : {icao}\n"
                                     f"CPR Format\t\t : {'Odd' if cprFormat else 'Even'}\n"
                                     f"CPR Latitude\t\t : {cprLat} - {cprLat / 131072.0}\n"
                                     f"CPR Longitude\t\t : {cprLon} - {cprLon / 131072.0}\n"
                                     f"Altitude\t\t\t : {altitude} feet\n"
                                     f"Vertical Status \t\t : Airborne\n\n"
                                     f"\t\t\t\t| DF       | CA   | ICAO                                             | ME                                                                                                           | PI                                                |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {dataFrameBinary} | {transponderBinary} | {icaoBinary} | {messageBinary} | {parityBinary} |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {len(dataFrameBinary)}         | {len(transponderBinary)}     | {len(icaoBinary)}                                                  | {len(messageBinary)}                                                                                                             | {len(parityBinary)}                                                |\n"
                                     f"")

        if typeCode == 19:
            speed, track, verticalRate, t = pms.adsb.velocity(message)
            types = {"GS": "Ground speed", "TAS": "True airspeed"}

            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Airborne velocity\n"
                                     f"ICAO\t\t\t : {icao}\n"
                                     f"Speed\t\t\t : {speed} knots\n"
                                     f"Track\t\t\t : {track} degrees\n"
                                     f"Vertical Rate\t\t : {verticalRate} feet/minute\n"
                                     f"Type\t\t\t : {types[t]}\n\n"
                                     f"\t\t\t\t| DF       | CA   | ICAO                                             | ME                                                                                                           | PI                                                |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {dataFrameBinary} | {transponderBinary} | {icaoBinary} | {messageBinary} | {parityBinary} |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {len(dataFrameBinary)}         | {len(transponderBinary)}     | {len(icaoBinary)}                                                  | {len(messageBinary)}                                                                                                             | {len(parityBinary)}                                                |\n"
                                     f"")

        if 20 <= typeCode <= 22:
            cprFormat = pms.adsb.oe_flag(message)
            cprLat = pms.bin2int(adsbBinary[54:71])
            cprLon = pms.bin2int(adsbBinary[71:88])
            altitude = pms.adsb.altitude(message)

            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Airborne position (with GNSS altitude)\n"
                                     f"ICAO\t\t\t : {icao}\n"
                                     f"CPR Format\t\t : {'Odd' if cprFormat else 'Even'}\n"
                                     f"CPR Latitude\t\t : {cprLat} - {cprLat / 131072.0}\n"
                                     f"CPR Longitude\t\t : {cprLon} - {cprLon / 131072.0}\n"
                                     f"Altitude\t\t\t : {altitude} feet\n"
                                     f"Vertical Status \t\t : Airborne\n\n"
                                     f"\t\t\t\t| DF       | CA   | ICAO                                             | ME                                                                                                           | PI                                                |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {dataFrameBinary} | {transponderBinary} | {icaoBinary} | {messageBinary} | {parityBinary} |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {len(dataFrameBinary)}         | {len(transponderBinary)}     | {len(icaoBinary)}                                                  | {len(messageBinary)}                                                                                                             | {len(parityBinary)}                                                |\n"
                                     f"")

        if 23 <= typeCode <= 27:
            subType = pms.bin2int(adsbBinary[37:40])
            squawkId = pms.bin2int(adsbBinary[40:53])

            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Test Message with Squawk (Reserved)\n"
                                     f"ICAO\t\t\t : {icao}\n"
                                     f"Sub Type\t\t\t : {subType}\n"
                                     f"Squawk Identity\t\t : {squawkId}\n\n"
                                     f"\t\t\t\t| DF       | CA   | ICAO                                             | ME                                                                                                           | PI                                                |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {dataFrameBinary} | {transponderBinary} | {icaoBinary} | {messageBinary} | {parityBinary} |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {len(dataFrameBinary)}         | {len(transponderBinary)}     | {len(icaoBinary)}                                                  | {len(messageBinary)}                                                                                                             | {len(parityBinary)}                                                |\n"
                                     f"")

        if typeCode == 28:
            subType = pms.bin2int(adsbBinary[37:40])

            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Aircraft Status\n"
                                     f"ICAO\t\t\t : {icao}\n"
                                     f"Sub Type\t\t\t : {subType}\n"
                                     f"Vertical Status \t\t : Airborne\n\n"
                                     f"\t\t\t\t| DF       | CA   | ICAO                                             | ME                                                                                                           | PI                                                |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {dataFrameBinary} | {transponderBinary} | {icaoBinary} | {messageBinary} | {parityBinary} |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {len(dataFrameBinary)}         | {len(transponderBinary)}     | {len(icaoBinary)}                                                  | {len(messageBinary)}                                                                                                             | {len(parityBinary)}                                                |\n"
                                     f"")

        if typeCode == 29:
            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Aircraft Status\n"
                                     f"ICAO\t\t\t : {icao}\n"
                                     f"Vertical Status \t\t : Airborne\n\n"
                                     f"\t\t\t\t| DF       | CA   | ICAO                                             | ME                                                                                                           | PI                                                |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {dataFrameBinary} | {transponderBinary} | {icaoBinary} | {messageBinary} | {parityBinary} |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {len(dataFrameBinary)}         | {len(transponderBinary)}     | {len(icaoBinary)}                                                  | {len(messageBinary)}                                                                                                             | {len(parityBinary)}                                                |\n"
                                     f"")

            if typeCode == 31:
                subType = pms.bin2int(adsbBinary[37:40])
                compassHeading = ""

                if subType == 0:
                    compassHeading = "True North"
                if subType == 1:
                    compassHeading = "Magnetic North"

            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Aircraft Operation Status\n"
                                     f"Sub Type\t\t\t : {subType}\n"
                                     f"Compass Heading\t : {compassHeading}\n\n"  # Data masih belum akurat
                                     f"\t\t\t\t| DF       | CA   | ICAO                                             | ME                                                                                                           | PI                                                |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {dataFrameBinary} | {transponderBinary} | {icaoBinary} | {messageBinary} | {parityBinary} |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {len(dataFrameBinary)}         | {len(transponderBinary)}     | {len(icaoBinary)}                                                  | {len(messageBinary)}                                                                                                             | {len(parityBinary)}                                                |\n"
                                     f"")

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
    window = DecoderWindow()
    window.showMaximized()
    app.exec_()
