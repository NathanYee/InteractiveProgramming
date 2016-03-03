import numpy as np
import cv2

# set full length numpy arrays
np.set_printoptions(threshold=np.nan)

#make color filter function
def rbgcvt(image):
    lower = [0, 0, 100]
    upper = [50, 50, 255]
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)

    return mask 

cap = cv2.VideoCapture(0)

# Capture frame-by-frame
ret, frame = cap.read()
detection = rbgcvt(frame)

def vertical(image):
    #find average vertical location
    #first find number of successes in each line
    numberLine = []
    for line in image:
        counter = 0
        for value in line:
            if value == 255:
                counter += 1
        numberLine.append(counter)
    #next compute the average vertical distance using distance and weight
    numerator = 0
    for i in range(len(numberLine)):
        numerator += (i+1) *  numberLine[i]
        denominator = np.sum(numberLine)
        vertPos = int(numerator / denominator)
    return vertPos

#next find horizontal positon

# Our operations on the frame come here
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Display the resulting frame

# When everything done, release the capture
