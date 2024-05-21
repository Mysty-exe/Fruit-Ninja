import pygame
import random
import helpers

class Fruit:

    # Class Variables
    fruitNames = ["green pepper", "tomato", "tangerine", "lime", "potato", "apple", "yellow mango", "coconut", "pumpkin", "beet", "green apple", "orange", "mango", "pear", "lemon"]
    minSize, maxSize = 96, 112
    minSpawnX, maxSpawnX = 200, 800-64
    spawnY = 850
    minVelocityX, maxVelocityX = -2, 2
    minVelocityY, maxVelocityY = 18, 23
    minRotate, maxRotate = -4, 4
    explosion1 = []
    explosion2 = []
    explosion3 = []

    # Gets all the images for 3 different explosions
    for n in range(1, 4):
        for n2 in range(1, 11):
            try:
                frame = pygame.image.load(f"Assets\\Animations\\Explosion {n}\\{n2}.png")
                frame = pygame.transform.scale(frame, (128, 128))
                frame.set_colorkey((0, 0, 0))
                if n == 1:
                    explosion1.append(frame)
                elif n == 2:
                    explosion2.append(frame)
                else:
                    explosion3.append(frame)
            except:
                pass

    def __init__(self, fruit, inGame=True):
        self.size = random.randrange(self.minSize, self.maxSize)
        self.fruit = pygame.image.load("Assets\\Fruits\\" + fruit + ".png").convert_alpha()
        self.fruit = pygame.transform.scale(self.fruit, (self.size, self.size))
        self.inGame = inGame
        
        self.fruit_copy = self.fruit.copy()
        self.rect = self.fruit.get_rect()
        self.mask = pygame.mask.from_surface(self.fruit)
        
        # Checks if fruit is in the main menu or game
        if self.inGame:
            self.rect.x, self.rect.y = random.randrange(self.minSpawnX, self.maxSpawnX), self.spawnY
            self.velocityX = random.randrange(self.minVelocityX, self.maxVelocityX)
            self.velocityY = random.randrange(self.minVelocityY, self.maxVelocityY)
            self.gravity = 0.1
        else:
            self.rect.x, self.rect.y = random.randrange(50, 900), -100
            self.velocityX = random.randint(-2, 2)
            self.velocityY = 6
            self.gravity = 0

        self.rotateSpeed = random.randrange(self.minRotate, self.maxRotate)
        self.currentRotate = 0

        # Variables for explosion
        self.slashed = False
        self.explosion = random.randint(1, 3)
        self.frameTimer = 3
        self.currentExplodeFrame = 0
        self.exploded = False

    def draw(self, surface):
        # Draws fruit if it hasn't been slashed
        if not self.slashed:
            surface.blit(self.fruit, self.rect)

    def move(self):
        # Moves fruit if it hasn't been slashed
        if not self.slashed:
            self.rect.x += self.velocityX
            self.rect.y -= self.velocityY

            self.gravity += 0.01    
            self.velocityY -= self.gravity
            self.currentRotate += self.rotateSpeed
            self.rotate(self.currentRotate)

    def fall(self):
        # Function used in main menu where fruits fall from sky
        self.rect.x += self.velocityX
        self.rect.y += self.velocityY + self.gravity
        self.gravity += 0.5
        self.currentRotate += self.rotateSpeed
        self.rotate(self.currentRotate)

    def rotate(self, angle):
        # Rotates fruit
        self.fruit = helpers.rotate(self.fruit_copy, angle)

    def checkBoundary(self):
        # Checks if fruit has reached boundary
        if self.rect.y >= 875:
            return True
        return False

    def cut(self, pos, slicing):
        # Checks if player has sliced the fruit
        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y
        if slicing and self.rect.collidepoint(pos) and self.mask.get_at(pos_in_mask):
            self.slashed = True
            return True
        return False

    def explode(self, screen):            
        # Draws explosion of fruits on the screen
        middle = [self.rect.x + self.size / 2, self.rect.y + self.size / 2]
        if self.slashed:
            try:
                if self.explosion == 1:
                    screen.blit(self.explosion1[self.currentExplodeFrame], (middle[0] - 64, middle[1] - 64))
                if self.explosion == 2:
                    screen.blit(self.explosion1[self.currentExplodeFrame], (middle[0] - 64, middle[1] - 64))
                if self.explosion == 3:
                    screen.blit(self.explosion1[self.currentExplodeFrame], (middle[0] - 64, middle[1] - 64))

                if self.frameTimer > 0:
                    self.frameTimer -= 1
                else:
                    self.currentExplodeFrame += 1
                    self.frameTimer = 3
            except Exception:
                self.exploded = True
