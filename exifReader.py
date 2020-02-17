import sys
import glob
import webbrowser

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableView, QLabel
from PyQt5.QtGui import QPixmap, QTransform

from MainWindow import Ui_MainWindow
from utils import getExif, convertToDegree


class ExifTableModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, todos=None, **kwargs):
        super(ExifTableModel, self).__init__(*args, **kwargs)
        self.exifData = None

    def update(self, data):
        self.exifData = data

    def rowCount(self, parent=QtCore.QModelIndex()):
        if self.exifData is not None:
            return len(list(self.exifData.values()))
        else:
            return 0

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 2

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            i = index.row()
            j = index.column()
            if j == 0:
                return list(self.exifData)[i]
            else:
                return str(self.exifData[(list(self.exifData)[i])])
        else:
            return QtCore.QVariant()

    def headerData(self, rowcol, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if rowcol == 0:
                return 'Exif Info'
            else:
                return 'Data'

    def getPosition(self):
        try:
            return str(convertToDegree(self.exifData['GPSInfo'][2])) + ',' +\
                   str(convertToDegree(self.exifData['GPSInfo'][4]))
        except:
            return None


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.firstTime = True;

        self.leftRotateButton.clicked.connect(self.leftRotate)
        self.rightRotateButton.clicked.connect(self.rightRotate)
        self.mapButton.clicked.connect(self.openMapPosition)

        self.previousButton.clicked.connect(self.previuos)
        self.nextButton.clicked.connect(self.next)

        self.imagesPaths = glob.glob('*.JPG') + glob.glob('*.jpg') + glob.glob('*.jpeg')
        self.actualImagePath = self.imagesPaths[0]

        self.pixmap = QPixmap(self.actualImagePath)
        self.label.setPixmap(self.pixmap.scaled(512, 512, QtCore.Qt.KeepAspectRatio))

        self.tableModel = ExifTableModel(self)
        self.tableModel.update(getExif(self.actualImagePath))

        self.tableView.setModel(self.tableModel)

    def resizeEvent(self, event):
        if self.firstTime:
            self.label.setPixmap(self.pixmap.scaled(512, 512, QtCore.Qt.KeepAspectRatio))
            self.firstTime = False
        else:
            self.label.setPixmap(self.pixmap.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio))

    def imageUpdate(self, imagePath):
        self.pixmap = QPixmap(imagePath)
        self.label.setPixmap(self.pixmap.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio))

    def previuos(self):
        self.actualImagePath = self.imagesPaths[(self.imagesPaths.index(self.actualImagePath) - 1)
                                                % len(self.imagesPaths)]
        self.imageUpdate(self.actualImagePath)
        self.tableModel.update(getExif(self.actualImagePath))
        self.tableModel.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def next(self):
        self.actualImagePath = self.imagesPaths[(self.imagesPaths.index(self.actualImagePath) + 1)
                                                % len(self.imagesPaths)]
        self.imageUpdate(self.actualImagePath)
        self.tableModel.update(getExif(self.actualImagePath))
        self.tableModel.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def leftRotate(self):
        self.pixmap = self.pixmap.transformed(QTransform().rotate(-90))
        scaled = self.pixmap.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaled)

    def rightRotate(self):
        self.pixmap = self.pixmap.transformed(QTransform().rotate(90))
        scaled = self.pixmap.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaled)

    def openMapPosition(self):
        position = self.tableModel.getPosition()
        if (position is not None):
            webbrowser.open_new("https://www.google.com/maps/search/?api=1&query=" + str(position))
        else:
            webbrowser.open_new("https://www.google.com/maps/search/")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()