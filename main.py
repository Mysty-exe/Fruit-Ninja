# Imports modules needed
import pygame
import random
from fruits import Fruit
from game import Game

# Initializes Pygame
pygame.init()

# Game Object
game = Game("Fruit Slash", 1000, 600, 60)

running = True
while running:
    game.mouse_pos = pygame.mouse.get_pos() # Sets mouse position
    game.slashing = pygame.mouse.get_pressed()[0] # Checks if mouse button is being held (slashing)
    game.click = False
    events = pygame.event.get()

    # Event loop
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.click = True
        else:
            game.click = False

    # Checks game states
    if game.state == "Main Menu":
        game.main_menu(events)
    elif game.state == "Game":
        game.game(events)
    elif game.state == "Pause":
        game.game_pause(events)
    elif game.state == "Quit":
        running = False

    # Sets fps and updates screen
    game.clock.tick(game.fps)
    pygame.display.update()

pygame.quit()
