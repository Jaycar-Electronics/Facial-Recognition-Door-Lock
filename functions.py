import cv2
import numpy as np
import asyncio
import face_recognition as fr
import time
import string
import random
from pathlib import Path
import json
from picamera.array import PiRGBArray
from picamera import PiCamera


import gpiozero

relay = gpiozero.LED(14)

def accessGranted(name=None):
	relay.blink(5, 1, 1)
	# put any code here that you want to activate when the door is meant to be unlocked
	# this should be done as quickly as possible
	print('Acess Granted')
	if name:
		print('Hello',name)


def accessDenied(name=None):
	# put any code here that you want to activate when the door is kept locked
	# this should be done as quickly as possible
	relay.off()
	print('Access Denied')
	pass

# ---------------------------------------------------------------------------------------
# this is the video processing routine using asyncio

async def videoProcessing(identifier, imshow=False):

	#vstream = cv2.VideoCapture(0)  #desktop webcamera
	picam = PiCamera()
	picam.resolution = ( 1280, 720 )
	raw = PiRGBArray(picam)

	print('started video stream')
	await asyncio.sleep(0.1)

	while True:
		#await sleeps to cut up the loop and do other stuff
		await asyncio.sleep(0.1)
		if identifier.exit:
			break
	
		print('detectloop')
		try:
			raw.seek(0)
			raw.truncate()
			picam.capture(raw, format='bgr', use_video_port=True)
			frame = raw.array
		except Exception as e:
			print(e)
			continue


		#scaled is faster
		scaled = cv2.resize(frame,None, fx=0.5, fy=0.5)
		face_locations = fr.face_locations(scaled)
		

		for top,right,bottom,left in face_locations:
			
			# draw a rectangle on the frame for this face
			cv2.rectangle(scaled,(left, top), (right, bottom), (255,0,0), 3)

			top *= 2
			bottom *= 2
			right *= 2
			left *= 2

			face_img = frame[top:bottom, left:right] #extract face image


			try:
				await asyncio.sleep(0.1)	
				face_encoding = fr.face_encodings(face_img)[0]

			except Exception as e:
				# we could not detect a face in this square, so skip and continue loop
				continue

			person = identifier.getIDFromEncoding(face_encoding)

			if person is None:
				# it is a new person, 
				# so lets generate a new ID
				# and save it
				print('adding new person')
				identifier.addNew(face_img, face_encoding)
				continue

			if identifier.hasAccess(person):
				accessGranted()
			else:
				accessDenied()

		ret, v = cv2.imencode('.jpg', scaled)
		identifier.setView(v)

	#cleanup after breakout of loop
	picam.close()
	#vstream.release()
	cv2.destroyAllWindows()

