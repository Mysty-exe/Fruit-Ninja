import pygame
import random
from helpers import add_decimal, sub_decimal

class Fruit:

    fruitNames = ["green pepper", "tomato", "tangerine", "lime", "potato", "apple", "yellow mango", "coconut", "pumpkin", "beet", "green apple", "orange", "mango", "pear", "lemon"]
    minSize, maxSize = 64, 128
    minSpawnX, maxSpawnX = 200, 800-64
    spawnY = 850
    minVelocityX, maxVelocityX = -2, 2
    minVelocityY, maxVelocityY = 18, 23

    def __init__(self, fruit):
        size = random.randrange(self.minSize, self.maxSize)
        self.fruit = pygame.image.load("Assets\\Fruits\\" + fruit + ".png").convert_alpha()
        self.fruit = pygame.transform.scale(self.fruit, (size, size))
        self.rect = self.fruit.get_rect()
        self.rect.x, self.rect.y = random.randrange(self.minSpawnX, self.maxSpawnX), self.spawnY
        self.mask = pygame.mask.from_surface(self.fruit)
        self.velocityX = random.randrange(self.minVelocityX, self.maxVelocityX)
        self.velocityY = random.randrange(self.minVelocityY, self.maxVelocityY)
        self.stayAtPeakTimer = 5
        self.gravity = 0.1

    def move(self):
        self.rect.x += self.velocityX
        self.rect.y -= self.velocityY

        self.gravity += 0.01    
        self.velocityY -= self.gravity

    def draw(self, surface):
        surface.blit(self.fruit, self.rect)

    def checkBoundary(self):
        if self.rect.y > 875:
            return True
        return False

    def slashed(self, pos, slicing):
        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y
        if slicing and self.rect.collidepoint(pos) and self.mask.get_at(pos_in_mask):
            return True
        return False
