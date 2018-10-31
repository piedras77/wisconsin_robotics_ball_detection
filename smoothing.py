import cv2
import numpy as np

class Smooth():


    def __init__(self):
        pass

    # we use morphological transformation approach to smooth image
    def smoothing(self, frame):
        # morphological transformations, note that these arent commutative
        kernel = np.ones((12,12))
        #similar to soil erosion,
        #erodes those pixels where all the pizels inside the kernel size are not true
        #kernel size is none, but we will have to calibrate with our balls dataset
        frame = cv2.erode(frame, None, iterations=2)
        #opposite of erotion, assumes the objects can dilate since we probably didnt get the boundary right
        return cv2.dilate(frame, kernel, iterations=2)
