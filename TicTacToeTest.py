import sys, pygame
import cv2
import numpy as np
import random
import time
from time import time

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

pygame.init()

def print_game_state(i,j):
    """ Prints game state as a matrix"""
    for i in range(3):
        for j in range(3):
            print cell_states.get((i,j)),
        print ""

def find_third(pos):
    """ Finds which box was clicked in """
    #determine which third the click was in (veritcal rectangles)
    if pos[0] < left_third:
        j = 0
    elif left_third <= pos[0] and pos[0]  <= right_third:
        j = 1
    elif right_third <= pos[0]:
        j = 2

    #determine which third the click was in (horizontal rectangles)
    if pos[1] < top_third:
        i = 0
    elif top_third <= pos[1] and pos[1]  <= bottom_third:
        i = 1
    elif bottom_third <= pos[1]:
        i = 2
    return (i , j)

def generate_random_cell():
    """
    generate_random_cell generates a random cell to be used by the computer player
    """
    i = random.randint(0,2)
    j = random.randint(0,2)
    # print i,j
    return (i , j)

def check_for_win(cell_states):
    """
    Takes the game state dictionary and checks to see if there is a winner.  Calls declare_winner if there is a winner.
    """
    #check verticals
    for j in range(3):
        if ( cell_states.get((0,j)) == cell_states.get((1,j)) 
            == cell_states.get((2,j)) != 0) : 
            declare_winner(cell_states.get((0,j)))
    #check horizontals
    for i in range(3):
        if ( cell_states.get((i, 0)) == cell_states.get((i, 1)) 
            == cell_states.get((i ,2)) != 0) : 
            declare_winner(cell_states.get((i, 0)))
    #check diagonals
    if (cell_states.get((0, 0)) == cell_states.get((1, 1)) 
            == cell_states.get((2,2)) != 0) :
            declare_winner(cell_states.get((1, 1))) 
    elif (cell_states.get((2, 0)) == cell_states.get((1, 1)) 
            == cell_states.get((0, 2)) != 0) :
            declare_winner(cell_states.get((1, 1)))

def declare_winner(int):
    """
    declare_winner determines which player wins the game and prints to the console
    """
    if int == 1:
        print "Player 1 wins"
    elif int == -1:
        print "Player 2 wins"


size = width, height = 1280, 920
black = 0, 0, 0
red = 200, 0, 0
blue = 0, 0, 200

screen = pygame.display.set_mode(size)

# Initializing the game state
cell_states = dict()
for i in range(3):
    for j in range(3):
        cell_states[(i,j)] = 0

#Find the screen's "thirds"
left_third = width/3.0
right_third = 2.0 * (left_third)
top_third = height/3.0
bottom_third = 2.0 * (top_third)

#Creating borders
left = pygame.Rect((left_third-5.0), 0, 10, height)
pygame.draw.rect(screen, (200,200,200) , left)
right = pygame.Rect((right_third-5.0), 0, 10, height)
pygame.draw.rect(screen, (200,200,200) , right)
top = pygame.Rect(0, (top_third-5.0), width, 10)
pygame.draw.rect(screen, (200,200,200) , top)
bottom = pygame.Rect(0, (bottom_third-5.0), width, 10)
pygame.draw.rect(screen, (200,200,200) , bottom)

rect_widths = (width-20)/3.0
rect_heights = (height-20)/3.0
rect_x_pos = [0, left_third+5, right_third+5]
rect_y_pos = [0, top_third+5, bottom_third+5]

#creates a dictionary of rectangles
rect_dict = dict()
for i in range(len(rect_x_pos)):
    for j in range(len(rect_y_pos)):
        rect_dict[(j,i)] = pygame.Rect(rect_x_pos[i], rect_y_pos[j], rect_widths, rect_heights)

turn = 0 #initialize the turn

t = time() #capture the current time.  Will update gamestate when the time is at least three seconds later


while True: #main control loop
    # Take each frame
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

    # Threshold the HSV image to get only blue colors

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    # res = cv2.bitwise_and(frame,frame, mask= mask)

    ret, track_window = cv2.meanShift(dst, track_window, term_crit)

    # #draw it on frame
    x,y,w,h = track_window

    img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    # cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


    for event in pygame.event.get():

        if event.type == pygame.QUIT: sys.exit()

        #control loop

    if time() > t + 3: 
        t = time()
        pos = (2*(x+(w/2)), 2*(y+(h/2))) #green ball location
        # print pos

        #update clicked cell
        if cell_states[find_third(pos)] == 0 and (turn % 2 == 0) :
            #user input
            cell_states[find_third(pos)] = 1
            update_rectangle = rect_dict.get(find_third(pos))
            pygame.draw.rect(screen, blue, update_rectangle)
            turn +=1
            check_for_win (cell_states)

            #AI turn
            random_cell = generate_random_cell()
            cell_states[random_cell] = -1
            update_rectangle = rect_dict.get(random_cell)
            pygame.draw.rect(screen, red, update_rectangle)

            turn +=1

        # print_game_state(i,j)

        check_for_win (cell_states)

    pygame.display.flip()

#close opencv windows
cv2.destroyAllWindows()


