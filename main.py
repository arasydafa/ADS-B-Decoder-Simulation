import sys
import traceback
import pyModeS as pms
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import QTimer, QTime, QDate, pyqtSlot


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("guiadsb.ui", self)
        self.timer = QTimer()
        self.componentui()
        self.initui()

    def componentui(self):
        # Window Styling
        self.setWindowIcon(QtGui.QIcon("assets/Satellite Dish.png"))

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
        self.statusBar().showMessage("Copyright © 2021. All right reserved. Politeknik Elektronika Negeri Surabaya. "
                                     "D3 Teknik Telekomunikasi")
        self.statusBar().setStyleSheet("background-color : #F5CC00;"
                                       "font-family : Roboto;"
                                       "font-size : 20px;"
                                       "font-style : bold;")

        # Date and Time Label Styling
        self.labelDate.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.labelTime.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

    def initui(self):
        self.timer.timeout.connect(self.showtime)
        self.timer.start(1000)

        self.showtime()
        self.showdate()

        self.buttonDecode.clicked.connect(self.decode_onclick)
        self.textBoxDecode.returnPressed.connect(self.decode_onclick)

    def showtime(self):
        currentTime = QTime.currentTime()
        stringTime = currentTime.toString('hh:mm:ss')
        self.labelTime.setText(stringTime)

    def showdate(self):
        currentDate = QDate.currentDate()
        stringDate = currentDate.toString('dddd, dd MMMM yyyy')
        self.labelDate.setText(stringDate)

    # def radiostate(self, radio):

    @pyqtSlot()
    def decode_onclick(self):
        # 8D4840D6202CC371C32CE0576098
        textBoxDecodeValue = self.textBoxDecode.text()
        # QMessageBox.question(self, 'Decoder', f"Pesan : {textBoxDecodeValue}", QMessageBox.Ok, QMessageBox.Ok)

        # Common
        message = textBoxDecodeValue
        dataFrame = pms.df(message)
        lengthBit = len(pms.hex2bin(textBoxDecodeValue))
        typeCode = pms.typecode(message)

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
            cprLat = pms.bin2int(adsbBinary[54:71]) / 131072.0
            cprLon = pms.bin2int(adsbBinary[71:88]) / 131072.0
            velocity = pms.adsb.surface_velocity(message)

            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Surface position\n"
                                     f"CPR Format\t\t : {'Odd' if cprFormat else 'Even'}\n"
                                     f"CPR Latitude\t\t : {cprLat}\n"
                                     f"CPR Longitude\t\t : {cprLon}\n"
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
            cprLat = pms.bin2int(adsbBinary[54:71]) / 131072.0
            cprLon = pms.bin2int(adsbBinary[71:88]) / 131072.0
            altitude = pms.adsb.altitude(message)

            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Airborne position (with barometric altitude)\n"
                                     f"CPR Format\t\t : {'Odd' if cprFormat else 'Even'}\n"
                                     f"CPR Latitude\t\t : {cprLat}\n"
                                     f"CPR Longitude\t\t : {cprLon}\n"
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
            cprLat = pms.bin2int(adsbBinary[54:71]) / 131072.0
            cprLon = pms.bin2int(adsbBinary[71:88]) / 131072.0
            altitude = pms.adsb.altitude(message)

            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Airborne position (with GNSS altitude)\n"
                                     f"CPR Format\t\t : {'Odd' if cprFormat else 'Even'}\n"
                                     f"CPR Latitude\t\t : {cprLat}\n"
                                     f"CPR Longitude\t\t : {cprLon}\n"
                                     f"Altitude\t\t\t : {altitude} feet\n"
                                     f"Vertical Status \t\t : Airborne\n\n"
                                     f"\t\t\t\t| DF       | CA   | ICAO                                             | ME                                                                                                           | PI                                                |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {dataFrameBinary} | {transponderBinary} | {icaoBinary} | {messageBinary} | {parityBinary} |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {len(dataFrameBinary)}         | {len(transponderBinary)}     | {len(icaoBinary)}                                                  | {len(messageBinary)}                                                                                                             | {len(parityBinary)}                                                |\n"
                                     f"")

        if 23 <= typeCode <= 28:
            subType = pms.bin2int(adsbBinary[32:37])
            squawkId = pms.bin2int(adsbBinary[40:52])

            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Test Message with Squawk (Reserved)\n"
                                     f"Sub Type\t\t\t : {subType}\n"
                                     f"Squawk Identity\t\t : {squawkId}\n\n"
                                     f"\t\t\t\t| DF       | CA   | ICAO                                             | ME                                                                                                           | PI                                                |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {dataFrameBinary} | {transponderBinary} | {icaoBinary} | {messageBinary} | {parityBinary} |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {len(dataFrameBinary)}         | {len(transponderBinary)}     | {len(icaoBinary)}                                                  | {len(messageBinary)}                                                                                                             | {len(parityBinary)}                                                |\n"
                                     f"")

        if typeCode == 28:
            self.textBoxAdsb.setText(f"Frame\t\t\t : {message} \n"
                                     f"Length\t\t\t : {lengthBit} bits\n"
                                     f"Downlink Format (DF)\t : ({dataFrame}) ADS-B \n"
                                     f"Type Code (TC)\t\t : {typeCode} - Aircraft Status\n\n"
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
                                     f"Vertical Status \t\t : On The Ground\n"
                                     f"Sub Type\t\t\t : {subType}\n"
                                     f"Compass Heading\t : {compassHeading}\n\n"
                                     f"\t\t\t\t| DF       | CA   | ICAO                                             | ME                                                                                                           | PI                                                |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {dataFrameBinary} | {transponderBinary} | {icaoBinary} | {messageBinary} | {parityBinary} |\n"
                                     f"\t\t\t\t-------------+-------+------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------------------------+\n"
                                     f"\t\t\t\t| {len(dataFrameBinary)}         | {len(transponderBinary)}     | {len(icaoBinary)}                                                  | {len(messageBinary)}                                                                                                             | {len(parityBinary)}                                                |\n"
                                     f"")

    @staticmethod
    def raise_error():
        assert False


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Error Catched! :")
    print("Error Message :\n", tb)
    QtWidgets.QApplication.quit()
    # or QtWidgets.QApplication.exit(0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    sys.excepthook = excepthook
    window = MainWindow()
    window.show()
    app.exec_()
