import sys, pygame
pygame.init()

size = width, height = 1280, 920
black = 0, 0, 0

screen = pygame.display.set_mode(size)

left_third = width/3.0
right_third = 2.0 * (left_third)
top_third = height/3.0
bottom_third = 2.0 * (top_third)

# Initializing the game state
cell_states = dict()
for i in range(3):
    for j in range(3):
        cell_states[(i,j)] = 0

def print_game_state(i,j):
    """ Prints game state as a matrix"""
    for i in range(3):
        for j in range(3):
            print cell_states.get((i,j)),
        print ""

def find_third(pos):
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


while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT: sys.exit()

        #control loop
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            
            #update clicked cell
            cell_states[find_third(pos)] = 1
            
            print_game_state(i,j)

    screen.fill(black)
    # screen.blit(ball, ballrect)
    pygame.display.flip()


