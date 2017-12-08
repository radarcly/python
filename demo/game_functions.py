import sys
import pygame
from bullet import Bullet
from alien import  Alien
from time import sleep

def check_events(gameSettings,screen,ship,bullets,status,play_button,aliens,sb):
    """ response to  key and mouse event"""
    for event in pygame.event.get():
        #do not need argument because it copys events
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event,gameSettings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(status, play_button, mouse_x, mouse_y,aliens,bullets,ship,gameSettings,screen,sb)

def check_play_button(status, play_button, mouse_x, mouse_y,aliens,bullets,ship,gameSettings,screen,sb):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not status.game_active:
        gameSettings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        status.reset_status()
        status.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        status.score = 0
        status.level = 1

        # 创建一群新的外星人，并让飞船居中
        create_fleet(gameSettings, screen,aliens,ship)
        ship.center_ship()


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
    elif event.key == pygame.K_z:
        gameSettings.bullet_width += 10
    elif event.key == pygame.K_x:
        gameSettings.bullets_allowed += 1
    elif event.key == pygame.K_c:
        gameSettings.bullet_width -= 10
    elif  event.key == pygame.K_v:
        gameSettings.bullets_allowed -= 1
    elif event.key == pygame.K_b:
       ship.rect.centery -=1
    elif event.key == pygame.K_n:
        ship.rect.centery += 1


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


def update_screen(gameSettings,screen,ship,bullets,aliens,status,play_button,sb):
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
    sb.show_score()
    # 如果游戏处于非活动状态，就绘制Play按钮
    if not status.game_active:
        play_button.draw_button()
    # let the screen to see
    pygame.display.flip()


def update_bullets(aliens,bullets,screen,ship,gameSettings,status,sb):
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(gameSettings,screen,ship,aliens,bullets,status,sb)


def check_bullet_alien_collisions(gameSettings,screen,ship,aliens,bullets,status,sb):
    # 两个实参True告诉Pygame删除发生碰撞的子弹和外星人。（要模拟能够穿行到屏幕顶端的高能子弹——消灭它击中的每个外星人，
    # 可将第一个布尔实参设置为False，并让第二个布尔实参为True。这样
    # 被击中的外星人将消失，但所有的子弹都始终有效，直到抵达屏幕顶端后消失。）
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            status.score += gameSettings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(status, sb)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        gameSettings.increase_speed()
        status.level += 1
        sb.prep_level()
        create_fleet(gameSettings, screen, aliens, ship)

def create_fleet(gameSettings,screen,aliens,ship):
    """ create aliens"""
    alien = Alien(gameSettings, screen)
    number_aliens_x = get_number_aliens_x(gameSettings, alien.rect.width)
    number_rows = get_number_rows(gameSettings, ship.rect.height, alien.rect.height)

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
    alien.rect.y = 3*alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -(4 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return  number_rows


def update_aliens(gameSettings,aliens,ship,status,screen,bullets,sb):
    """更新外星人群中所有外星人的位置"""
    check_fleet_edges(gameSettings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
         ship_hit(gameSettings, status, screen, ship, aliens, bullets,sb)
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(gameSettings, status, screen, ship, aliens, bullets,sb)

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


def ship_hit(gameSettings, status, screen, ship, aliens, bullets,sb):
    """响应被外星人撞到的飞船"""
    # 将ships_left减1
    if status.ships_left > 0:
        # 将ships_left减1
        status.ships_left -= 1
        sb.prep_ships()
        # 暂停一会儿
        sleep(0.5)
    else:
        status.game_active = False
        pygame.mouse.set_visible(True)

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(gameSettings, screen, aliens,ship)
    ship.center_ship()

    # 暂停
    sleep(0.5)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets,sb):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets,sb)
            break


def check_high_score(status, sb):
    """检查是否诞生了新的最高得分"""

    if status.score > status.high_score:
          status.high_score = status.score
          sb.prep_high_score()
          file = open('highest.txt', 'w')
          file.write(str(status.high_score))
          file.close()
