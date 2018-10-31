import cv2


class Threshold():
	GREEN_LOWER = (29, 86, 6) #represents the lower boundary for the green ball
	GREEN_UPPER = (64, 255, 255) #represents the upper boundary for the green we'll accept

	def __init__(self):
		pass

	# applies the first color filter, using only what is inside the color range
	# returns thresholded image, meaning the filtered image
	def thresholding(self, frame):
		return cv2.inRange(frame, self.GREEN_LOWER, self.GREEN_UPPER)