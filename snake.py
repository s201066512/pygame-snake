import pygame
import random
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCALE = SCREEN_WIDTH/40
pygame.font.init()
game_font = pygame.font.SysFont('arial', 50)

from pygame.locals import (
    K_UP,
    K_LEFT,
    K_DOWN,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_r,
    KEYDOWN,
    QUIT
)
class Food:
    def __init__(self, apple: pygame.Surface):
        self.apple = apple
        
    def spawn(self):
        if type(self.apple) != pygame.Rect:
            self.apple = self.apple.get_rect()

        self.apple.x = random.randrange(SCALE, (int(SCREEN_WIDTH) - SCALE), SCALE)
        self.apple.y = random.randrange(SCALE, (int(SCREEN_HEIGHT) - SCALE), SCALE)

    def getX(self):
        return self.apple.x
    def getY(self):
        return self.apple.y
    
class Snake:
    def __init__(self, body: list[pygame.Rect] = [], direction: int = 0):
        self.body = body
        self.direction = direction
    def grow(self):
        square = pygame.Surface((SCALE, SCALE))
        square.fill((0, 255, 0))
        body_part = square.get_rect()
        if self.direction == 0:
            body_part.x = SCREEN_WIDTH/2
            body_part.y = SCREEN_HEIGHT/2
        else:
            prev_body_part = self.body[-1] if self.body else None
            body_part.x = prev_body_part.x + SCALE
            body_part.y = prev_body_part.y + SCALE

        self.body.append(body_part)

    def move(self):
        for i in range(len(self.body) -1, 0, -1):
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y
        if len(self.body) != 0:
            if self.direction == 1: # moving down
                self.body[0].y += SCALE
            elif self.direction == 2: # moving up
                self.body[0].y -= SCALE
            elif self.direction == 3: # moving left
                self.body[0].x -= SCALE
            elif self.direction == 4: # moving right
                self.body[0].x += SCALE
    
    def eat(self, apple: Food):
        if len(self.body) != 0:
            if self.body[0].x == apple.getX() and self.body[0].y == apple.getY():
                return True
            else:
                return False
        
    def game_over(self):
        # collding with own body
        if len(self.body) > 1:
            for i in range(len(self.body) - 1, 1, -1):
                if self.body[0].x == self.body[i].x and self.body[0].y == self.body[i].y: 
                    return True
        if len(self.body) != 0:
            # out of bounds/ hit wall check
            if self.body[0].x >= SCREEN_WIDTH or self.body[0].x <= 0:
                return True
            if self.body[0].y >= SCREEN_HEIGHT or self.body[0].y <= 0:
                return True

        
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

running = True
paused = False
score = 0
state = running
snake = Snake()
apple = pygame.Surface((SCALE, SCALE))
fruit = Food(apple)
fps = 12
def restart():
    global score
    score = 0
    del snake.body[:]
    snake.direction = 0
    state = running

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                pygame.quit()
            if event.key == pygame.QUIT:
                running = False
                pygame.quit()

            if event.key == K_SPACE:
                if state == paused:
                    state = running
                elif state == running:
                    state = paused

            if event.key == K_r: # restart
                restart()

            if event.key == K_DOWN and snake.direction != 2:
                snake.direction = 1
            if event.key == K_UP and snake.direction != 1:
                snake.direction = 2 
            if event.key == K_LEFT and snake.direction != 4:
                snake.direction = 3
            if event.key == K_RIGHT and snake.direction != 3:
                snake.direction = 4

    if state == running:

        if snake.direction == 0:
            snake.grow()
            fruit.spawn()
            snake.direction = -1

        if snake.eat(fruit):
            score = score + 1
            snake.grow()
            fruit.spawn()

        screen.fill((0, 0, 0))  # Clear the screen

        # Draw
        snake.move()
        for body_part in snake.body:
            pygame.draw.rect(screen, (0, 255, 0), body_part)  # Draw the snake

        pygame.draw.rect(screen, (255, 0, 0), fruit.apple) # Draw the fruit

        if snake.game_over():
            # restart_text = game_font.render("Press R to Respawn", True, (255, 255, 255))
            # screen.blit(restart_text, ((SCREEN_WIDTH/2), SCREEN_HEIGHT/2))
            restart()
            restart()

        score_text = ("Score: " + str(score))
        score_output = game_font.render(score_text, True, (255, 255, 255))
        screen.blit(score_output, ((SCREEN_WIDTH/10), SCALE))

        pygame.display.flip()
        clock.tick(fps)

pygame.quit()
