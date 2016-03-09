import cv2
import numpy as np

def grid(x,y):
    x = x/640.
    y = y/480.

    if x < .33:
        x_return = 0
    elif x < .66:
        x_return = 1
    else:
        x_return = 2

    if y < .33:
        y_return = 0
    elif y < .66:
        y_return = 1
    else:
        y_return = 2

    return x_return, y_return

cap = cv2.VideoCapture(0)

# take first frame of the video
ret, frame = cap.read()

# define range of green color in HSV
lower_blue = np.array([50,75,50])
upper_blue = np.array([75,150,200])

# setup initial location of window
r,h,c,w = 200,120,260,120  # simply hardcoded the values
track_window = (c,r,w,h)

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv_roi, lower_blue, upper_blue)

roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):

    # Take each frame
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

    # Threshold the HSV image to get only blue colors

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    ret, track_window = cv2.meanShift(dst, track_window, term_crit)

    #draw it on frame
    x,y,w,h = track_window

    print (x+(w/2), y+(h/2))

    img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
