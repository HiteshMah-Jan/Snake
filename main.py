import random
import sys
import pygame

'''The Classic Snake Game'''

pygame.init()
pygame.display.init()
pygame.font.init()
comic = pygame.font.SysFont('Comic Sans MS' , 30)

size = 600, 600
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
screen = pygame.display.set_mode(size)
pygame.display.set_caption('The Snake Game')


class SnakeHead:
    def __init__(self):
        self.position = [300, 300]
        self.velocity = [20, 0]
        self.old_velocity = self.velocity.copy()
        self.rect = pygame.Rect(self.position, (20, 20))

    def update(self):
        self.old_position = self.position.copy()
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        self.position[0] = self.position[0] % 600
        self.position[1] = self.position[1] % 600

        self.rect = pygame.Rect(self.position, (20, 20))

#######################################################################


class SnakeBody:
    def __init__(self, parent):
        self.position = parent.position.copy()
        self.rect = pygame.Rect((-20, -20), (20, 20))

    def follow(self, parent):
        self.old_position = self.position.copy()
        self.position[0] = parent.old_position[0]
        self.position[1] = parent.old_position[1]
        self.rect = pygame.Rect(self.position, (20, 20))

########################################################################


class Food:
    def __init__(self):
        self.x = random.randint(1, 29) * 20
        self.y = random.randint(1, 29) * 20
        self.rect = pygame.Rect((self.x, self.y), (5, 5))

#######################################################################


snake = [SnakeHead()]
food = Food()
scr = 0
score = comic.render('Score = '+ str(scr), False, (250,250,250))
screen.blit(score,(0,0))


while True:
    snake[0].update()
    for i in range(1, len(snake)):
        snake[i].follow(snake[i-1])

    if pygame.Rect.collidepoint(snake[0].rect, food.x-10, food.y-10):
        scr += 1
        score = comic.render('Score = ' + str(scr), False, (255, 255, 255))
        #print(scr)
        food = Food()
        snake.append(SnakeBody(snake[len(snake)-1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        snake = [SnakeHead()]
    if keys[pygame.K_RIGHT] and snake[0].velocity != [-20, 0]:
        snake[0].velocity = [20, 0]
    if keys[pygame.K_LEFT] and snake[0].velocity != [20, 0]:
        snake[0].velocity = [-20, 0]
    if keys[pygame.K_UP] and snake[0].velocity != [0, 20]:
        snake[0].velocity = [0, -20]
    if keys[pygame.K_DOWN] and snake[0].velocity != [0, -20]:
        snake[0].velocity = [0, 20]

    for i in range(1, len(snake)):
        if pygame.Rect.colliderect(snake[0].rect, snake[i].rect):
            print('You Lose!')
            pygame.quit()
            sys.exit()

    screen.fill(black)
    for snk in snake:
        pygame.draw.rect(screen, white, snk.rect)
    pygame.draw.circle(screen, red, [food.x-10, food.y-10], 10)

    screen.blit(score, (0, 0))
    pygame.display.flip()
    pygame.time.delay(125)
