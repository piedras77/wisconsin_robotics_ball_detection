import cv2

class Contour():

    def __init__(self):
        pass

    def find_contours(self, frame):
        #compute contours of our binary image
        # from cv documentation: we need binary image 
        modified_image, contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        center = None
        #only when something was found, we can draw contours
        if len( contours ):
            #gets the biggest 'most outstaiding' contour from all the contours
            outstading_object = max(contours, key=cv2.contourArea)
            return outstading_object

        return []
