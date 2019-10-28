#!/usr/bin/python3
import cv2
import numpy as np
import face_recognition
import time
#import gpiozero

#relay = LED(3) # relay pin, modelled as a "LED"

def unlockDoor(timeout):
	#relay.blink(timeout, 0, 1)
	print('unlock door')

#video_stream = VideoStream(usePiCamera=True).start()
video_stream = cv2.VideoCapture(0)

face_locations = []
time.sleep(2)

while(True):
	ret, frame = video_stream.read()
	# resize to make it faster
	scaled = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)

	face_locations = face_recognition.face_locations(scaled)

	for top,right,bottom,left in face_locations:
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4

		face_img = frame[top:bottom, left:right]
		cv2.imshow('Face', face_img)
	cv2.imshow('Frame', scaled)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video_stream.release()
cv2.destroyAllWindows()

