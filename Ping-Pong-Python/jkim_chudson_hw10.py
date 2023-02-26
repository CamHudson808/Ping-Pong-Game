"""
CS 145 - Assignment 10 - Breakout Game 
@authors: Cameron Hudson, Johnathan Kim
Due Date: 5/17/22

Added image as background and background music
Image: resort.jpg
Background Music: wii.wav
Added restart by pressing r key
Added message when all bricks are cleared

"""

from re import S
import pygame
import random
from asyncio.windows_events import NULL

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
SURFACE_BKG = (255, 255, 255)

GAME_FPS = 60

BALL_SPEED_MIN = -200
BALL_SPEED_MAX = 200
BALL_NUMBER = 1
BALL_SIZE = 10

TXT_COLOR = (255, 0, 0) 

class Ball:

    """
    A class representing a ball on the screen
    
    Attributes
    ----------
    surface : a pygame Surface 
        A pygame Surface type object from the module pygame
    radius : float
        The radius of the ball
    x : float
        The x coordinate of the ball
    y : float
        The y coordinate of the ball
    vx : float
        The x component of the velocity of the ball
    vy : float
        The y component of the velocity of the ball
    color : tuple
        The color of the ball as (red, green, blue)
    
    Methods
    -------
    update()
        Update the ball location and exploding status each time it is called
    collide(other)
        Check for collision with another ball
    swap_velocity(other)
        Bounce this ball off another ball
    draw()
        Draw the ball on the screen
    """

    def __init__(self, surface, radius, x, y, vx, vy, color):

        """
        Parameters
        ----------
        surface : a pygame Surface 
            A pygame Surface type object from the module pygame
        radius : float
            The radius of the ball
        x : float
            The x coordinate of the ball
        y : float
            The y coordinate of the ball
        vx : float
            The x component of the ball velocity
        vy : float
            The y component of the ball velocity
        color : tuple
            The color of the ball as (res, green, blue)
        """

        self.surface = surface
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
    
    def draw(self):

        """
        Draw the ball on the screen
        """
        self.rect = pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)

    def collided_with(self, other):

        """
        Check if this ball is colliding with another ball
        
        Parameters 
        ----------
        other : ball
            Another ball to be checked for collision
        """
        dx = self.x - other.x
        dy = self.y - other.y
        sr = self.radius + other.radius
        
        return (dx * dx + dy * dy) < sr * sr

    def swap_velocity(self, other):

        """
        Bounce this ball off another ball by swapping velocities
        
        Parameters
        ----------
        other : ball
            Another ball to bounce off
        """

        (temp_vx, temp_vy) = (self.vx, self.vy)
        (self.vx, self.vy) = (other.vx, other.vy)
        (other.vx, other.vy) = (temp_vx, temp_vy)

    def update(self, paddle, brick, visibles):
        """
        Update the ball status:
        - Check if the ball should bounce off the window edges
        - Update position using the velocity

        Parameters: paddle, bricks, visibles
        paddle: yellow bar at bottom of screen
        brick: black bricks at top of screen that ball collides with
        visibles: List of bricks with visible = True that have not been collided
        """

        self.paddle = paddle
        self.brick = brick
        self.visibles = visibles
        delta_t = 1/GAME_FPS 

        if (self.x - self.radius < 0) or (self.x + self.radius > DISPLAY_WIDTH):
            self.vx = -self.vx
        if (self.y - self.radius < 0):
            self.vy = -self.vy

        collide = pygame.Rect.colliderect(self.paddle, self.rect)

        if collide == True:
            self.vy = -self.vy

        for i in range(len(self.brick)):
            collide2 = pygame.Rect.colliderect(self.rect, self.brick[i].rect)

            if self.brick[i].visible == True and collide2 == True:
                if self.brick[i].rect.topleft[0] <= self.rect.midtop[0] <= self.brick[i].rect.topright[0]:
                    self.vy = -self.vy
                    self.brick[i].visible = False
                    self.visibles[i] = False

                if self.brick[i].rect.topleft[1] <= self.rect.midright[1] <= self.brick[i].rect.bottomleft[1]:
                    self.vx = -self.vx
                    self.brick[i].visible = False
                    self.visibles[i] = False

        self.x += self.vx * delta_t
        self.y += self.vy * delta_t

class Paddle:

    """
    A class representing a paddle on the screen
    
    Attributes
    ----------
    surface : a pygame Surface 
        A pygame Surface type object from the module pygame
    x : float
        The x coordinate of the paddle
    y : float
        The y coordinate of the paddle
    width : float
        width of paddle
    height : float
        height of paddle
    color : tuple
        The color of the paddle as (red, green, blue)
    
    Methods
    -------
    draw()
        Draw the paddle on the screen
    """

    def __init__(self, surface, x, y, width, height, color):
        """
        Parameters
        ----------
        surface : a pygame Surface 
            A pygame Surface type object from the module pygame
        x : float
            The x coordinate of the paddle
        y : float
            The y coordinate of the paddle
        width : float
            width of paddle
        height : float
            height of paddle
        color : tuple
            The color of the paddle as (red, green, blue)
        """

        self.surface = surface
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y

    def draw(self):
        rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect = pygame.draw.rect(self.surface, self.color, rectangle)

class Brick:

    """
    A class representing a brick on the screen
    
    Attributes
    ----------
    surface : a pygame Surface 
        A pygame Surface type object from the module pygame
    x : float
        The x coordinate of the brick
    y : float
        The y coordinate of the brick
    width : float
        width of brick
    height : float
        height of brick
    color : tuple
        The color of the brick as (red, green, blue)
    
    
    Methods
    -------
    draw()
        Draw the brick on the screen
    """
    
    def __init__(self, surface, x, y, width, height, color):
        """
         Parameters
        ----------
        surface : a pygame Surface 
            A pygame Surface type object from the module pygame
        x : float
            The x coordinate of the brick
        y : float
            The y coordinate of the brick
        width : float
            width of brick
        height : float
            height of brick
        color : tuple
            The color of the brick as (red, green, blue)
        """

        self.surface = surface
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y

        self.visible = True

    def draw(self):
        rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect = pygame.draw.rect(self.surface, self.color, rectangle)

class Game:
    """
    A class implementing the breakout game
    
    Attributes
    ----------
    surface : Surface
        A Surface type object from the module pygame
    clock : Clock
        A Clock type object from the module pygame
    bricks : list
        A list containing all the bricks objects
    
    Methods
    -------
    initialize_objects()
        Create the gamefield by adding the paddle, bricks, and ball
    run()
        Determines the game dynamic frame by frame (one frame for each call)
    """

    def __init__(self):

        """
        Initialize the scene
        """
        
        pygame.init()
       
        self.surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 50)
        self.initialize_objects()

    def initialize_objects(self):
        """
        Initialize all the objects in the scene
        """

        self.bricks = []
        self.visibles = []

        self.paddle = Paddle(self.surface, 370, 550, 90, 10, (255, 255, 0))

        x = random.randint(BALL_SIZE, DISPLAY_WIDTH - BALL_SIZE)
        y = random.randint(BALL_SIZE, DISPLAY_HEIGHT - BALL_SIZE)
                
        vx = random.randint(BALL_SPEED_MIN, BALL_SPEED_MAX)
        vy = random.randint(BALL_SPEED_MIN, BALL_SPEED_MAX)
       
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        color = (red, green, blue)

        self.ball = Ball(self.surface, 10, DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2, vx, -200, (0,0,0))
        
        brick_position_x = 0
        brick_position_y = 0

        while True:
            brick = Brick(self.surface, brick_position_x, brick_position_y, 80, 20, (0,0,0))
            self.bricks.append(brick)
            self.visibles.append(brick.visible)
            brick_position_x += 80
            if brick_position_x == 800:
                brick_position_y += 20
                brick_position_x = 0
            if brick_position_y == 80:
                break

    def run(self):
        """
        Determines the game dynamic frame by frame
        """
        window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        background_image = pygame.image.load("resort.jpg")
        background_image = pygame.transform.scale(background_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

        pygame.mixer.init()
        pygame.mixer.music.load('one_day.wav')
        pygame.mixer.music.play(-1)
        
        while True:
            i = 0
            window.blit(background_image, (i,0))
            i -= 1
            event = pygame.event.poll()  
            
            if event.type == pygame.QUIT:
                break
            if self.ball.y - self.ball.radius > DISPLAY_HEIGHT:
                break
            
            if event.type == pygame.KEYDOWN:     
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_r:
                    pygame.quit()
                    new_game = Game()
                    new_game.run()
                if event.key == pygame.K_LEFT:
                    p1.x -= 20
                if event.key == pygame.K_RIGHT:
                    p1.x += 20

            for i in range(len(self.bricks)):
                self.brick1 = self.bricks[i]
                if self.bricks[i].visible == True:
                    self.bricks[i].draw()

            if True not in self.visibles:
                text = self.font.render('You Won' , True, TXT_COLOR)
                self.surface.blit(text, (10, 0.95 * DISPLAY_HEIGHT))
                
            p1 = self.paddle
            p1.draw()
            
            b1 = self.ball
            b1.draw()
            b1.update(self.paddle.rect, self.bricks, self.visibles)

            pygame.display.update()
            self.clock.tick(GAME_FPS)
            

game = Game()
game.run()


