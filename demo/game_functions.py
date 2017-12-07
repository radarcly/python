import sys
import pygame
from bullet import Bullet
from alien import  Alien

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


def update_screen(gameSettings,screen,ship,bullets,aliens):
    """update the new image and turn to the new screen"""
    # draw the screen
    screen.fill(gameSettings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    #for alien in aliens.sprites():
        #print (alien.rect.y)
    ship.blitme()
    #print (aliens)
    aliens.draw(screen)
    # let the screen to see
    pygame.display.flip()

def update_bullets(aliens,bullets,screen,ship,gameSettings):
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 两个实参True告诉Pygame删除发生碰撞的子弹和外星人。（要模拟能够穿行到屏幕顶端的高能子弹——消灭它击中的每个外星人，
    # 可将第一个布尔实参设置为False，并让第二个布尔实参为True。这样
    # 被击中的外星人将消失，但所有的子弹都始终有效，直到抵达屏幕顶端后消失。）
    collisions = pygame.sprite.groupcollide(bullets, aliens, True,True)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        create_fleet(gameSettings, screen, aliens,ship)



def create_fleet(gameSettings,screen,aliens,ship):
    """ create aliens"""
    alien = Alien(gameSettings, screen)
    number_aliens_x = get_number_aliens_x(gameSettings, alien.rect.width)
    number_rows = get_number_rows(gameSettings, ship.rect.height,alien.rect.height)

    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(gameSettings, screen, aliens, alien_number,row_number)


def get_number_aliens_x(gameSettings,alien_width):
    """ compute how many alines a line can hold"""
    available_space_x = gameSettings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return  number_aliens_x

def create_alien(gameSettings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(gameSettings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -(3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return  number_rows


def update_aliens(gameSettings,aliens):
    """更新外星人群中所有外星人的位置"""
    check_fleet_edges(gameSettings, aliens)
    aliens.update()

def check_fleet_edges(gameSettings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(gameSettings, aliens)
            break

def change_fleet_direction(gameSettings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += gameSettings.fleet_drop_speed
    gameSettings.fleet_direction *= -1