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

# This file contains the two classes that use OpenCV.
# It provides all methods to manage cameras and frame rendering.

from functools import reduce
import time
import numpy

from PyQt4 import QtCore, QtGui
import cv2

from CameraSetting import CameraUI


class WorkingCameraSetting(QtGui.QDialog, CameraUI):
	"""This class is the working part of the widget allowing
	the user to choose a camera.

	It detects all the cameras OpenCV can open and display
	their index in the widget's list box (a QComboBox).
	It also informs the user on what he must do with his
	camera settings.
	"""
	def __init__(self, camResponseTime):
		"""WorkingCameraSetting class constructor. 

		It needs one argument : <camResponseTime> is the
		waiting period (in seconds) during which a camera
		is called. This delay avoids undetected cameras.
		"""
		super(WorkingCameraSetting, self).__init__()
		self.CAM_RESPONSE_TIME = camResponseTime
		self.setupCameraUi(self)
		self.setWindowFlags(QtCore.Qt.CustomizeWindowHint|QtCore.Qt.WindowTitleHint)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose) #makes Qt delete the dialog when it's closed
		self.setModal(True) #disables the main window when open
		self.callCameraSetting()


	def cameraDetection(self):
		"""Provide the list of indexes of the connected cameras.

		There is a reported bug concerning OpenCV and Logitech cameras.
		Nevertheless, this function seems work and detect all the plugged cameras.
		"""
		camList = []
		index = 0
		cam = cv2.VideoCapture(index)
		time.sleep(self.CAM_RESPONSE_TIME)
		while cam.isOpened():
			camList.append(str(index))
			index += 1
			cam = cv2.VideoCapture(index)
			time.sleep(self.CAM_RESPONSE_TIME)
		cam.release()
		#the errors when index is wrong can't be avoided, that's why the following msg
		print '#########################################################\nIf you are executing this program in a console,\nsome errors can occur. Please do not take care of that :\nthese errors occur when the function used to detect\nthe cameras plugged on the machine try to connect\nan unplugged camera.\nAll is alright.\nBut still be carefull : other errors are not allowed.\n#########################################################\n'
		del cam
		return camList


	def refreshCamera(self):
		"""Refreshes the list box with the list provided by cameraDetection method.

		Calls cameraDetection and Returns the number of cameras.
		"""
		CameraList = self.cameraDetection()
		QCameraList = QtCore.QStringList(CameraList)
		self.cameraChoice.clear()
		self.cameraChoice.addItems(QCameraList)
		return len(CameraList)


	def callCameraSetting(self):
		"""Depending on the number of plugged cameras, this function displays
		a message in the text box that indicates what to do to the user.

		Calls refreshCamera and then cameraDetection methods.
		"""
		cameraNb = self.refreshCamera()
		if cameraNb == 0:
			msg = 'Unable to find a camera, please plug one or retry. \n\nIf it still doesn\'t work, ensure you that your camera works.\nIf you have plugged more than one camera, ensure you that the cameras are not plugged on the same USB hub.'
			QMsg = QtCore.QString(msg)
			self.textZone.setPlainText(QMsg)
		elif cameraNb == 1:
			msg = 'One camera found! Push \'OK\' button to start'
			QMsg = QtCore.QString(msg)
			self.textZone.setPlainText(QMsg)
		else:
			msg = 'Several cameras found!\nPlease choose one beside and push \'OK\' button to start.'
			QMsg = QtCore.QString(msg)
			self.textZone.setPlainText(QMsg)



class DisplayThread(QtCore.QThread):
	"""This class is a QThread designed to relieve the main thread for frame rendering computations.

	It provides the current filtered frame in the form of a QImage to the main thread
	(DisplayFrames class) and also computes the barycentre's coordinates.
	OpenCV module is used for video capture and frame rendering.
	"""
	def __init__(self, camResponseTime):
		"""DisplayThread class constructor.

		It needs one argument : <camResponseTime> is the
		waiting period (in seconds) during which a camera
		is called, used or released. This delay avoids OpenCV
		errors about the camera.
		"""
		super(DisplayThread, self).__init__()
		self.isRunning = False
		self.CAM_RESPONSE_TIME = camResponseTime


	def __del__(self):
		"""This function makes part of QThread's structure.
		"""
		self.wait()


	def defineCamera(self, index):
		"""Defines a camera object from the camera indexed on
		<index> and takes his resolution.
		"""
		self.cam = cv2.VideoCapture(index)
		time.sleep(self.CAM_RESPONSE_TIME)
		_, frame = self.cam.read() #frame sample to take resolution
		self.w, self.h = frame.shape[1], frame.shape[0]


	def getValues(self, hmin, hmax, smin, smax, vmin, vmax, prec):
		"""Func used to synchronize bounds and precision with values of GUI's sliders.

		Precision attribute is used to make the barycentre computation faster,
		see run function documentation for more details.
		"""
		self.hMinT = hmin
		self.hMaxT = hmax
		self.sMinT = smin
		self.sMaxT = smax
		self.vMinT = vmin
		self.vMaxT = vmax
		self.precisionT = prec


	def startCapture(self):
		"""Function used to start video capture.

		See run function documentation for more details.
		"""
		self.isRunning = True


	def stopCapture(self):
		"""Function used to stop video capture and then to release the camera.

		See run function documentation for more details.
		"""
		self.isRunning = False


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
		"""Function ran when the thread is started. Through a loop,
		it emits signals carrying the rendered QImage, the barycentre coordinates,
		and the bool from barycentre function to the main thread (DisplayFrames class).

		It uses openCV (cv2) methods to filter frame's colors and then
		performs an array-to-QImage conversion.
		The precision attribute set in the GUI by the user is, in percents, 
		the size of the resized frame in relation to the initial frame size.
		This is this resized frame which is given to the barycentre func.
		When the loop is stopped (when stopCapture method is called),
		this func releases the camera. stopCapture also stops the thread.
		The video capture starts if startCapture method was called and,
		then, if the thread was started.
		"""
		while self.isRunning:
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

		self.cam.release()