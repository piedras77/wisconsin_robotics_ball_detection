import cv2
import numpy as np
import math

class Decision():
    def __init__(self):
        pass

    def get_circle(self, image, radius, contours):
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

    def get_probability(self, A, B, radius):
        x = A[0] - B[0] #delta x
        y = A[1] - B[1] #delta y
        d = math.sqrt( (x * x) + (y * y) ) / radius #distance between the two centers
        if d > radius: #circles do not overlap
            return 0

        P = (2 * np.arccos(d/2) - d * math.sqrt( 1 - ( ( d * d ) ) / 4 ) ) / math.pi
        return P

    def decision(self, contour, frame):
        center_of_mass = (-1, -1)
        radius = 0
        probability = 0
        if len(contour) is 0:
            return center_of_mass, radius, probability

        # gets the smalles possible circle that can enclose everything of the contour
        ((x,y), radius) = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))   
        radius = int(radius)

        # anything less than 2, is noise
        if radius > 2:
            # getting the hugh's radius is expensive, 
            # and since the ball is static we don't need to update it for every frame
            if True : # random() < 0.2:
                hugh_center = self.get_circle(frame, radius, contour)
                if len(hugh_center) is not 0:
                    probability = self.get_probability(center, hugh_center, radius)
                    if probability > 0.6:
                        print(probability)
                        center_of_mass = center


        return center_of_mass, radius, probability
