class GameStatus():
    """跟踪游戏的统计信息"""
    def __init__(self, gameSettings):
        """初始化统计信息"""
        self.gameSettings = gameSettings
        self.reset_status()
        # 游戏刚启动时处于活动状态
        self.game_active = False

        self.score = 0
        # 在任何情况下都不应重置最高得分
        file = open("highest.txt",'r')
        self.high_score = (int)(file.read())
        file.close()

        self.level = 1

    def reset_status(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.gameSettings.ship_limit
