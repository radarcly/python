import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from alien import Alien
from game_status import GameStatus
from button import Button
from scoreboard import Scoreboard

def run_game():
    # init
    pygame.display.set_caption("Alien Invasion")
    pygame.init()
    gameSettings = Settings()
    # 创建一个用于存储游戏统计信息的实例
    status = GameStatus(gameSettings)
    screen = pygame.display.set_mode((gameSettings.screen_width,gameSettings.screen_height))
    sb = Scoreboard(gameSettings, screen, status)
    # create the ship
    ship = Ship(gameSettings,screen)
    # create a group to store bullet
    bullets = Group()
    # create an alien
    aliens = Group()
    gf.create_fleet(gameSettings,screen,aliens,ship)

    # 创建Play按钮
    play_button = Button(gameSettings, screen, "Play")
    while True:
        # check the event
        gf.check_events(gameSettings,screen,ship,bullets,status,play_button,aliens,sb)
        # update the ship and bullets
        if status.game_active:
            ship.update()
            gf.update_bullets(aliens,bullets,screen,ship,gameSettings,status,sb)
            gf.update_aliens(gameSettings,aliens,ship,status,screen,bullets,sb)
        #  update the screen
        gf.update_screen(gameSettings,screen,ship,bullets,aliens,status,play_button,sb)


run_game()