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

# This program is a tool to track any object of a certain color with a camera,
# displaying a square on aimed object.
# It was designed to be a tool to configure any program which needs to track
# an specified object with a camera.
# 
# Our project is to use it for creating a 'numeric theremin'
# (search www.google.com to learn what's a theremin) : theremin's player 
# will wear gloves of a certain color and be allowed to play music,
# moving his hands in front of his camera. Before, he will have to use this program
# to set the instrument. That's why this program save user's setting in a file which
# will be used by theremin's program.
# 
# This program is achieved with Python 2.7.13, using OpenCV 3.2.0 and PyQt 4.8.7.
# 
# We are Vanessa Dan, Eve Machefert and Alix Plamont, french students working on this school project.

# This version implements a startup widget which allows the user to choose which camera he wants to use.
# Thus, no or several cameras can be pluggeg without bug.
#
# The code also has a new structure : it is more divided in order to provide a good flexibility.
# The old structure involved a fat main class (which was WorkingSetting). Now the main class,
# DisplayFrames is no more a subclass and is as big as the others. That reduces the number of self attributes
# and makes the code more flexible.

import time
import pickle

from PyQt4 import QtCore, QtGui

from TrackingGUI import UiSetting
from cameraThread import DisplayThread, WorkingCameraSetting



class WorkingSetting(QtGui.QMainWindow, UiSetting):
	"""This is the class making usable the GUI.

	This class contains all methods used to manage widgets ;
	it also handles the file saving. 
	When the user closes the window, a signal is emitted
	in order to connect it with a function from DisplayFrames class.
	That allows a custom close.
	"""
	def __init__(self):
		"""WorkingSetting class constructor.		
		"""
		super(WorkingSetting, self).__init__()
		self.setupUi(self)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose) #makes Qt delete the setting GUI when it's closed
		self.initValues()

		self.hMinSlider.valueChanged.connect(self.refreshHMin)
		self.hMaxSlider.valueChanged.connect(self.refreshHMax)
		self.sMinSlider.valueChanged.connect(self.refreshSMin)
		self.sMaxSlider.valueChanged.connect(self.refreshSMax)
		self.vMinSlider.valueChanged.connect(self.refreshVMin)
		self.vMaxSlider.valueChanged.connect(self.refreshVMax)
		self.precisionSlider.valueChanged.connect(self.refreshPrecision)
		self.resetBtn.clicked.connect(self.resetFilter)
		self.applyBtn.clicked.connect(self.applyFunc)

		self.isApplied = False


	def initValues(self):
		"""This function initializes the values of the bounds (and the values
		of the sliders used to move the bounds) used to filter the frame's colors.

		If there's already a saved file, the bounds pick up their old values.
		"""
		try:
			with open('savedSetting', 'r') as savingFile:
				savingFileUnpickler = pickle.Unpickler(savingFile)				
				self.initList = savingFileUnpickler.load()
		except IOError:
			self.initList = [0, 255, 0, 255, 0, 255, 40]

		#hsv format is used to filter colors
		self.hMin = self.initList[0]
		self.hMax = self.initList[1]
		self.sMin = self.initList[2]
		self.sMax = self.initList[3]
		self.vMin = self.initList[4]
		self.vMax = self.initList[5]
		self.precision = self.initList[6]

		self.hMinSlider.setValue(self.initList[0])
		self.hMaxSlider.setValue(self.initList[1])
		self.sMinSlider.setValue(self.initList[2])
		self.sMaxSlider.setValue(self.initList[3])
		self.vMinSlider.setValue(self.initList[4])
		self.vMaxSlider.setValue(self.initList[5])
		self.precisionSlider.setValue(self.initList[6])


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


	def applyFunc(self):
		"""Saves user's settings in a file, in the form of a python list.
		"""
		with open('savedSetting', 'w') as savingFile:
			savingFilePickler = pickle.Pickler(savingFile)
			L = [self.hMin, self.hMax, self.sMin, self.sMax, self.vMin, self.vMax, self.precision]
			savingFilePickler.dump(L)
		self.isApplied = True
		self.close()


	def isOkToClose(self):
		"""On exit, if the user has applied or didn't modify nothing, returns True.
		Else, returns False.
		"""
		L = [self.hMin, self.hMax, self.sMin, self.sMax, self.vMin, self.vMax, self.precision]
		return self.isApplied or self.initList == L


	def drawQuitMsg(self):
		"""Provides the message drawn when isOkToClose returns False.
		"""
		quitMsg = 'Would you like to apply your setting?'
		msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'Save?', quitMsg, QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel)
		msgBox.setWindowFlags(QtCore.Qt.CustomizeWindowHint|QtCore.Qt.WindowTitleHint)
		return msgBox.exec_()

	def closeEvent(self, event):
		"""Overrides the QWidget closeEvent function in order to make a custom quit.
		"""
		self.emit(QtCore.SIGNAL('closeSettingGUI(QCloseEvent)'), event)



class DisplayFrames():
	"""Thiss class is the main class of this tool. It manages the other classes
	and provides methods to control camera settings and frame displaying.

	It handles all the display part of this program, from cameras to drawing on GUI.
	Several QObjects are connected to its functions.
	"""
	def __init__(self, RESPONSE_TIME=0.25):
		"""DisplayFrames class constructor. Makes connections with QObjects.

		The optional argument is the waiting period (in seconds) during
		which a camera is called, used or released. This delay avoids OpenCV
		errors about the camera.
		"""
		self.CAM_RESPONSE_TIME = RESPONSE_TIME

		self.mainWorkingGUI = WorkingSetting()
		self.mainWorkingGUI.connect(self.mainWorkingGUI, QtCore.SIGNAL('closeSettingGUI(QCloseEvent)'), self.closeEvent) #the closeEvent

		self.blackQPixmap = QtGui.QPixmap(640, 480)  #A default black QPixmap is defined here in order
		self.blackQPixmap.fill(QtCore.Qt.black)                #to display it when no barycentre can be computed.

		self.cameraUI = WorkingCameraSetting(self.CAM_RESPONSE_TIME)
		self.cameraUI.connect(self.cameraUI.cameraChoice, QtCore.SIGNAL('activated(int)'), self.changeCamIndex) #the drop-down box
		self.cameraUI.refreshBtn.clicked.connect(self.refreshCameras)
		self.cameraUI.OKBtn.clicked.connect(self.applyCameraSetting)

		self.displaying = DisplayThread(self.CAM_RESPONSE_TIME)
		self.displaying.getValues(self.mainWorkingGUI.hMin, self.mainWorkingGUI.hMax, self.mainWorkingGUI.sMin, self.mainWorkingGUI.sMax, self.mainWorkingGUI.vMin, self.mainWorkingGUI.vMax, self.mainWorkingGUI.precision)
		self.displaying.connect(self.displaying, QtCore.SIGNAL('refreshFrame(QImage, int, int, bool)'), self.displayFunc)

		self.initCam()


	def initCam(self):
		"""If that's possible, defines a camera on open.
		"""
		initIndex = self.cameraUI.cameraChoice.currentIndex()
		if initIndex != -1:
			self.displaying.defineCamera(initIndex)
			self.displaying.startCapture()
			self.displaying.start()


	def refreshCameras(self):
		"""Refreshes the list of the plugged cameras,
		taking care to interrupt displaying before.
		"""
		self.displaying.stopCapture()
		time.sleep(self.CAM_RESPONSE_TIME)
		self.cameraUI.callCameraSetting()
		self.initCam()


	def changeCamIndex(self, index):
		"""Function used to change the camera,
		replacing it by the camera of index <index>.
		"""
		self.displaying.stopCapture()
		time.sleep(self.CAM_RESPONSE_TIME)
		self.displaying.defineCamera(index)
		self.displaying.startCapture()
		self.displaying.start()


	def applyCameraSetting(self):
		"""Called when OK button from camera widget is pushed.

		If no camera was detected, it closes all.
		Else, it destroys the widget.
		"""
		if self.cameraUI.cameraChoice.currentIndex() == -1:
			print 'A camera must be plugged to make the program start.'
			self.mainWorkingGUI.close()
			self.cameraUI.close()
		else: self.cameraUI.close()


	def displayFunc(self, qImg, bx, by, isOk):
		"""Function communicating with the thread to display rendering frames.

		It converts the received QImage in a QPixmap in order to display it in the
		QGraphicsScene object from the main GUI,
		provides the sliders' values to the thread and displays its rendered images
		if barycentre function wants it.
		In the case where a barycentre has been computed, a green square locates his position.
		Its size depends on the set precision.
		"""
		currentFrame = QtGui.QPixmap.fromImage(qImg)
		self.displaying.getValues(self.mainWorkingGUI.hMin, self.mainWorkingGUI.hMax, self.mainWorkingGUI.sMin, self.mainWorkingGUI.sMax, self.mainWorkingGUI.vMin, self.mainWorkingGUI.vMax, self.mainWorkingGUI.precision)
		self.mainWorkingGUI.graphicsScene.clear()

		if isOk:
			self.mainWorkingGUI.graphicsScene.addPixmap(currentFrame)
			self.mainWorkingGUI.graphicsView.fitInView(QtCore.QRectF(0,0,640,480), QtCore.Qt.KeepAspectRatio)

			squareSide = 400 / self.mainWorkingGUI.precision #would be equal to 4px if a full sized frame was given to barycentre function
			squareDims = QtCore.QRectF(bx - squareSide / 2, by - squareSide / 2, squareSide, squareSide)
			self.mainWorkingGUI.graphicsScene.addRect(squareDims, QtGui.QPen(QtCore.Qt.green), QtGui.QBrush(QtCore.Qt.green))
		else:
			self.mainWorkingGUI.graphicsScene.addPixmap(self.blackQPixmap)
			self.mainWorkingGUI.graphicsView.fitInView(QtCore.QRectF(0,0,640,480), QtCore.Qt.KeepAspectRatio)

		self.playMusic(bx, by)
		self.mainWorkingGUI.graphicsScene.update()


	def playMusic(self, bx, by):
		""" This function play a music note depending on the barycentre position.
		"""
		pass


	def closeEvent(self, event):
		"""The custom closeEvent function. 
		Asks the user to confirm the saving of his settings
		and disconnects properly the camera.
		"""
		if self.mainWorkingGUI.isOkToClose():
			self.displaying.stopCapture()
			time.sleep(self.CAM_RESPONSE_TIME) #to allow camera releasing
			self.displaying.exit()
			event.accept()
		else:
			reply = self.mainWorkingGUI.drawQuitMsg()
			if reply == QtGui.QMessageBox.Yes:
				self.mainWorkingGUI.applyFunc()
				self.displaying.stopCapture()
				time.sleep(self.CAM_RESPONSE_TIME)
				self.displaying.exit()
				event.accept()
			elif reply == QtGui.QMessageBox.No:
				self.displaying.stopCapture()
				time.sleep(self.CAM_RESPONSE_TIME)
				self.displaying.exit()
				event.accept()
			else: event.ignore()



def main():
	"""To run the whole application.
	"""
	import sys
	app = QtGui.QApplication(sys.argv)
	prog = DisplayFrames()
	prog.mainWorkingGUI.show()
	prog.cameraUI.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
