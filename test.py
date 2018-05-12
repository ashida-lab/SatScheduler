# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\test.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1452, 712)
        Dialog.setStyleSheet("QPushButton#evilButton {\n"
"    border-radius: 10px;\n"
"}")
        self.mapView = PlotWidget(Dialog)
        self.mapView.setGeometry(QtCore.QRect(720, 10, 720, 360))
        self.mapView.setObjectName("mapView")
        self.calendarWidget = QtWidgets.QCalendarWidget(Dialog)
        self.calendarWidget.setGeometry(QtCore.QRect(10, 10, 411, 261))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setObjectName("calendarWidget")
        self.timeSlider = QtWidgets.QSlider(Dialog)
        self.timeSlider.setGeometry(QtCore.QRect(10, 280, 411, 22))
        self.timeSlider.setMaximum(86399)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setObjectName("timeSlider")
        self.hourSpinBox = QtWidgets.QSpinBox(Dialog)
        self.hourSpinBox.setGeometry(QtCore.QRect(90, 320, 42, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.hourSpinBox.setFont(font)
        self.hourSpinBox.setMinimum(-1)
        self.hourSpinBox.setMaximum(24)
        self.hourSpinBox.setObjectName("hourSpinBox")
        self.minuteSpinBox = QtWidgets.QSpinBox(Dialog)
        self.minuteSpinBox.setGeometry(QtCore.QRect(200, 320, 42, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.minuteSpinBox.setFont(font)
        self.minuteSpinBox.setMinimum(-1)
        self.minuteSpinBox.setMaximum(60)
        self.minuteSpinBox.setObjectName("minuteSpinBox")
        self.secondSpinBox = QtWidgets.QSpinBox(Dialog)
        self.secondSpinBox.setGeometry(QtCore.QRect(310, 320, 42, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.secondSpinBox.setFont(font)
        self.secondSpinBox.setMinimum(-1)
        self.secondSpinBox.setMaximum(60)
        self.secondSpinBox.setObjectName("secondSpinBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(180, 320, 16, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(290, 320, 16, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(400, 320, 16, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.taskView = GraphicsLayoutWidget(Dialog)
        self.taskView.setGeometry(QtCore.QRect(10, 390, 1431, 311))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.taskView.setFont(font)
        self.taskView.setObjectName("taskView")
        self.addButton = QtWidgets.QPushButton(Dialog)
        self.addButton.setGeometry(QtCore.QRect(450, 90, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")
        self.removeButton = QtWidgets.QPushButton(Dialog)
        self.removeButton.setGeometry(QtCore.QRect(570, 90, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.removeButton.setFont(font)
        self.removeButton.setObjectName("removeButton")
        self.latSpinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.latSpinBox.setGeometry(QtCore.QRect(470, 20, 81, 22))
        self.latSpinBox.setMinimum(-90.0)
        self.latSpinBox.setMaximum(90.0)
        self.latSpinBox.setSingleStep(0.5)
        self.latSpinBox.setObjectName("latSpinBox")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(440, 22, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(440, 50, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lonSpinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.lonSpinBox.setGeometry(QtCore.QRect(470, 50, 81, 22))
        self.lonSpinBox.setMinimum(-180.0)
        self.lonSpinBox.setMaximum(180.0)
        self.lonSpinBox.setSingleStep(0.5)
        self.lonSpinBox.setObjectName("lonSpinBox")
        self.sat1cb = QtWidgets.QCheckBox(Dialog)
        self.sat1cb.setGeometry(QtCore.QRect(450, 180, 75, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sat1cb.setFont(font)
        self.sat1cb.setObjectName("sat1cb")
        self.sat3cb = QtWidgets.QCheckBox(Dialog)
        self.sat3cb.setGeometry(QtCore.QRect(450, 210, 75, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sat3cb.setFont(font)
        self.sat3cb.setObjectName("sat3cb")
        self.sat2cb = QtWidgets.QCheckBox(Dialog)
        self.sat2cb.setGeometry(QtCore.QRect(530, 180, 75, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sat2cb.setFont(font)
        self.sat2cb.setObjectName("sat2cb")
        self.sat4cb = QtWidgets.QCheckBox(Dialog)
        self.sat4cb.setGeometry(QtCore.QRect(530, 210, 75, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sat4cb.setFont(font)
        self.sat4cb.setObjectName("sat4cb")
        self.mapView.raise_()
        self.calendarWidget.raise_()
        self.timeSlider.raise_()
        self.hourSpinBox.raise_()
        self.minuteSpinBox.raise_()
        self.secondSpinBox.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.taskView.raise_()
        self.addButton.raise_()
        self.removeButton.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.lonSpinBox.raise_()
        self.sat1cb.raise_()
        self.sat3cb.raise_()
        self.sat2cb.raise_()
        self.sat4cb.raise_()
        self.latSpinBox.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "h"))
        self.label_2.setText(_translate("Dialog", "m"))
        self.label_3.setText(_translate("Dialog", "s"))
        self.addButton.setText(_translate("Dialog", "Add"))
        self.removeButton.setText(_translate("Dialog", "Remove"))
        self.label_4.setText(_translate("Dialog", "Lat"))
        self.label_5.setText(_translate("Dialog", "Lon"))
        self.sat1cb.setText(_translate("Dialog", "Sat1"))
        self.sat3cb.setText(_translate("Dialog", "Sat3"))
        self.sat2cb.setText(_translate("Dialog", "Sat2"))
        self.sat4cb.setText(_translate("Dialog", "Sat4"))

from pyqtgraph import GraphicsLayoutWidget, PlotWidget
