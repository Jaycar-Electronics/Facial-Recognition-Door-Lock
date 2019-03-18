import cv2
import base64, webbrowser
import numpy as np

image = cv2.imread('someimage.png')


ret, image = cv2.imencode('.jpg', image)

bimage = base64.b64encode(image)

print('data:image/jpg;base64,{}'.format(bimage.decode()))

