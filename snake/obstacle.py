# obstacle.py

import pygame
import random
from settings import Setting

class Obstacle:
    """
    障碍物类，负责生成和绘制障碍物。
    """
    def __init__(self, settings: Setting):
        """
        初始化障碍物。
        :param settings: 设置对象
        """
        self.settings = settings
        self.color = self.settings.COLOR_OBSTACLE
        self.segments = []

    def generate(self, snake_body, food_position):
        """
        在游戏区域内生成新的障碍物。
        :param snake_body: 蛇的身体坐标列表
        :param food_position: 食物的坐标
        """
        self.segments.clear()
        
        # 从设置中获取障碍物数量范围
        min_segments, max_segments = self.settings.OBSTACLE_SEGMENT_COUNT_RANGE
        num_obstacles = random.randint(min_segments, max_segments)
        
        game_area_height = self.settings.SCREEN_HEIGHT - self.settings.UI_PANEL_HEIGHT
        max_x_idx = (self.settings.SCREEN_WIDTH - self.settings.GRID_SIZE) // self.settings.GRID_SIZE
        max_y_idx = (game_area_height - self.settings.GRID_SIZE) // self.settings.GRID_SIZE
        
        for _ in range(num_obstacles):
            while True:
                x_idx = random.randint(0, max_x_idx)
                y_idx = random.randint(0, max_y_idx)
                
                x = x_idx * self.settings.GRID_SIZE
                y = self.settings.UI_PANEL_HEIGHT + y_idx * self.settings.GRID_SIZE
                
                obstacle_pos = (x, y)
                
                # 确保障碍物不与蛇、食物或其他障碍物重叠
                if (obstacle_pos not in snake_body and 
                    obstacle_pos != food_position and 
                    obstacle_pos not in self.segments):
                    self.segments.append(obstacle_pos)
                    break

    def draw(self, screen):
        """
        在屏幕上绘制所有障碍物块。
        :param screen: Pygame的屏幕对象
        """
        for pos in self.segments:
            obstacle_rect = pygame.Rect(pos[0], pos[1], self.settings.GRID_SIZE, self.settings.GRID_SIZE)
            pygame.draw.rect(screen, self.color, obstacle_rect)