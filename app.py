import cv2
from preprocessing import Preprocess
from thresholding import Threshold
from smoothing import Smooth
from contour import Contour
from decision import Decision

camera = cv2.VideoCapture(0) #access the camera, currently webcam 
while True:
    valid, frame = camera.read()
    preprocessed_image = Preprocess().preprocessing(frame)
    thresholded_image = Threshold().thresholding(preprocessed_image)
    smooth_image = Smooth().smoothing(thresholded_image)
    contour = Contour().find_contours(smooth_image)
    center, radius = Decision().decision(contour, smooth_image)
    if radius is not 0:
        cv2.circle(frame, center, radius, (255,0,0), 2)

    cv2.imshow('Main video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
