import pygame
import random
from fruits import Fruit
from bomb import Bomb

class Game:
    def __init__(self, name, width, height, fps):
        self.name = name
        self.width = width
        self.height = height
        self.fps = fps

        # Initializing game and screen
        self.icon = pygame.image.load(f"Assets\\Fruits\\{random.choice(Fruit.fruitNames)}.png")
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(self.name)
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        self.display = pygame.Surface((self.width, self.height))
        self.pauseDisplayCopy = self.display.copy()
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        self.screenshake = 0
        self.slashing = False
        self.click = False

        # Other game variables
        self.state = "Main Menu"
        self.scoreImg = pygame.image.load(f"Assets\\Fruits\\{random.choice(Fruit.fruitNames)}.png").convert_alpha()
        self.scoreImg = pygame.transform.scale(self.scoreImg, (48, 48))
        self.startTimer = 60
        self.score = 0
        self.chances = 3

        self.spawnRate = 120
        self.fruitsInterval = self.spawnRate
        self.bombChance = 10
        self.fruitsIntervalMain = 0
        self.increaseDifficulty = 60 * 20
        self.difficulty = 1
        
        self.objects = []
        self.fruitsMain = [ ]
        self.slashSegments = []
        self.slashParticles = []
        self.slashColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.last_mouse_pos = None
        self.mouse_pos = []

        self.hitBomb = False
        self.gameOver = False

        self.combos = []
        self.slashMoving = False
        self.combo = 0

        # Background
        self.bg = pygame.image.load("Assets\\bg.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))

        # Pause Background
        self.white_bg = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.white_bg.fill((255, 255, 255, 150))
        self.pause_hovering = False

        # Cursor
        self.cursor = pygame.image.load("Assets\\cursor.png").convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (48, 48))
        self.cursor_rect = self.cursor.get_rect()

        # Sound
        self.btn_click = pygame.mixer.Sound("Assets\\Sounds\\Button Click.wav")
        self.slash_effect = pygame.mixer.Sound("Assets\\Sounds\\slash.mp3")
        self.fall_effect = pygame.mixer.Sound("Assets\\Sounds\\fall.mp3")
        self.explosion = pygame.mixer.Sound("Assets\\Sounds\\explosion.mp3")

        # Fonts
        self.bigFontObj = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 112)
        self.fontObj = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 48)
        self.fontCombo = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 12)

        # Texts
        self.title_text = self.bigFontObj.render(self.name, True, (0, 0, 0))
        self.title_text_rect = self.title_text.get_rect()

        self.pause_text = self.bigFontObj.render("Game Paused", True, (0, 0, 0))
        self.pause_text_rect = self.pause_text.get_rect()

        self.play_text = self.bigFontObj.render("Play", True, (0, 0, 0))
        self.play_text_hover = self.bigFontObj.render("Play", True, (255, 255, 255))
        self.play_text_rect = self.play_text.get_rect()

        self.leave_text = self.bigFontObj.render("Leave", True, (0, 0, 0))
        self.leave_text_hover = self.bigFontObj.render("Leave", True, (255, 255, 255))
        self.leave_text_rect = self.leave_text.get_rect()

        self.quit_text = self.bigFontObj.render("Quit", True, (0, 0, 0))
        self.quit_text_hover = self.bigFontObj.render("Quit", True, (255, 255 ,255))
        self.quit_text_rect = self.quit_text.get_rect()

        self.game_over_text = self.bigFontObj.render("Game Over", True, (0, 0, 0))
        self.game_over_text_rect = self.game_over_text.get_rect()

        self.press_esc_text = self.fontObj.render("Press ESCAPE to go to Main Menu", True, (0, 0, 0))
        self.press_esc_text_rect = self.press_esc_text.get_rect()

        self.score_text = self.fontObj.render('0', True, (0, 0, 0))
        self.score_text_rect = self.score_text.get_rect()

        self.end_score_text = self.fontObj.render("Score: 0", True, (0, 0, 0))
        self.end_score_text_rect = self.end_score_text.get_rect()

        self.combo2txt = self.fontObj.render("2x Combo!", True, (255, 255, 0))
        
        # Pause Button
        self.pause = pygame.image.load("Assets\\Buttons\\pauseButton.png")
        self.pause = pygame.transform.scale(self.pause, (48, 48))
        self.pause_rect = self.pause.get_rect()
        self.pause_rect.x, self.pause_rect.y = 937, 15

        # Pause Button when hovering
        self.pause_hover = pygame.image.load("Assets\\Buttons\\pauseButtonHover.png")
        self.pause_hover = pygame.transform.scale(self.pause_hover, (48, 48))
        self.pause_hover_rect = self.pause_hover.get_rect()
        self.pause_hover_rect.x, self.pause_hover_rect.y = 937, 15

        # X's
        self.emptyX = pygame.image.load("Assets\\emptyX.png")
        self.emptyX = pygame.transform.scale(self.emptyX, (48, 48))
        self.filledX = pygame.image.load("Assets\\filledX.png")
        self.filledX = pygame.transform.scale(self.filledX, (48, 48))

    def reset(self):
        # Resets game
        self.startTimer = 60
        self.score = 0
        self.chances = 3
        self.fruitsInterval = self.spawnRate
        self.screenshake = 0
        self.objects = []
        self.last_mouse_pos = None
        self.slashParticles = []
        self.slashSegments = []
        self.slashColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.hitBomb = False
        self.gameOver = False
        self.difficulty = 1

    def main_menu(self, events):
        pygame.mouse.set_visible(True)
        
        # Draws screen
        self.screen.blit(self.display, (0, 0))
        self.display.fill((0, 0, 0))
        self.display.blit(self.bg, (0, 0))

        # Adds a fruit after interval
        if self.fruitsIntervalMain > 0:
            self.fruitsIntervalMain -= 1
        else:
            self.fruitsMain.append(Fruit(random.choice(Fruit.fruitNames), inGame=False))
            self.fruitsIntervalMain = 30

        # Loops through fruits and draws them
        for fruit in self.fruitsMain:
            fruit.draw(self.display)
            fruit.fall()
            if fruit.checkBoundary():
                self.fruitsMain.remove(fruit)

        # Draws title and buttons
        self.title_text_rect.x, self.title_text_rect.y = 500 - self.title_text.get_width() / 2, 100
        self.display.blit(self.title_text, self.title_text_rect)

        self.play_text_rect.x, self.play_text_rect.y = 500 - self.play_text.get_width() / 2, 275
        self.quit_text_rect.x, self.quit_text_rect.y = 500 - self.quit_text.get_width() / 2, 400

        if self.play_text_rect.collidepoint(self.mouse_pos):
            self.screen.blit(self.play_text_hover, self.play_text_rect)
            if self.click:
                self.btn_click.play()
                self.reset()
                self.state = "Game"
        else:
            self.screen.blit(self.play_text, self.play_text_rect)
        
        if self.quit_text_rect.collidepoint(self.mouse_pos):
            self.screen.blit(self.quit_text_hover, self.quit_text_rect)
            if self.click:
                self.btn_click.play()
                self.state = "Quit"
        else:
            self.screen.blit(self.quit_text, self.quit_text_rect)

    def game_pause(self, events):
        pygame.mouse.set_visible(True)

        # Event loop
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.btn_click.play()
                    self.state = "Game"

        # Draws screen
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.pauseDisplayCopy, (0, 0))
        self.screen.blit(self.white_bg, (0, 0))
        
        # Draws Pause text and buttons
        self.pause_text_rect.x, self.pause_text_rect.y = 500 - self.pause_text.get_width() / 2, 125
        self.screen.blit(self.pause_text, self.pause_text_rect)
        
        self.play_text_rect.x, self.play_text_rect.y = 500 - self.play_text.get_width() / 2, 300
        self.leave_text_rect.x, self.leave_text_rect.y = 500 - self.leave_text.get_width() / 2, 400

        if self.play_text_rect.collidepoint(self.mouse_pos):
            self.screen.blit(self.play_text_hover, self.play_text_rect)
            if self.click:
                self.btn_click.play()
                self.state = "Game"
        else:
            self.screen.blit(self.play_text, self.play_text_rect)
        
        if self.leave_text_rect.collidepoint(self.mouse_pos):
            self.screen.blit(self.leave_text_hover, self.leave_text_rect)
            if self.click:
                self.btn_click.play()
                self.state = "Main Menu"
        else:
            self.screen.blit(self.leave_text, self.leave_text_rect)

    def game_ui(self):
        # Draws score image and actual score
        self.display.blit(self.scoreImg, (15, 15))
        
        self.score_text = self.fontObj.render(str(self.score), True, (240,240,240))
        self.score_text_rect.x, self.score_text_rect.y = 70, 17
        self.display.blit(self.score_text, self.score_text_rect)
        self.drawChances() # Draws X's

        # Draws pause button
        if self.pause_rect.collidepoint(self.mouse_pos):
            self.pause_hovering = True
            self.display.blit(self.pause_hover, self.pause_hover_rect)
            if self.click:
                self.btn_click.play()
                self.state = "Pause"
        else:
            self.pause_hovering = False
            self.display.blit(self.pause, self.pause_rect)

    def game(self, events):
        pygame.mouse.set_visible(False)
        
        # Event Loop
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not self.gameOver:
                        self.btn_click.play()
                        self.state = "Pause"
                    else:
                        self.explosion.stop()
                        self.btn_click.play()
                        self.state = "Main Menu"

        # Displays screen
        renderOffset = (0, 0)
        if self.screenshake > 0:
            self.screenshake -= 1
            renderOffset = (random.randint(0, 12) - 6, random.randint(0, 12) - 6)

        self.screen.blit(self.display, renderOffset)
        self.display.fill((0, 0, 0))
        self.display.blit(self.bg, (0, 0))
        
        self.game_ui()

        # Increases Difficulty
        if self.increaseDifficulty > 0:
            self.increaseDifficulty -= 1
        else:
            self.increaseDifficulty = 60 * 20
            self.difficulty += 1
            if self.spawnRate > 10:
                self.spawnRate -= 5
            if self.bombChance < 40:
                self.bombChance + 2

        for combo in self.combos:
            if combo[2] > 0:
                combo[2] -= 1
                self.display.blit(combo[0], combo[1])
            else:
                self.combos.remove(combo)

        if not self.gameOver:
            # Displays cursor
            if not self.slashing:
                self.cursor_rect = self.mouse_pos
                self.display.blit(self.cursor, self.cursor_rect)
    
            if self.slashing:
                # Adds slash fragment
                if self.last_mouse_pos != None:
                    self.slashSegments.append([self.last_mouse_pos, self.mouse_pos, 5])
                
                # Adds slash particle
                if self.last_mouse_pos != self.mouse_pos:
                    self.slashMoving = True
                    for _ in range(5):
                        self.slashParticles.append([[self.mouse_pos[0], self.mouse_pos[1]], [random.randint(-6, 3) / 10, -0.5], random.randint(16, 20)])
                else:
                    self.slashMoving = False
                    self.combo = 0

            # Displays segments
            for segment in self.slashSegments:    
                segment[2] -= 1
                pygame.draw.line(self.display, (255, 255, 255), segment[0], segment[1], 10)
                if segment[2] <= 0:
                    self.slashSegments.remove(segment)
            
            # Displays particles
            for particle in self.slashParticles:
                particle[0][0] -= particle[1][0]
                particle[0][1] -= particle[1][1]
                particle[2] -= 0.3
                pygame.draw.rect(self.display, self.slashColor, [int(particle[0][0]), int(particle[0][1]), int(particle[2]), int(particle[2])])
                if particle[2] <= 0:
                    self.slashParticles.remove(particle)
        
        self.last_mouse_pos = self.mouse_pos

        if self.startTimer > 0:
            self.startTimer -= 1
        else:
            if self.fruitsInterval <= 0 and not self.gameOver:
                self.objects.append(random.choices([Fruit(random.choice(Fruit.fruitNames)), Bomb()], [100 - self.bombChance, self.bombChance])[0])
                self.fruitsInterval = self.spawnRate
            elif self.fruitsInterval > 0:
                self.fruitsInterval -= 1

            # Loops through objecst
            for obj in self.objects:
                obj.move()
                obj.draw(self.display)

                # Checks if object reached boundary
                if obj.checkBoundary(): 
                    self.objects.remove(obj)
                    if type(obj) is Fruit:
                        self.screenshake += 30
                        self.chances -= 1
                        self.fall_effect.play()

                # Checks if object has just been cut
                if not obj.slashed and obj.cut(self.mouse_pos, self.slashing) and not self.gameOver:
                    if type(obj) is Fruit:
                        self.slash_effect.play()
                        self.score += 1
                        if self.slashMoving:
                            # Checks for combos
                            self.combo += 1
                            if self.combo > 1:
                                self.score += self.combo
                            if self.combo == 2:
                                self.combos.append([self.combo2txt, (obj.rect.x, obj.rect.y), 60])
                            elif self.combo == 3 or self.combo == 4:
                                combotxt = self.fontObj.render(f"{self.combo}x Combo!", True, (255, 99, 71))
                                self.combos.append([combotxt, (obj.rect.x, obj.rect.y), 60])
                            elif self.combo > 4:
                                combotxt = self.fontObj.render("5x Combo!", True, (194, 24, 7))
                                self.combos.append([combotxt, (obj.rect.x, obj.rect.y), 60])
                    else:
                        self.screenshake += 60

                # Explodes object
                obj.explode(self.display)
                if type(obj) is Fruit:
                    if obj.exploded:
                        self.objects.remove(obj)
                else:
                    # Combusts bomb
                    if obj.combusting:
                        self.gameOver = True
                        self.explosion.play()
                    obj.combust(self.display)
                    if obj.done:
                        self.objects.remove(obj)
                        self.hitBomb = True

        if (self.hitBomb or self.chances <= 0) and not self.gameOver:
            self.gameOver = True
            if self.chances <= 0:
                self.screenshake += 60
                self.drawChances()

        if self.gameOver:
            self.game_over(events)

        self.pauseDisplayCopy = self.display.copy()

    def game_over(self, events):
        # Draws screen
        self.display.blit(self.white_bg, (0, 0))
        
        # Draws Final Score and game over text
        self.end_score_text = self.fontObj.render("Final Score: " + str(self.score), True, (0, 0, 0))
        self.game_over_text_rect.x, self.game_over_text_rect.y = 500 - self.game_over_text.get_width() / 2, 125
        self.end_score_text_rect.x, self.end_score_text_rect.y = 500 - self.end_score_text.get_width() / 2, 300
        self.press_esc_text_rect.x, self.press_esc_text_rect.y = 500 - self.press_esc_text.get_width() / 2, 400

        self.display.blit(self.game_over_text, self.game_over_text_rect)
        self.display.blit(self.end_score_text, self.end_score_text_rect)
        self.display.blit(self.press_esc_text, self.press_esc_text_rect)

        self.cursor_rect = self.mouse_pos
        self.display.blit(self.cursor, self.cursor_rect)

    def drawChances(self):
        # Draws X's depending on how many chances the user has
        for num in range(3):
            if (num == 0 and self.chances >= 3) or (num == 1 and self.chances >= 2) or (num == 2 and self.chances >= 1):
                self.display.blit(self.emptyX, (420 + 60 * num, 15))
            else:
                self.display.blit(self.filledX, (420 + 60 * num, 15))
