from pathlib import Path
import numpy as np
import face_recognition as fr

import base64, string, random
import cv2

class Identifier:
	def __init__(self):
		self.view = bytes()
		self.encodings = {}
		self.exit = False
		self.friendly_names = {}
		self.allowed = []
		print('loading known people')
		#load known people
		p = Path('people')
		if not (p.exists() and p.is_dir()):
			print(p,'does not exsist as a directory, aborting')
			exit()

		for fn in p.glob('*.jpg'):
			name = fn.stem #filename without extensio
			img = cv2.imread(str(fn))
			print('>>',name)

			try:
				self.encodings[name] = fr.face_encodings(img)[0]
			except Exception as e:
				print('failed to load',fn)
				print('reason:')
				print(e)
	
		# weird pathlib syntax
		p = p / 'meta.txt'
	
		if not(p.exists() and p.is_file()):
			print(p,'does not exist as a file, empty or otherwise')
			exit()
		
		for line in p.open('r').readlines():
			line = line.strip()
			if line == '':
				continue

			line = [x.strip() for x in line.split(',')]
			uid, access = line[0], line[1]

			if uid not in self.encodings.keys():
				print('err: no image for',uid)
				continue
			if bool(access):
				self.allowed.append(uid)

			if len(line) > 2:
				self.friendly_names[uid] = ' '.join(line[2:])

		print('loaded data')

	def setView(self, view):
		self.view = view

	def quit(self):
		self.exit = True

	async def stream(self, response):
		while True:
			r = b''.join([b'--frame\r\nContent-Type:image/jpeg\r\n\r\n', self.view, b'\r\n'])
			await response.write(r)

	def toggleAccess(self, uid):
		if not uid in self.encodings.keys():
			return 'unknown user'
	
		if uid in self.allowed:
			self.allowed.remove(uid)
		else:
			self.allowed.append(uid)

		self.saveMeta()

		return 'ok'

	def hasAccess(self, uid):
		if uid not in self.encodings.keys():
			return False
		if uid in self.allowed:
			return True
		return False

	def saveMeta(self, fn = 'people/meta.txt'):
		p = Path(fn)
		with p.open('w') as f:
			for user in self.encodings.keys():
				allowed = user in self.allowed
				try:
					name = self.friendly_names[user]
				except KeyError:
					name = ''
				f.write('{},{},{}\n'.format(user,allowed,name))


	def addNew(self, thumbnail, encoding):
		# generate random uid 8 char long
		c = string.ascii_uppercase + string.ascii_lowercase + string.digits
		
		uid = ''.join(random.choice(c) for _ in range(8))
		while uid in self.encodings.keys(): #regenerate just incase we have same id, slim chance
			uid = ''.join(random.choice(c) for _ in range(8))

		self.encodings[uid] = encoding
		cv2.imwrite('people/{}.jpg'.format(uid),thumbnail)

		return uid
	def setName(self, uid, name):
		if uid not in self.encodings.keys():
			return False
		if name:
			self.friendly_names[uid] = name
		else:
			del self.friendly_names[uid]
		self.saveMeta()
		return True
		
	def getNames(self):
		ret = []
		for uid in self.encodings.keys():
			if uid in self.friendly_names.keys():
				friendly = self.friendly_names[uid]
			else:
				friendly = None
			ret.append({
				'uid' : uid,
				'friendly' : friendly,
				'name' : friendly or uid, 
				'allowed' : True if uid in self.allowed else False
			})
		print(ret)
		return ret

	def delete(self,uid):
		if not uid in self.encodings.keys():
			return None

		del self.encodings[uid]
		p = Path('people/{}.jpg'.format(uid))
		if p.exists() and p.is_file():
			p.unlink()
	
	def getImageLocation(self, uid):
		if not uid in self.encodings.keys():
			return None
		return 'people/{}.jpg'.format(uid)

	def getIDFromEncoding(self, encoding, difference=0.6):
	
		other_encodings = list(self.encodings.values())
		distances = fr.face_distance(other_encodings, encoding)
		
		if not any([d <= difference for d in distances]):
			#this is a new face that we haven't seen before
			# so save it
			print('no user found')
			return None

		most_similar = np.argmin(distances)

		uid = list(self.encodings.keys())[most_similar] 

		#output debug statement
		print(uid, ' user, with accuracy {:.1%}'.format(1-distances[most_similar]))
		
		#change up this person's encoding a little bit, so we can trend towards true average

		self.encodings[uid] = np.average(
				[ encoding, self.encodings[uid] ],
				axis=0, weights=[1, 2]) # give more weight to the known values

		return uid

