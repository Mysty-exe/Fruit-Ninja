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

fontObj = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 48)
score_text = fontObj.render('0', True, (240,240,240))
score_text_rect = score_text.get_rect()

icon = pygame.image.load("Assets\\Fruits\\green apple.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Fruit Ninja")
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
display = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

cursor = pygame.image.load("Assets\\cursor.png").convert_alpha()
cursor = pygame.transform.scale(cursor, (48, 48))
cursor_rect = cursor.get_rect()
background = pygame.image.load("Assets\\background.jpeg").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

state = "Game"
scoreImg = pygame.image.load("Assets\\Fruits\\mango.png").convert_alpha()
scoreImg = pygame.transform.scale(scoreImg, (48, 48))
score = 0
chances = 3
spawnRate = 2
fruitsInterval = 0
fruits = []
slashing = False;

slashParticles = []

def game_ui():
    display.blit(scoreImg, (15, 15))
    score_text_rect.x, score_text_rect.y = 70, 17
    display.blit(score_text, score_text_rect)

def main_game(gameScore, gameChances, interval):
    game_ui()

    if not slashing:
        cursor_rect.center = mouse_pos
        display.blit(cursor, cursor_rect)

    if slashing:
        for _ in range(15):
            slashParticles.append([[mouse_pos[0], mouse_pos[1]], [random.randint(-6, 3) / 10, -0.3], random.randint(16, 20)])
    
    for particle in slashParticles:
        particle[0][0] -= particle[1][0]
        particle[0][1] -= particle[1][1]
        particle[2] -= 0.3
        pygame.draw.rect(display, (208, 254, 254), [int(particle[0][0]), int(particle[0][1]), int(particle[2]), int(particle[2])])
        if particle[2] <= 0:
            slashParticles.remove(particle)

    if interval <= 0:
        fruits.append(Fruit(random.choice(Fruit.fruitNames)))
        interval = spawnRate

    for fruit in fruits:
        fruit.move()
        fruit.draw(display)
        if fruit.checkBoundary():
            fruits.remove(fruit)
            gameChances -= 1
        if fruit.slashed(mouse_pos, slashing):
            fruits.remove(fruit)  
            gameScore += 1

    return gameScore, gameChances, interval

running = True
while running:
    screen.blit(display, (0, 0))
    display.fill(BLACK)
    display.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    slashing = pygame.mouse.get_pressed()[0]

    if state == "Game":
        fruitsInterval -= (1 / FPS)
        score, chances, fruitsInterval = main_game(score, chances, fruitsInterval)
        score_text = fontObj.render(str(score), True, (240,240,240))
    
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
