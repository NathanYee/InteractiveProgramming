import numpy as np
import cv2

# # set full length numpy arrays
# np.set_printoptions(threshold=np.nan)



#make color filter function
def rbgcvt(image):
    lower = [0, 0, 100]
    upper = [100, 100, 255]
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    #output = cv2.bitwise_and(image, image, mask = mask)

    return mask

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
def horizontal(image):
    #first find number of success for vertical line
    numberVertLine = []
    total = 0
    for i in range(len(image[0])):
        counter = 0
        for line in image:
            if line[i] == 255:
                counter += 1
                total += 1
        numberVertLine.append(counter*(i+1))


    return np.sum(numberVertLine)/total

#create capture object
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    detection = rbgcvt(frame)

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',detection)
    print (horizontal(detection)/640., vertical(detection)/480.)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print (horizontal(detection)/640., vertical(detection)/480.)

# cv2.imshow("image", detection)
# cv2.waitKey(0)
# # Our operations on the frame come here
# # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# # Display the resulting frame

# # When everything done, release the capture
cap.release()
