#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br>

import RPi.GPIO as gp
import time
import numpy as np
import os
import io
import cv2
import picamera
import picamera.array
from PIL import Image

def configureMultiCamera():
	gp.setwarnings(False)
	gp.setmode(gp.BOARD)

	gp.setup(7, gp.OUT)
	gp.setup(11, gp.OUT)
	gp.setup(12, gp.OUT)

	gp.setup(15, gp.OUT)
	gp.setup(16, gp.OUT)
	gp.setup(21, gp.OUT)
	gp.setup(22, gp.OUT)

	gp.output(11, True)
	gp.output(12, True)
	gp.output(15, True)
	gp.output(16, True)
	gp.output(21, True)
	gp.output(22, True)

def enableCamera(num):
	if num == 1:
		gp.output(7, False)
		gp.output(11, False)
		gp.output(12, True)
	elif num == 2:
		gp.output(7, True)
		gp.output(11, False)
		gp.output(12, True)
	elif num == 3:
		gp.output(7, False)
		gp.output(11, True)
		gp.output(12, False)
	elif num == 4:
		gp.output(7, True)
		gp.output(11, True)
		gp.output(12, False)

def disableMultiCamera():
	gp.output(7, False)
	gp.output(11, False)
	gp.output(12, True)

def capture(cam):
    camera.capture('foto-'  + str(cam) + '.jpg')
    
def displayImage(img, mode):
	"""
	Displays the four images
	"""
	if not len(img) <= 0 and mode == 1:
		height, width, z = img[0].shape
		if len(img) < 4:
			for i in xrange(4 - len(img), 4):
				img.append(np.zeros((height, width, 3), dtype=np.uint8))
		#identifying the images
		cv2.putText(img[0], 'Cam 1', (5, 10), cv2.FONT_HERSHEY_SIMPLEX, .4, 255)
		cv2.putText(img[1], 'Cam 2', (5, 10), cv2.FONT_HERSHEY_SIMPLEX, .4, 255)
		cv2.putText(img[2], 'Cam 3', (5, 10), cv2.FONT_HERSHEY_SIMPLEX, .4, 255)
		cv2.putText(img[3], 'Cam 4', (5, 10), cv2.FONT_HERSHEY_SIMPLEX, .4, 255)
		#Combines the images into one to display
		image = np.zeros((2 * height, 2 * width, 3), dtype=np.uint8)
		image[0:height, 0:width, :] = img[0]
		image[height:, 0:width, :] = img[2]
		image[0:height, width:, :] = img[1]
		image[height:, width:, :] = img[3]
		# Display
		cv2.imshow('Multi-Camera Raspberry Pi by Maik', image)
	if mode == 2:
		for i in xrange(0, len(img)):
			cv2.imshow('Camera ' + str(i+1), img[i])
		

if __name__ == "__main__":
	numberOfCameras = int(input("Number of cameras:"))
	configureMultiCamera()
	with picamera.PiCamera() as camera:
		
		#camera settings
		camera.resolution = [160,112]
		camera.framerate = 30
		
		#time to wait for the settings to be applied successfully
		time.sleep(2)
		
		#create all camera streams
		stream = list()
		for i in xrange(1,numberOfCameras+1):
			stream.append(io.BytesIO())
			
		while True:
			
			startTime = time.time()
			
			img = list()
			
			for i in xrange(1,numberOfCameras+1):
				enableCamera(i)
				camera.capture(stream[i-1], format='jpeg')
				data = np.fromstring(stream[i-1].getvalue(), dtype=np.uint8)
				#Decode the image from the array, preserving colour
				image = cv2.imdecode(data, 1)
				#get the array of the image
				img.append(image.copy())
				#Delete the contents of a stream.
				stream[i-1].seek(0)
			
			#Display all images
			displayImage(img, 1)
			#displayImage(img, 2)
			
			totalTime = time.time() - startTime
			print "Aquisition time: %f s" %(totalTime)
			print "FPS(all cameras): %f" %(1 / totalTime)
			
			# If we press ESC then break out of the loop
			key = cv2.waitKey(7) % 0x100
			if key == 27:
				break
			
	disableMultiCamera()
	#Clears the cash at the end of the application
	cv2.destroyAllWindows()

