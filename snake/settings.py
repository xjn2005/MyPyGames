class Setting:
    """
    存储游戏《贪吃蛇》中所有设置的类
    """
    def __init__(self):
        """初始化游戏的静态设置"""

        self.UP = (0, -1)
        self.DOWN = (0, 1)
        self.LEFT = (-1, 0)
        self.RIGHT = (1, 0)
        # 屏幕设置
        self.UI_PANEL_HEIGHT = 60 
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.TOTAL_SCREEN_WIDTH = self.SCREEN_WIDTH  # 兼容之前的代码，如有侧边栏可修改
        self.BACKGROUND_COLOR = (0, 0, 0)  # 黑色背景
        self.COLOR_UI_PANEL = (40, 40, 40) # 顶部信息栏背景
        # 网格和方块设置
        self.GRID_SIZE = 20
        self.GRID_WIDTH = self.SCREEN_WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = self.SCREEN_HEIGHT // self.GRID_SIZE

        # 颜色设置
        self.COLOR_SNAKE = (0, 255, 0)        # 蛇的颜色（绿色）
        self.COLOR_FOOD = (255, 0, 0)         # 食物的颜色（红色）
        self.COLOR_TEXT = (255, 255, 255)     # 文字颜色（白色）
        self.COLOR_OBSTACLE = (100, 100, 100) # 障碍物颜色（灰色）
        self.COLOR_GRID_LINE = (40, 40, 40)   # 网格线颜色（深灰色）
        self.COLOR_PAUSE = (255, 255, 255)    # 暂停文字颜色
        self.COLOR_GAME_OVER_MASK = (0, 0, 0, 180) # 游戏结束遮罩颜色（半透明黑）

        # 游戏逻辑设置
        self.FPS = 60  # 渲染帧率
        self.INITIAL_LOGIC_INTERVAL = 150    # 初始蛇移动间隔（毫秒）
        self.LOGIC_INTERVAL_DECREASE = 5     # 每次升级减少的间隔（毫秒）
        self.MIN_LOGIC_INTERVAL = 50         # 最小移动间隔（毫秒），防止速度过快
        self.LEVEL_UP_THRESHOLD = 100        # 每获得100分升级一次

        # 障碍物设置
        self.OBSTACLE_CHANGE_INTERVAL = 30000 # 障碍物变换间隔（毫秒）
        self.OBSTACLE_SEGMENT_COUNT_RANGE = (15, 20) # 障碍物总段数范围

        # 字体设置 (如果需要使用系统字体，可以指定字体名)
        self.FONT_TITLE = "PressStart2P-Regular.ttf"  # 像素风格字体文件
        self.FONT_TITLE_SIZE = 72                     # 标题字体大小

        self.FONT_MAIN = None  # 使用默认字体
        self.FONT_LARGE_SIZE = 60
        self.FONT_NORMAL_SIZE = 36
        self.FONT_SMALL_SIZE = 24

        # 音效设置
        self.SOUND_VOLUME = 0.7