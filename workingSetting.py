#!/usr/bin/python
# -*- coding: utf-8 -*-

# Object Tracker program : a tool to track an object of a specified color with a camera.
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

# This file is the main python file of this program.
# This program tracks an object of a particular color with a camera,
# displaying a square on tracked object.
# It was designed to be a tool to configure some program which needs to track
# an specified object with a camera.
# Our project is to use it for creating a 'numeric theremin' : theremin's user will put gloves
# of a certain color and use this program to configure his instrument.
# That's why, in future updates, this program will save user's setting in a file which will be used
# by theremin's program.

from functools import reduce
import numpy

from PyQt4 import QtCore, QtGui
import cv2

from TrackingGUI import UiSetting



class DisplayThread(QtCore.QThread):
	"""This class is a QThread designed to relieve the main thread for frame rendering computations.

	It provides the current filtered frame in the form of a QImage to the main thread
	and also computes the barycentre's coordinates.
	OpenCV module is used for video capture and frame rendering.
	"""
	def __init__(self):
		"""Displaying class' constructor.

		It subclass QThread and defines :
		- bounds used to filter video colors ;
		- an attribute to set the precision of barycentre computation ;
		- the cam object ;
		- attributes for frame resolution.
		"""
		super(DisplayThread, self).__init__()

		#hsv format is used to filter colors
		self.hMinT = 0
		self.hMaxT = 255
		self.sMinT = 0
		self.sMaxT = 255
		self.vMinT = 0
		self.vMaxT = 255

		self.precisionT = 40

		self.cam = cv2.VideoCapture(0)
		_, frame = self.cam.read() #frame sample to take resolution
		self.w, self.h = frame.shape[1], frame.shape[0]


	def __del__(self):
		"""This func makes part of QThread's structure.
		"""
		self.wait()


	def getValues(self, hmin, hmax, smin, smax, vmin, vmax, prec):
		"""Func used to synchronize bounds and precision with values of GUI's sliders.
		"""
		self.hMinT = hmin
		self.hMaxT = hmax
		self.sMinT = smin
		self.sMaxT = smax
		self.vMinT = vmin
		self.vMaxT = vmax
		self.precisionT = prec


	def barycentre(self, image):
		"""Returns the barycentre of non-null pixels.

		The third value returned is a bool that indicates if there are non-null pixels.
		Because colors filtering will only keeps non-null pixels from the aimed object,
		compute their barycentre is a good way to track an object of a particular color.
		To make the computing faster, the image given in arg is resized smaller.
		"""
		L0 = image[:, :, 0].nonzero() #lists of coordinates of pixels
		L1 = image[:, :, 1].nonzero() #which have a non-zero R (then G, then B) value
		L2 = image[:, :, 2].nonzero() 
		LY = reduce(numpy.intersect1d, (L0[0], L1[0], L2[0])) #lists of ordinates and abscissa
		LX = reduce(numpy.intersect1d, (L0[1], L1[1], L2[1])) #of non-zeros pixels
		nY = float(len(LY)) #to avoid Euclidean division
		nX = float(len(LX))
		f = 100. / self.precisionT #to accord resized image's barycentre with full size image
		try:
			return int(f * numpy.sum(LX) / nX + 0.5), int(f * numpy.sum(LY) / nY + 0.5), True
		except ZeroDivisionError:
			return 0, 0, False


	def run(self):
		"""Func ran when the thread is started. Through an infinite loop,
		it emits signals carrying rendered QImage, barycentre coordinates
		and the bool from barycentre func to the main thread.

		It uses openCV (cv2) methods to filter frame's colors and then performs an array-to-QImage conversion.
		The precision attribute set in the GUI by the user is,
		in percents, the size of the resized frame in relation to initial frame size.
		This is this resized frame which is given to the barycentre func.
		"""
		while True:
			_, frame = self.cam.read()

			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

			lowerColor = numpy.array([self.hMinT, self.sMinT, self.vMinT])
			upperColor = numpy.array([self.hMaxT, self.sMaxT, self.vMaxT])

			mask = cv2.inRange(hsv, lowerColor, upperColor)
			res = cv2.bitwise_and(frame, frame, mask=mask)
			resizedRes = cv2.resize(res, (0,0), fx=self.precisionT/100., fy=self.precisionT/100.)

			qImg = QtGui.QImage(res.data, self.w, self.h, QtGui.QImage.Format_RGB888)
			bary = self.barycentre(resizedRes)
			self.emit(QtCore.SIGNAL('refreshFrame(QImage, int, int, bool)'), qImg, bary[0], bary[1], bary[2])



class WorkingSetting(QtGui.QMainWindow, UiSetting):
	"""This is the working part of the program, making the GUI work.

	This class contains all methods used to set the color filter,
	it displays the computed barycente on a little green square.
	Frame rendering and barycentre computation are achieved by a separated QThread.
	"""
	def __init__(self):
		"""WorkingSetting class' constructor. Makes usable the GUI.

		It subclass QMainWindow and UiSetting, shows the UI,
		connects the UI's widgets to WorkingSetting methods and defines some attributes :
		- bounds given to the thread in order to filter colors,
		set by sliders (are ranged in [|0,255|] integers intervall) ;
		- precision attribute given to the thread to set the precision of barycentre computation ;
		- a bool used to know if the user has applied his setting ;
		- a default black QImage displayed when the barycentre func from the thread returns False.
		It also connects the display func with thread's signal and starts it.
		"""
		super(WorkingSetting, self).__init__()
		self.setupUi(self)

		self.hMinSlider.valueChanged.connect(self.refreshHMin)
		self.hMaxSlider.valueChanged.connect(self.refreshHMax)
		self.sMinSlider.valueChanged.connect(self.refreshSMin)
		self.sMaxSlider.valueChanged.connect(self.refreshSMax)
		self.vMinSlider.valueChanged.connect(self.refreshVMin)
		self.vMaxSlider.valueChanged.connect(self.refreshVMax)
		self.precisionSlider.valueChanged.connect(self.refreshPrecision)
		self.resetBtn.clicked.connect(self.resetFilter)
		self.applyBtn.clicked.connect(self.applyFunc)

		self.hMin = 0
		self.hMax = 255
		self.sMin = 0
		self.sMax = 255
		self.vMin = 0
		self.vMax = 255

		self.precision = 40

		self.isApplied = False

		self.blackQPixmap = QtGui.QPixmap(640,480)
		self.blackQPixmap.fill(QtCore.Qt.black)

		self.displaying = DisplayThread()
		self.connect(self.displaying, QtCore.SIGNAL('refreshFrame(QImage, int, int, bool)'), self.displayFunc)
		self.displaying.start()


	def refreshHMin(self):
		self.hMin = self.hMinSlider.value()


	def refreshHMax(self):
		self.hMax = self.hMaxSlider.value()


	def refreshSMin(self):
		self.sMin = self.sMinSlider.value()


	def refreshSMax(self):
		self.sMax = self.sMaxSlider.value()


	def refreshVMin(self):
		self.vMin = self.vMinSlider.value()


	def refreshVMax(self):
		self.vMax = self.vMaxSlider.value()


	def refreshPrecision(self):
		self.precision = self.precisionSlider.value()


	def resetFilter(self):
		self.hMin = 0
		self.hMax = 255
		self.sMin = 0
		self.sMax = 255
		self.vMin = 0
		self.vMax = 255
		self.precision = 40

		self.hMinSlider.setValue(0)
		self.hMaxSlider.setValue(255)
		self.sMinSlider.setValue(0)
		self.sMaxSlider.setValue(255)
		self.vMinSlider.setValue(0)
		self.vMaxSlider.setValue(255)
		self.precisionSlider.setValue(40)


	def displayFunc(self, qImg, bx, by, isOk):
		"""Func communicating with the thread to display rendering frames.

		It converts QImage received in QPixmap in order to display it in the QGraphicsScene object of the GUI,
		provides sliders' values to the thread and displays its rendered images if barycentre func wants it.
		In the case where a barycentre has been computed, a green square locates his position.
		Its size depends of the set precision.
		"""
		currentFrame = QtGui.QPixmap.fromImage(qImg)
		self.displaying.getValues(self.hMin, self.hMax, self.sMin, self.sMax, self.vMin, self.vMax, self.precision)
		self.graphicsScene.clear()

		if isOk:
			self.graphicsScene.addPixmap(currentFrame)
			self.graphicsView.fitInView(QtCore.QRectF(0,0,640,480), QtCore.Qt.KeepAspectRatio)

			squareSide = 400 / self.precision #would be equal to 4px if a full sized frame were given to barycentre func
			squareDims = QtCore.QRectF(bx - squareSide / 2, by - squareSide / 2, squareSide, squareSide)
			self.graphicsScene.addRect(squareDims, QtGui.QPen(QtCore.Qt.green), QtGui.QBrush(QtCore.Qt.green))
		else:
			self.graphicsScene.addPixmap(self.blackQPixmap)
			self.graphicsView.fitInView(QtCore.QRectF(0,0,640,480), QtCore.Qt.KeepAspectRatio)

		self.graphicsScene.update()


	def applyFunc(self):
		self.isApplied = True


	def closeEvent(self, event):
		"""Func overriding the closeEvent func inherited from QWidget.
		It is called when the user push the close button (X button) on the window.

		It takes care the user has well applied his setting, asking a question if not.
		Moreover it kills the thread, breaking its infinite loop, before to quit.
		"""
		if self.isApplied:
			self.displaying.exit()
			event.accept()
		else:
			quitMsg = 'Would you like to apply your setting?'
			msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'Save?', quitMsg, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)

			msgBox.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
			reply = msgBox.exec_()

			if reply == QtGui.QMessageBox.Yes:
				self.applyFunc()
				self.displaying.exit()
				event.accept()
			elif reply == QtGui.QMessageBox.No:
				self.displaying.exit()
				event.accept()
			else: event.ignore()



def main():
	"""To run the whole application.
	"""
	import sys
	app = QtGui.QApplication(sys.argv)
	win = WorkingSetting()
	win.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
