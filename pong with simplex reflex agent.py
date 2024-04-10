import pygame
import  random
pygame.init()

WINNING_SCORE = 5
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
FPS = 60
BLACK = (0, 0, 0)
YELLOW = (0, 255, 255)
WHITE = (255, 255, 255)
PADDLE_W, PADDLE_H = 30, 135
BALL_RADIUS = 10
RED = (255, 0, 0)
SCORE_FONT = pygame.font.SysFont("comicsans", 50)


class Paddle:
    COLOR = WHITE

    def __init__(self, x, y, width, height,vel):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.vel =  vel
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self,vel,up=True):
        if up:
            self.y -= self.vel 
        else:
            self.y += self.vel 

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    COLOR = RED
    MAX_VEL = 8

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"PLayer:{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"AI:{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))
    for paddle in paddles:
        paddle.draw(win)
    for i in range(20, HEIGHT, HEIGHT // 10):
        if i % 4 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))
    ball.draw(win)
    pygame.display.update()


def handle_collision(ball, pad1, pad2):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= pad1.y and ball.y <= pad1.y + pad1.height:
            if ball.x - ball.radius <= pad1.x + pad1.width:
                ball.x_vel *= -1

                middle_y = pad1.y + (pad1.height / 2)
                diff_y = middle_y - ball.y
                reduction_factor = (pad1.height / 2) / ball.MAX_VEL
                y_vel = diff_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= pad2.y and ball.y <= pad2.y + pad2.height:
            if ball.x + ball.radius >= pad2.x:
                ball.x_vel *= -1

                middle_y = pad2.y + (pad2.height / 2)
                diff_y = middle_y - ball.y
                reduction_factor = (pad2.height / 2) / ball.MAX_VEL
                y_vel = diff_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_pad_move(keys, pad1, pad2):
    if keys[pygame.K_w] and pad1.y - pad1.vel >= 0:
        pad1.move(10,up=True)
    if keys[pygame.K_s] and pad1.y + pad1.height + pad1.vel <= HEIGHT:
        pad1.move(10,up=False)


def simple_ai(ball, paddle):
    num = random.random()
    if ball.x_vel > 0:
        if ball.y < paddle.y + num*(paddle.height)and paddle.y - paddle.vel >= 0:
            paddle.move(10,up=True)
        elif ball.y > paddle.y + num*(paddle.height) and paddle.y + paddle.height + paddle.vel <= HEIGHT:
            paddle.move(10,up=False)


def main():
    run = True
    clock = pygame.time.Clock()
    pad1 = Paddle(10, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H,10)
    pad2 = Paddle(WIDTH - 10 - PADDLE_W, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H,7.5)
    ball1 = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    left_score = 0
    right_score = 0
    while run:
        clock.tick(FPS)
        draw(WIN, [pad1, pad2], ball1, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_pad_move(keys, pad1, pad2)
        simple_ai(ball1, pad2)
        ball1.move()
        handle_collision(ball1, pad1, pad2)

        if ball1.x < 0:
            right_score += 1
            ball1.reset()
        elif ball1.x > WIDTH:
            left_score += 1
            ball1.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            wintext = "Left Player Won"
        elif right_score >= WINNING_SCORE:
            won = True
            wintext = "AI Player Won"
        if won:
            text = SCORE_FONT.render(wintext, 1, YELLOW)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball1.reset()
            pad1.reset()
            pad2.reset()
            left_score = 0
            right_score = 0
    pygame.quit()


if __name__ == '__main__':
    main()
