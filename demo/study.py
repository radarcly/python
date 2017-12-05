import sys
import pygame
from settings import Settings

def run_game():
    # init
    pygame.init()
    gameSetting = Settings()
    screen = pygame.display.set_mode(gameSetting.screen_width,gameSetting.screen_height)
    while True:
         for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
         #set color
         screen.fill(gameSetting.bg_color)
         #set screen show the latest
         pygame.display.flip()


run_game()