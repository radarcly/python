class Settings():
        """store all the setting of the game"""
        def __init__(self):
            """init screen appearance and ship speed"""
            self.screen_width = 800
            self.screen_height = 600
            self.bg_color = (230, 230, 230)

            self.ship_speed_factor = 1.5

            self.bullet_speed_factor = 1
            self.bullet_width = 3
            self.bullet_height = 15
            self.bullet_color = 60, 60, 60
            self.bullets_allowed = 10

            self.alien_speed_factor = 1
            self.fleet_drop_speed = 10
            # fleet_direction为1表示向右移，为-1表示向左移
            self.fleet_direction = 1
