import cv2


class Preprocess():

	def __init__(self):
		pass

	# blur the image to decrease noise from high quality image
	# allows faster processing
	# returns HSV (hue, saturation, value) version of image
	def preprocessing(self, frame):
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		return hsv