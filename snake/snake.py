import pygame
from settings import Setting

class Snake:
    """
    蛇类，负责处理蛇的移动、生长和碰撞检测。
    """
    def __init__(self, settings: Setting):
        self.settings = settings
        self.body = [(self.settings.SCREEN_WIDTH // 2, self.settings.SCREEN_HEIGHT // 2 + self.settings.UI_PANEL_HEIGHT)]
        self.direction = self.settings.RIGHT
        self.length = 1
        self.color = self.settings.COLOR_SNAKE

    def move(self, mode):
        """
        根据当前方向移动蛇头，并更新蛇身。
        """
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction

        # 计算新蛇头位置
        new_head_x = head_x + dir_x * self.settings.GRID_SIZE
        new_head_y = head_y + dir_y * self.settings.GRID_SIZE

        new_head = (new_head_x, new_head_y)

        # 将新蛇头插入到身体列表的最前面
        self.body.insert(0, new_head)

        # 如果长度没有增加，则删除尾部
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        """
        增加蛇的长度。
        """
        self.length += 1

    def change_direction(self, new_direction):
        """
        改变蛇的移动方向，但不允许向相反方向移动。
        """
        # 检查是否是相反方向
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def check_collision(self, obstacle_segments, mode):
        """
        检查蛇是否撞到了边界、自己或障碍物。
        :param obstacle_segments: 障碍物的身体部分列表
        :param mode: 游戏模式
        :return: 如果发生碰撞，返回 True，否则返回 False
        """
        head = self.body[0]

        # 1. 检查撞到自己
        if head in self.body[1:]:
            return True

        # 2. 检查撞到边界
        if head[0] < 0 or head[0] >= self.settings.SCREEN_WIDTH:
            return True
        if head[1] < self.settings.UI_PANEL_HEIGHT or head[1] >= self.settings.SCREEN_HEIGHT:
            return True

        # 3. 检查撞到障碍物 (无尽障碍模式)
        if mode == "endless_obstacle" and head in obstacle_segments:
            return True

        return False

    def draw(self, screen):
        """
        在屏幕上绘制蛇。
        :param screen: Pygame的屏幕对象
        """
        for segment in self.body:
            snake_rect = pygame.Rect(segment[0], segment[1], self.settings.GRID_SIZE, self.settings.GRID_SIZE)
            pygame.draw.rect(screen, self.color, snake_rect)