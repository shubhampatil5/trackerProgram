#!/usr/bin/python
# -*- coding: utf-8 -*-

# Object Tracker program version 1.2 : a tool to track an object of a specified color with a camera.
# Copyright (C) 2017  Vanessa Dan, Eve Machefert and Alix Plamont
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# To contact us: <alix.plamont@etu.upmc.fr>.

# This is the main GUI of this tool.
# This file has been generated by pyuic4 command, from a ui file we have made with QtDesigner.
# The generated code has been few modified -- a QGraphicsScene was added for example.

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class UiSetting(object):
    def setupUi(self, Setting):
        Setting.setObjectName(_fromUtf8("Setting"))
        Setting.resize(650, 760)
        Setting.setMinimumSize(QtCore.QSize(650, 760))
        Setting.setMaximumSize(QtCore.QSize(650, 760))
        self.centralwidget = QtGui.QWidget(Setting)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.applyBtn = QtGui.QPushButton(self.centralwidget)
        self.applyBtn.setGeometry(QtCore.QRect(570, 620, 60, 115))
        self.applyBtn.setMinimumSize(QtCore.QSize(60, 115))
        self.applyBtn.setMaximumSize(QtCore.QSize(60, 115))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.applyBtn.setFont(font)
        self.applyBtn.setObjectName(_fromUtf8("applyBtn"))
        self.resetBtn = QtGui.QPushButton(self.centralwidget)
        self.resetBtn.setGeometry(QtCore.QRect(570, 500, 60, 115))
        self.resetBtn.setMinimumSize(QtCore.QSize(60, 115))
        self.resetBtn.setMaximumSize(QtCore.QSize(60, 115))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.resetBtn.setFont(font)
        self.resetBtn.setObjectName(_fromUtf8("resetBtn"))
        self.hMinSlider = QtGui.QSlider(self.centralwidget)
        self.hMinSlider.setGeometry(QtCore.QRect(80, 500, 440, 21))
        self.hMinSlider.setMinimumSize(QtCore.QSize(440, 21))
        self.hMinSlider.setMaximumSize(QtCore.QSize(440, 21))
        self.hMinSlider.setToolTip(_fromUtf8(""))
        self.hMinSlider.setStatusTip(_fromUtf8(""))
        self.hMinSlider.setWhatsThis(_fromUtf8(""))
        self.hMinSlider.setAccessibleName(_fromUtf8(""))
        self.hMinSlider.setAccessibleDescription(_fromUtf8(""))
        self.hMinSlider.setStyleSheet(_fromUtf8(""))
        self.hMinSlider.setMaximum(255)
        self.hMinSlider.setOrientation(QtCore.Qt.Horizontal)
        self.hMinSlider.setObjectName(_fromUtf8("hMinSlider"))
        self.hMaxSlider = QtGui.QSlider(self.centralwidget)
        self.hMaxSlider.setGeometry(QtCore.QRect(80, 530, 440, 21))
        self.hMaxSlider.setMinimumSize(QtCore.QSize(440, 21))
        self.hMaxSlider.setMaximumSize(QtCore.QSize(440, 21))
        self.hMaxSlider.setMaximum(255)
        self.hMaxSlider.setProperty("value", 255)
        self.hMaxSlider.setOrientation(QtCore.Qt.Horizontal)
        self.hMaxSlider.setObjectName(_fromUtf8("hMaxSlider"))
        self.sMinSlider = QtGui.QSlider(self.centralwidget)
        self.sMinSlider.setGeometry(QtCore.QRect(80, 570, 440, 21))
        self.sMinSlider.setMinimumSize(QtCore.QSize(440, 21))
        self.sMinSlider.setMaximumSize(QtCore.QSize(440, 21))
        self.sMinSlider.setMaximum(255)
        self.sMinSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sMinSlider.setObjectName(_fromUtf8("sMinSlider"))
        self.sMaxSlider = QtGui.QSlider(self.centralwidget)
        self.sMaxSlider.setGeometry(QtCore.QRect(80, 600, 440, 21))
        self.sMaxSlider.setMinimumSize(QtCore.QSize(440, 21))
        self.sMaxSlider.setMaximumSize(QtCore.QSize(440, 21))
        self.sMaxSlider.setMaximum(255)
        self.sMaxSlider.setProperty("value", 255)
        self.sMaxSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sMaxSlider.setObjectName(_fromUtf8("sMaxSlider"))
        self.vMinSlider = QtGui.QSlider(self.centralwidget)
        self.vMinSlider.setGeometry(QtCore.QRect(80, 640, 440, 21))
        self.vMinSlider.setMinimumSize(QtCore.QSize(440, 21))
        self.vMinSlider.setMaximumSize(QtCore.QSize(440, 21))
        self.vMinSlider.setMaximum(255)
        self.vMinSlider.setOrientation(QtCore.Qt.Horizontal)
        self.vMinSlider.setObjectName(_fromUtf8("vMinSlider"))
        self.vMaxSlider = QtGui.QSlider(self.centralwidget)
        self.vMaxSlider.setGeometry(QtCore.QRect(80, 670, 440, 21))
        self.vMaxSlider.setMinimumSize(QtCore.QSize(440, 21))
        self.vMaxSlider.setMaximumSize(QtCore.QSize(440, 21))
        self.vMaxSlider.setMaximum(255)
        self.vMaxSlider.setProperty("value", 255)
        self.vMaxSlider.setOrientation(QtCore.Qt.Horizontal)
        self.vMaxSlider.setTickPosition(QtGui.QSlider.NoTicks)
        self.vMaxSlider.setObjectName(_fromUtf8("vMaxSlider"))
        self.graphicsScene = QtGui.QGraphicsScene(self.centralwidget)
        self.graphicsView = QtGui.QGraphicsView(self.graphicsScene,self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(5, 5, 640, 480))
        self.graphicsView.setMinimumSize(QtCore.QSize(640, 480))
        self.graphicsView.setMaximumSize(QtCore.QSize(640, 480))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.precisionSlider = QtGui.QSlider(self.centralwidget)
        self.precisionSlider.setGeometry(QtCore.QRect(80, 710, 440, 21))
        self.precisionSlider.setMinimumSize(QtCore.QSize(440, 21))
        self.precisionSlider.setMaximumSize(QtCore.QSize(440, 21))
        self.precisionSlider.setMinimum(10)
        self.precisionSlider.setMaximum(90)
        self.precisionSlider.setProperty("value", 40)
        self.precisionSlider.setOrientation(QtCore.Qt.Horizontal)
        self.precisionSlider.setObjectName(_fromUtf8("precisionSlider"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(530, 500, 30, 15))
        self.label.setMinimumSize(QtCore.QSize(30, 15))
        self.label.setMaximumSize(QtCore.QSize(30, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.hMinSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.hMinSpinBox.setGeometry(QtCore.QRect(20, 500, 60, 20))
        self.hMinSpinBox.setMinimumSize(QtCore.QSize(60, 20))
        self.hMinSpinBox.setMaximumSize(QtCore.QSize(60, 20))
        self.hMinSpinBox.setMaximum(255)
        self.hMinSpinBox.setObjectName(_fromUtf8("hMinSpinBox"))
        self.hMaxSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.hMaxSpinBox.setGeometry(QtCore.QRect(20, 530, 60, 20))
        self.hMaxSpinBox.setMinimumSize(QtCore.QSize(60, 20))
        self.hMaxSpinBox.setMaximumSize(QtCore.QSize(60, 20))
        self.hMaxSpinBox.setMaximum(255)
        self.hMaxSpinBox.setProperty("value", 255)
        self.hMaxSpinBox.setObjectName(_fromUtf8("hMaxSpinBox"))
        self.sMinSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.sMinSpinBox.setGeometry(QtCore.QRect(20, 570, 60, 20))
        self.sMinSpinBox.setMinimumSize(QtCore.QSize(60, 20))
        self.sMinSpinBox.setMaximumSize(QtCore.QSize(60, 20))
        self.sMinSpinBox.setMaximum(255)
        self.sMinSpinBox.setObjectName(_fromUtf8("sMinSpinBox"))
        self.sMaxSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.sMaxSpinBox.setGeometry(QtCore.QRect(20, 600, 60, 20))
        self.sMaxSpinBox.setMinimumSize(QtCore.QSize(60, 20))
        self.sMaxSpinBox.setMaximumSize(QtCore.QSize(60, 20))
        self.sMaxSpinBox.setMaximum(255)
        self.sMaxSpinBox.setProperty("value", 255)
        self.sMaxSpinBox.setObjectName(_fromUtf8("sMaxSpinBox"))
        self.vMinSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.vMinSpinBox.setGeometry(QtCore.QRect(20, 640, 60, 20))
        self.vMinSpinBox.setMinimumSize(QtCore.QSize(60, 20))
        self.vMinSpinBox.setMaximumSize(QtCore.QSize(60, 20))
        self.vMinSpinBox.setMaximum(255)
        self.vMinSpinBox.setObjectName(_fromUtf8("vMinSpinBox"))
        self.vMaxSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.vMaxSpinBox.setGeometry(QtCore.QRect(20, 670, 60, 20))
        self.vMaxSpinBox.setMinimumSize(QtCore.QSize(60, 20))
        self.vMaxSpinBox.setMaximumSize(QtCore.QSize(60, 20))
        self.vMaxSpinBox.setMaximum(255)
        self.vMaxSpinBox.setProperty("value", 255)
        self.vMaxSpinBox.setObjectName(_fromUtf8("vMaxSpinBox"))
        self.precisionSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.precisionSpinBox.setGeometry(QtCore.QRect(20, 710, 60, 20))
        self.precisionSpinBox.setMinimumSize(QtCore.QSize(60, 20))
        self.precisionSpinBox.setMaximumSize(QtCore.QSize(60, 20))
        self.precisionSpinBox.setMinimum(10)
        self.precisionSpinBox.setMaximum(90)
        self.precisionSpinBox.setProperty("value", 40)
        self.precisionSpinBox.setObjectName(_fromUtf8("precisionSpinBox"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(530, 530, 30, 15))
        self.label_2.setMinimumSize(QtCore.QSize(30, 15))
        self.label_2.setMaximumSize(QtCore.QSize(30, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(530, 570, 30, 15))
        self.label_3.setMinimumSize(QtCore.QSize(30, 15))
        self.label_3.setMaximumSize(QtCore.QSize(30, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(530, 600, 30, 15))
        self.label_4.setMinimumSize(QtCore.QSize(30, 15))
        self.label_4.setMaximumSize(QtCore.QSize(30, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(530, 640, 30, 15))
        self.label_5.setMinimumSize(QtCore.QSize(30, 15))
        self.label_5.setMaximumSize(QtCore.QSize(30, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(530, 670, 30, 15))
        self.label_6.setMinimumSize(QtCore.QSize(30, 15))
        self.label_6.setMaximumSize(QtCore.QSize(30, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(530, 710, 30, 15))
        self.label_7.setMinimumSize(QtCore.QSize(30, 15))
        self.label_7.setMaximumSize(QtCore.QSize(30, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        Setting.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(Setting)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Setting.setStatusBar(self.statusbar)

        self.retranslateUi(Setting)
        QtCore.QObject.connect(self.hMinSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.hMinSpinBox.setValue)
        QtCore.QObject.connect(self.hMinSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.hMinSlider.setValue)
        QtCore.QObject.connect(self.hMaxSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.hMaxSpinBox.setValue)
        QtCore.QObject.connect(self.hMaxSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.hMaxSlider.setValue)
        QtCore.QObject.connect(self.sMinSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sMinSpinBox.setValue)
        QtCore.QObject.connect(self.sMinSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sMinSlider.setValue)
        QtCore.QObject.connect(self.sMaxSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sMaxSpinBox.setValue)
        QtCore.QObject.connect(self.sMaxSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.sMaxSlider.setValue)
        QtCore.QObject.connect(self.vMinSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.vMinSpinBox.setValue)
        QtCore.QObject.connect(self.vMinSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.vMinSlider.setValue)
        QtCore.QObject.connect(self.vMaxSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.vMaxSpinBox.setValue)
        QtCore.QObject.connect(self.vMaxSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.vMaxSlider.setValue)
        QtCore.QObject.connect(self.precisionSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.precisionSpinBox.setValue)
        QtCore.QObject.connect(self.precisionSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.precisionSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(Setting)

    def retranslateUi(self, Setting):
        Setting.setWindowTitle(_translate("Setting", "Setting", None))
        self.applyBtn.setText(_translate("Setting", "Apply", None))
        self.resetBtn.setText(_translate("Setting", "Reset", None))
        self.label.setText(_translate("Setting", "hMin", None))
        self.label_2.setText(_translate("Setting", "hMax", None))
        self.label_3.setText(_translate("Setting", "sMin", None))
        self.label_4.setText(_translate("Setting", "sMax", None))
        self.label_5.setText(_translate("Setting", "vMin", None))
        self.label_6.setText(_translate("Setting", "vMax", None))
        self.label_7.setText(_translate("Setting", "prec", None))


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    Setting = QtGui.QMainWindow()
    ui = UiSetting()
    ui.setupUi(Setting)
    Setting.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    