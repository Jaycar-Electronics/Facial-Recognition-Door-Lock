import cv2
import numpy as np
import face_recognition as fr
import time
import string
import random
from pathlib import Path
import json
from quart import Quart, websocket

known_people = {}

# list of allowed people to unlock door
allowed_people = []

# dictionary of friendly names
friendly_names = {}

#thumbnails
thumbnails = {} 

#asyncio.run(videoProcessing(True))
vstream = cv2.VideoCapture(0)
while True:
	ret, frame = vstream.read()

	# provide a resize to make it faster
	scaled = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
	

	face_locations = fr.face_locations(scaled)

	for top,right,bottom,left in face_locations:
		
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4
		
		face_img = frame[top:bottom, left:right] #get face image

		# draw a rectangle on the frame for this face
		cv2.rectangle(frame,(left, top), (right, bottom), (255,0,0), 3)


		try:
			# await keyword, do something else until face_encodings returns
			face_encoding = fr.face_encodings(face_img)[0]

		except Exception as e:
			# we could not detect a face in this square, so skip and continue loop
			continue

		other_encodings = list(known_people.values())

		
		distances = fr.face_distance(other_encodings,face_encoding)

		if not any([d <= 0.6 for d in distances]):
			# none of the faces were less than 40% similar.
			# this is a new face, so capture it, and put somewhere.
			storeNewFace(face_encoding, face_img)
			continue

		# otherwise, get the index of the most similar ( minimum ) 
		most_similar = np.argmin(distances) 

		#apply index to keys to get the right key
		person = list(known_people.keys())[most_similar] 
	
		# print a debug statement
		print( '{} ({:.1%})'.format(
			person, 
			(1-distances[most_similar])
		))
	
		# add our captured encoding to the encoding we have 
		# recorded for that user, averging between the two 
		# and giving weight to what we had previously.

		known_people[person] = np.average([
			face_encoding,
			known_people[person]
		], axis=0, weights=[1,2]) # more weight on the known values, 

		if person in allowed_people:
			accessGranted()
		else:
			accessDenied()

	cv2.imshow('Frame',frame)
