import pygame


class Ship():
    def __init__(self,gameSettings, screen):
        """初始化飞船并设置其初始位置"""
        self.screen = screen
        self.gameSettings = gameSettings
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """update the ship position according to flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.gameSettings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.gameSettings.ship_speed_factor
        # self.rect.centerx 只保存整数部分，对于显示问题不大，但对于数据存储有问题，所以需要新的变量center存精确值
        self.rect.centerx = self.center
