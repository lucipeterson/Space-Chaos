import pygame
import time
import random

pygame.init()

#DISPLAY
display_width = 800
display_height = 600

#COLORS
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
bluegreen = (0, 200, 98)
thingcolors = [white, red, bluegreen]

#IMAGES
gameIcon = pygame.image.load('space-ship.gif')
bg = pygame.image.load("spaceabyss.png")
shipImg = pygame.image.load('space-ship.gif')

ship_width = 73
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_icon(gameIcon)
clock = pygame.time.Clock()
pygame.display.set_caption('Space Chaos')

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.circle(gameDisplay, random.choice(thingcolors), [thingx, thingy], random.randrange(10,100), 0)
    #pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def ship(x,y):
    gameDisplay.blit(shipImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',72)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2) #How long before a new game automatically starts.

    game_loop() #A new game automatically starts.

def crash():
    message_display('FAIL')
    
def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 35
    thing_width = random.randrange(10,100)
    thing_height = random.randrange(10,100)

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -15
                if event.key == pygame.K_RIGHT:
                    x_change = 15

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
		
        gameDisplay.blit(bg, (0,0))

        things(thing_startx, thing_starty, thing_width, thing_height, white)
        thing_starty += thing_speed
		
        ship(x,y)

        if x > display_width - ship_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
        
        if y < thing_starty+thing_height:
            print('y crossover')

            if x > thing_startx and x < thing_startx + thing_width or x+ship_width > thing_startx and x + ship_width < thing_startx+thing_width:
                print('x crossover')
                crash() #Collision detection.
        
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()