import cv2
from preprocessing import Preprocess
from thresholding import Threshold
from smoothing import Smooth
from contour import Contour
from decision import Decision
import os

SAMPLE_IMAGE = 'thresh1.jpg'
frame = cv2.imread(SAMPLE_IMAGE, cv2.IMREAD_UNCHANGED)
thresholded_image = frame	
smooth_image = Smooth().smoothing(thresholded_image)
contour = Contour().find_contours(smooth_image)
center, radius, probability = Decision().decision(contour, smooth_image)
if radius is not 0:
    # cv2.putText(frame, str(probability * 100) + '%', center, cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
    print("Probability: " + str(probability * 100) + '%')
    cv2.circle(frame, center, radius, (255,0,0), 2)

cv2.imshow('Main video', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()