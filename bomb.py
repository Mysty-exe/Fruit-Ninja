# Initializes modules needed
import pygame
import random
import helpers

class Bomb:

    # Class Variables
    size = 96
    minSpawnX, maxSpawnX = 200, 800-64
    spawnY = 850
    minVelocityX, maxVelocityX = -2, 2
    minVelocityY, maxVelocityY = 18, 23
    minRotate, maxRotate = -4, 4

    # Gets images of bomb explosion and combustion
    bombExplosions = []
    bombCombustions = []
    for n in range(2, 9):
        frame = pygame.image.load(f"Assets\\Animations\\Bomb\\Explode\\{n}.png")
        frame = pygame.transform.scale(frame, (100, 100))
        bombExplosions.append(frame)

    for n in range(1, 27):
        frame = pygame.image.load(f"Assets\\Animations\\Bomb\\Combust\\{n}.png")
        frame = pygame.transform.scale(frame, (800, 800))
        bombCombustions.append(frame)

    def __init__(self):
        self.bomb = pygame.image.load("Assets\\Animations\\Bomb\\Explode\\1.png")
        self.bomb = pygame.transform.scale(self.bomb, (self.size, self.size))
        self.bomb_copy = self.bomb.copy()
        self.rect = self.bomb.get_rect()
        self.mask = pygame.mask.from_surface(self.bomb)
        self.rect.x, self.rect.y = random.randrange(self.minSpawnX, self.maxSpawnX), self.spawnY
        
        self.velocityX = random.randrange(self.minVelocityX, self.maxVelocityX)
        self.velocityY = random.randrange(self.minVelocityY, self.maxVelocityY)
        self.gravity = 0.1

        self.rotateSpeed = random.randrange(self.minRotate, self.maxRotate)
        self.currentRotate = 0

        self.slashed = False

        # Explosion and Combustion variables
        self.frameTimer = 1
        self.currentExplodeFrame = 3
        self.combusting = False
        self.done = False

    def draw(self, surface):
        # Draws bomb if it hasn't been slashed
        if not self.slashed:
            surface.blit(self.bomb, self.rect)

    def move(self):
        # Moves bomb if it hasn't been slashed
        if not self.slashed:
            self.rect.x += self.velocityX
            self.rect.y -= self.velocityY

            self.gravity += 0.01    
            self.velocityY -= self.gravity
            self.currentRotate += self.rotateSpeed
            self.rotate(self.currentRotate)

    def rotate(self, angle):
        # Rotates bomb
        self.bomb = helpers.rotate(self.bomb_copy, angle)

    def checkBoundary(self):
        # Checks if bomb reached boundary
        if self.rect.y > 875:
            return True
        return False

    def cut(self, pos, slicing):
        # Checks if bomb has been slashed
        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y
        if slicing and self.rect.collidepoint(pos) and self.mask.get_at(pos_in_mask):
            self.slashed = True
            return True
        return False

    def explode(self, screen):      
        # Starts bomb explosion animation      
        if self.slashed and not self.combusting:
            screen.blit(helpers.rotate(self.bombExplosions[self.currentExplodeFrame], self.currentRotate), self.rect)
            if self.frameTimer > 0:
                self.frameTimer -= 1
            else:
                self.frameTimer = 3
                self.currentExplodeFrame += 1
                if self.currentExplodeFrame >= 7:
                    self.currentExplodeFrame = 0
                    self.combusting = True

    def combust(self, screen):
        # Starts bomb combustion animation
        middle = [self.rect.x + self.size / 2, self.rect.y + self.size / 2]
        if self.combusting:
            screen.blit(self.bombCombustions[self.currentExplodeFrame], (middle[0] - 400, middle[1] - 400))
            if self.frameTimer > 0:
                self.frameTimer -= 1
            else:
                self.frameTimer = 1
                self.currentExplodeFrame += 1
                if self.currentExplodeFrame >= 25:
                    self.done = True
