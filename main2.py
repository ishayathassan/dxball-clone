import pygame
import sys


# General Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()


# Main Window
screen_width = 800
screen_height = 700
SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("dxball")

# Global Variables
VEL = 10
RADIUS = 14


# Color Codes
LIGHT_GREY = (200, 200, 200)
GREY = pygame.Color('grey12')
BLACK = (255, 255, 255)
WHITE = pygame.Color('white')


# Rectangles
PADDLE = pygame.Rect(screen_width // 2 - 70, screen_height - 25, 140, 10)

BALL_WIDTH = PADDLE.x + 63
BALL = pygame.Rect(BALL_WIDTH, PADDLE.y - RADIUS, RADIUS, RADIUS)

move = False

# Speed
paddle_speed = 0
ball_speed_x = -7
ball_speed_y = -7


def paddle_animation():
    PADDLE.x += paddle_speed

    if PADDLE.left <= 0:
        PADDLE.left = 0

    if PADDLE.right >= screen_width:
        PADDLE.right = screen_width


def ball_animation():
    global ball_speed_x, ball_speed_y

    if move:  # Ball starts moving if true
        BALL.x += ball_speed_x
        BALL.y += ball_speed_y

        if BALL.top <= 0:
            ball_speed_y *= -1
        if BALL.left <= 0 or BALL.right >= screen_width:
            ball_speed_x *= -1

        if BALL.colliderect(PADDLE):
            if abs(BALL.right - PADDLE.left < 10):
                ball_speed_x *= -1
            elif abs(BALL.bottom - PADDLE.top) < 10 and ball_speed_y > 0:
                ball_speed_y *= -1
            elif abs(BALL.top - PADDLE.bottom) < 10 and ball_speed_y < 0:
                ball_speed_y *= -1

    if not move:  # ball moves with paddle
        BALL.x += paddle_speed
        if PADDLE.left <= 0:
            BALL.x = PADDLE.x + 63
        if PADDLE.right >= screen_width:
            BALL.x = PADDLE.x + 63


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                paddle_speed -= VEL
            if event.key == pygame.K_d:
                paddle_speed += VEL

            # starting ball movement
            if event.key == pygame.K_SPACE:
                move = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                paddle_speed += VEL
            if event.key == pygame.K_d:
                paddle_speed -= VEL

    paddle_animation()
    ball_animation()

    # Visuals
    SCREEN.fill(GREY)
    pygame.draw.rect(SCREEN, LIGHT_GREY, PADDLE)
    pygame.draw.ellipse(SCREEN, LIGHT_GREY, BALL)

    pygame.display.flip()
    clock.tick(60)
