import pygame
from pygame.sprite import Sprite


#Sprite is the parent of Bullet
class Bullet(Sprite):
    """manage te bullet"""
    def __init__(self, gameSettings, screen, ship):
        """create a bullet object in the position of the ship """
        super(Bullet, self).__init__()
        self.screen = screen
        # create a rect at (0,0) to represent bullet ,then put it to the right position
        self.rect = pygame.Rect(0, 0, gameSettings.bullet_width,gameSettings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # store the bullet position by float
        self.y = float(self.rect.y)
        self.color = gameSettings.bullet_color
        self.speed_factor = gameSettings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.speed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)