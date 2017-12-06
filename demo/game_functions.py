import sys
import pygame
from bullet import Bullet

def check_events(gameSettings,screen,ship,bullets):
    """ response to  key and mouse event"""
    for event in pygame.event.get():
        #do not need argument because it copys events
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event,gameSettings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ship)



def check_key_down_events(event,gameSettings,screen,ship,bullets):
    """ respond to key down"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # 创建一颗子弹，并将其加入到编组bullets中
        fire_bullet(gameSettings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(gameSettings,screen,ship,bullets):
    if len(bullets) < gameSettings.bullets_allowed:
        new_bullet = Bullet(gameSettings, screen, ship)
        bullets.add(new_bullet)


def check_key_up_events(event,ship):
    """ respond to key up"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(gameSettings,screen,ship,bullets,alien):
    """update the new image and turn to the new screen"""
    # draw the screen
    screen.fill(gameSettings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    alien.blitme()
    # let the screen to see
    pygame.display.flip()

def update_bullets(bullets):
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)