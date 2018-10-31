import numpy as np
import cv2
import time
import math
from random import random

GREEN_LOWER = (29, 86, 6) #represents the lower boundary for the green ball
GREEN_UPPER = (64, 255, 255) #represents the upper boundary for the green we'll accept

IMG_WIDTH = 600
IMG_HEIGHT = 540

camera = cv2.VideoCapture(0) #access the camera, currently webcam 
time.sleep(2) #allows the camera to load
hugh_center = (0, 0)
probability = 0

def get_circle(image, radius, contours):
	width, height = image.shape
	accumulator_matrix = np.zeros([width, height], dtype=int)
	local_maxima = (0, 0)
	max_value = -1
	for pixel in contours:
		for theta in range(0, 361):
			a = int( pixel[0][0] - radius * math.cos(theta * math.pi / 180) ) #polar coordinate for center
	  		b = int( pixel[0][1] - radius * math.sin(theta * math.pi / 180) ) #polar coordinate for center 

	  		if a >= len( accumulator_matrix ) or b >= len( accumulator_matrix[0] ):
	  			continue

	  		accumulator_matrix[a][b] += 1
	  		if accumulator_matrix[a][b] > max_value:	
				max_value = accumulator_matrix[a][b]
				local_maxima = (a, b)

	return local_maxima

def get_probability(A, B, radius):
	x = A[0] - B[0] #delta x
	y = A[1] - B[1] #delta y
	d = math.sqrt( (x * x) + (y * y) ) / radius #distance between the two centers
	if d > radius: #circles do not overlap
		return 0

	P = (2 * np.arccos(d/2) - d * math.sqrt( 1 - ( ( d * d ) ) / 4 ) ) / math.pi
	return P

def morphological_transformations():
	pass

while True:
	valid, frame = camera.read()
	#blur the image to decrease noise from high quality image, allows faster processing
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	#applies the first color filter, using only what is inside the color range
	filtered = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
	#morphological transformations, note that these arent commutative
	kernel = np.ones((12,12))
	#similar to soil erosion,
	#erodes those pixels where all the pizels inside the kernel size are not true
	#kernel size is none, but we will have to calibrate with our balls dataset
	filtered = cv2.erode(filtered, None, iterations=2)
	#opposite of erotion, assumes the objects can dilate since we probably didnt get the boundary right
	filtered = cv2.dilate(filtered, kernel, iterations=2)

	#compute contours of our binary image
	modified_image, contours, hierarchy = cv2.findContours(filtered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	print("Contours: " + str(type(contours)))
	center = None
	#only when something was found, we can draw contours
	if len( contours ):
		#gets the biggest 'most outstaiding' contour from all the contours
		outstading_object = max(contours, key=cv2.contourArea)
		#gets the smalles possible circle that can enclose everything of the contour
		((x,y), radius) = cv2.minEnclosingCircle(outstading_object)
		center = (int(x), int(y))	
		radius = int(radius)

		#TODO: get actual size range of a tennis ball with reference object
		#and compute radius max and min based on reference object and obtained radius
		if radius > 2:
			cv2.circle(frame, center,radius, (255,0,0), 2) #draws circle in main image
			cv2.circle(frame, hugh_center,radius, (0,0,0), 2)
			# getting the hugh's radius is expensive, 
			# and since the ball is static we don't need to update it for every frame
			if random() < 0.1:
				hugh_center = get_circle(modified_image, radius, outstading_object)
				if len(hugh_center) is not 0:
					probability = get_probability(center, hugh_center, radius)

			cv2.putText(frame, str(probability * 100) + '%', hugh_center, cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)



	cv2.putText(frame, 'position: ' + str(center), (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
	cv2.imshow('Filtered video', modified_image)
	cv2.imshow('Main video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
