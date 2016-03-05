import sys, pygame
pygame.init()

size = width, height = 1280, 920
speed = [1, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print pos [0]
            # print ballrect.left, pos[0], ballrect.right
            # print ballrect.bottom, pos[1], ballrect.top
            if ballrect.left < pos[0] and pos[0] <  ballrect.right: 
                print "true"
                if ballrect.bottom > pos[1] and pos[1] > ballrect.top:
                    print "true"
                    speed = [0,0]


    ballrect = ballrect.move(speed)
    if ballrect.left < 0:
        speed[0] = -speed[0]*.99
        if abs(speed[0]) < 2:
            speed[0] += 2
    if ballrect.right > width:
        speed[0] = -speed[0]*.99
        if abs(speed[0]) < 2:
            speed[0] -= 2
    if ballrect.top < 0:
        speed[1] = -speed[1]*.99
        if abs(speed[0]) < 2:
            speed[0] += 2
    if ballrect.bottom > height:
        speed[1] = -speed[1]*.99
        if abs(speed[0]) < 2:
            speed[0] -= 2

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()