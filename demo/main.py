import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from alien import Alien

def run_game():
    # init
    pygame.display.set_caption("Alien Invasion")
    pygame.init()
    gameSettings = Settings()
    screen = pygame.display.set_mode((gameSettings.screen_width,gameSettings.screen_height))
    # create the ship
    ship = Ship(gameSettings,screen)
    # create a group to store bullet
    bullets = Group()
    # create an alien
    aliens = Group()

    gf.create_fleet(gameSettings,screen,aliens,ship)
    while True:
        # check the event
        gf.check_events(gameSettings,screen,ship,bullets)
        # update the ship and bullets
        ship.update()
        gf.update_bullets(aliens,bullets,screen,ship,gameSettings)
        gf.update_aliens(gameSettings,aliens)
        # update the screen
        gf.update_screen(gameSettings,screen,ship,bullets,aliens)


run_game()