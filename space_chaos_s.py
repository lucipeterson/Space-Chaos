import pygame
from pygame.locals import *
import time
import random
from collections import deque
import os

pygame.init()

FPS = 60
ANIMATION_SPEED = 0.18

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
thingImg = pygame.image.load('asteroid.png')

ship_width = 73
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_icon(gameIcon)
clock = pygame.time.Clock()
pygame.display.set_caption('Space Chaos')

class things(pygame.sprite.Sprite):
    """Represents an obstacle.

    A PipePair has a top and a bottom pipe, and only between them can
    the bird pass -- if it collides with either part, the game is over.

    Attributes:
    x: The PipePair's X position.  This is a float, to make movement
        smoother.  Note that there is no y attribute, as it will only
        ever be 0.
    image: A pygame.Surface which can be blitted to the display surface
        to display the PipePair.
    mask: A bitmask which excludes all pixels in self.image with a
        transparency greater than 127.  This can be used for collision
        detection.
    top_pieces: The number of pieces, including the end piece, in the
        top pipe.
    bottom_pieces: The number of pieces, including the end piece, in
        the bottom pipe.

    Constants:
    WIDTH: The width, in pixels, of a pipe piece.  Because a pipe is
        only one piece wide, this is also the width of a PipePair's
        image.
    PIECE_HEIGHT: The height, in pixels, of a pipe piece.
    ADD_INTERVAL: The interval, in milliseconds, in between adding new
        pipes.
    """

    WIDTH = 80
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 3000

    def __init__(self, thingImg):
        """Initializes new random asteroid.

        It will automatically be assigned an x attribute of
        float(WIN_WIDTH - 200).

        Arguments:
        pipe_end_img: The image to use to represent a pipe's end piece.
        pipe_body_img: The image to use to represent one horizontal slice
            of a pipe's body.
        """
		
        self.x = float(WIN_HEIGHT - 200)
        self.score_counted = False
        self.image = pygame.Surface((PipePair.WIDTH, WIN_HEIGHT), SRCALPHA)
        self.image.convert()   
		
		# speeds up blitting
        self.image.fill((0, 0, 0, 0))

        # for collision detection
        self.mask = pygame.mask.from_surface(self.image)

    '''@property
    def top_height_px(self):
        """Get the top pipe's height, in pixels."""
        return self.top_pieces * PipePair.PIECE_HEIGHT

    @property
    def bottom_height_px(self):
        """Get the bottom pipe's height, in pixels."""
        return self.bottom_pieces * PipePair.PIECE_HEIGHT

    @property
    def visible(self):
        """Get whether this PipePair on screen, visible to the player."""
        return -PipePair.WIDTH < self.x < WIN_WIDTH

    @property
    def rect(self):
        """Get the Rect which contains this PipePair."""
        return Rect(self.x, 0, PipePair.WIDTH, PipePair.PIECE_HEIGHT)'''

    def update(self, delta_frames=1):
        """Update the asteroid's position.

        Arguments:
        delta_frames: The number of frames elapsed since this method was
            last called.
        """
        self.x -= ANIMATION_SPEED * frames_to_msec(delta_frames)

    def collides_with(self, ship):
        """Get whether the ship collides with an asteroid.
        """
        return pygame.sprite.collide_mask(self, ship)
		
def frames_to_msec(frames, fps=FPS):
    """Convert frames to milliseconds at the specified framerate.

    Arguments:
    frames: How many frames to convert to milliseconds.
    fps: The framerate to use for conversion.  Default: FPS.
    """
    return 1000.0 * frames / fps

class ship(pygame.sprite.Sprite):
    width = 73

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

        things(thing_startx, thing_starty)
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