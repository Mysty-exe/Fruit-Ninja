import pygame
import random
from fruits import Fruit

WIDTH = 1000
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()

pygame.display.set_caption("Fruit Ninja")
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
display = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()

background = pygame.image.load("Assets\\background.jpeg").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT));
spawnRate = 2
fruitsInterval = 0
fruits = []
slashing = False;

running = True
while running:
    fruitsInterval -= (1 / FPS)

    screen.blit(display, (0, 0))
    display.fill(BLACK)
    display.blit(background, (0, 0))

    mouse_pos = pygame.mouse.get_pos()
    slashing = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if fruitsInterval <= 0:
        fruits.append(Fruit(random.choice(Fruit.fruitNames)))
        fruitsInterval = spawnRate

    for fruit in fruits:
        fruit.move()
        fruit.draw(display)
        if fruit.checkBoundary():
            fruits.remove(fruit)
        if fruit.slashed(mouse_pos, slashing):
            fruits.remove(fruit)
    
    clock.tick(FPS)
    pygame.display.update()       

pygame.quit()