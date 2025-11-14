class Setting:
    def __init__(self):
        # 基础配置
        self.screen_width = 300
        self.screen_height = 600
        self.block_size = 30
        self.grid_width = 10
        self.grid_height = 20
        self.fps = 60
        self.border_padding = 5

        # 等级配置
        self.level_threshold = [0, 1000, 2500, 5000, 10000, 20000]
        self.level_speed = [500, 400, 300, 200, 150, 100]

        # 预览区配置（依赖基础配置，需在基础配置后初始化）
        self.preview_width = 120
        self.preview_height = 120
        self.preview_x = self.screen_width + 20
        self.preview_y = 50
        self.preview_padding = 5

        # 排行榜配置
        self.ranking_file = "tetris_ranking.json"
        self.max_ranking = 5

        # 颜色配置
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gray = (128, 128, 128)
        self.light_gray = (200, 200, 200)
        self.border_color = (255, 255, 255)
        self.red = (255, 0, 0)
        self.blue = (0, 100, 255)
        self.block_colors = [
            (0, 255, 255),    # I型：青色
            (255, 255, 0),    # O型：黄色
            (128, 0, 128),    # T型：紫色
            (255, 165, 0),    # L型：橙色
            (0, 0, 255),      # J型：蓝色
            (0, 255, 0),      # S型：绿色
            (255, 0, 0)       # Z型：红色
        ]

        # 方块形状配置
        self.block_shapes = [
            [[1, 1, 1, 1]],                              # I型
            [[1, 1], [1, 1]],                             # O型
            [[0, 1, 0], [1, 1, 1]],                       # T型
            [[0, 0, 1], [1, 1, 1]],                       # L型
            [[1, 0, 0], [1, 1, 1]],                       # J型
            [[0, 1, 1], [1, 1, 0]],                       # S型
            [[1, 1, 0], [0, 1, 1]]                        # Z型
        ]

        # 窗口总宽度（依赖基础配置和预览区配置）
        self.total_screen_width = self.screen_width + self.preview_width + 40