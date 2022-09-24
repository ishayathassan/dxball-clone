import pygame
import sys


class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Paddle(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screen_width:
            self.rect.right = screen_width

    def update(self):
        self.rect.x += self.movement
        self.screen_constrain()


class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddle, brick):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.paddle = paddle
        self.brick = brick
        self.active = False

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.rect.x += paddle.movement
            if paddle.rect.left <= 0:
                self.rect.x = paddle.rect.x + 65
            if paddle.rect.right >= screen_width:
                self.rect.x = paddle.rect.x + 65

    def collisions(self):
        if self.rect.top <= 0:
            self.speed_y *= -1
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.speed_x *= -1
        if pygame.sprite.spritecollide(self, self.paddle, False):
            pygame.mixer.Sound.play(paddle_sound)
            collision_paddle = pygame.sprite.spritecollide(
                self, self.paddle, False)[0].rect
            if abs(self.rect.right - collision_paddle.left < 10):
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10:
                self.speed_x *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.speed_y *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.speed_y *= -1
        if pygame.sprite.spritecollide(self, self.brick, True):
            pygame.mixer.Sound.play(brick_sound)
            self.speed_y *= -1

    def reset_ball(self):
        self.active = False
        self.rect.center = (paddle.rect.x + 72.5, paddle.rect.y - 8)


class Brick(Block):
    def __init__(self, path, x_pos, y_pos):
        super().__init__(path, x_pos, y_pos)


class GameManager:
    def __init__(self, ball_sprite, paddle_sprite, brick_sprite, health):
        self.ball_sprite = ball_sprite
        self.paddle_sprite = paddle_sprite
        self.brick_sprite = brick_sprite
        self.health = health

    def run_game(self):
        # Drawing the game object
        self.paddle_sprite.draw(SCREEN)
        self.ball_sprite.draw(SCREEN)
        self.brick_sprite.draw(SCREEN)

        # Updating the game object
        self.paddle_sprite.update()
        self.ball_sprite.update()
        self.reset_ball()

    def reset_ball(self):
        if self.ball_sprite.sprite.rect.bottom >= screen_height:
            self.health -= 1
            self.ball_sprite.sprite.reset_ball()

    def game_over(self):
        over_text = basic_font.render("GAME OVER", True, (255, 255, 255))
        SCREEN.blit(over_text, (200, 300))


def brick_pattern(width, height, column, row, brick_group):
    xpos = width // 2
    ypos = height // 2

    for brick_ver in range(int(column)):
        new_brick = Brick("Brick.png", xpos, ypos)
        brick_group.add(new_brick)
        for brick_hor in range(int(row)):
            xpos += 40
            new_brick = Brick("Brick.png", xpos, ypos)
            brick_group.add(new_brick)
        xpos = 20
        ypos += 15
    return brick_group


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
bg_color = pygame.Color('grey12')
basic_font = pygame.font.Font('freesansbold.ttf', 64)
paddle_sound = pygame.mixer.Sound('paddle.wav')
brick_sound = pygame.mixer.Sound("brick.flac")
paddle_speed = 12
ball_speedX = -8
ball_speedY = -8
health = 3
vertical_bricks = 19
horizontal_bricks = 19
game_over = False

# Game Object

# Paddle
paddle = Paddle('Paddle.png', screen_width // 2,
                screen_height - 25, paddle_speed)
paddle_sprite = pygame.sprite.GroupSingle()
paddle_sprite.add(paddle)

# Brick
brick_group = pygame.sprite.Group()
brick_sprite = brick_pattern(
    40, 15, vertical_bricks, horizontal_bricks, brick_group)

# Ball
ball = Ball("Ball.png", paddle.rect.x + 72.5,
            paddle.rect.y - 8, ball_speedX, ball_speedY, paddle_sprite, brick_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)


game_manager = GameManager(ball_sprite, paddle_sprite, brick_sprite, health)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                paddle.movement -= paddle.speed
            if event.key == pygame.K_d:
                paddle.movement += paddle.speed

            # starting ball movement
            if event.key == pygame.K_SPACE:
                ball.active = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                paddle.movement += paddle.speed
            if event.key == pygame.K_d:
                paddle.movement -= paddle.speed

    # Background Stuff
    SCREEN.fill(bg_color)

    # Game logic
    if not game_over:
        game_manager.run_game()

    if game_manager.health <= 0 or len(brick_sprite) == 0:
        game_over = True
        game_manager.game_over()
    # Rendering
    pygame.display.flip()
    clock.tick(60)
