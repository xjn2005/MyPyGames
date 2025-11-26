# food.py

import random
import pygame
from settings import Setting

class Food:
    """
    食物类，负责生成和绘制食物。
    """
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0) # 临时颜色，会在generate中从settings获取

    def generate(self, snake_body, obstacle_segments, mode, settings: Setting):
        """
        在游戏区域内生成一个新的食物位置，确保不与蛇身或障碍物重叠。
        :param snake_body: 蛇的身体坐标列表
        :param obstacle_segments: 障碍物的坐标列表
        :param mode: 游戏模式
        :param settings: 设置对象
        """
        self.color = settings.COLOR_FOOD # 从settings获取颜色
        game_area_height = settings.SCREEN_HEIGHT - settings.UI_PANEL_HEIGHT
        
        # 计算游戏区域内的有效网格索引范围
        max_x_idx = (settings.SCREEN_WIDTH - settings.GRID_SIZE) // settings.GRID_SIZE
        max_y_idx = (game_area_height - settings.GRID_SIZE) // settings.GRID_SIZE

        while True:
            # 随机生成网格索引
            x_idx = random.randint(0, max_x_idx)
            y_idx = random.randint(0, max_y_idx)
            
            # 转换为像素坐标，并确保Y坐标在游戏区域内
            x = x_idx * settings.GRID_SIZE
            y = settings.UI_PANEL_HEIGHT + y_idx * settings.GRID_SIZE
            
            self.position = (x, y)
            
            # 检查位置是否合法
            if (self.position not in snake_body and 
                (mode != "endless_obstacle" or self.position not in obstacle_segments)):
                break # 如果位置合法，跳出循环

    def draw(self, screen, settings: Setting):
        """
        在屏幕上绘制食物。
        :param screen: Pygame的屏幕对象
        :param settings: 设置对象
        """
        food_rect = pygame.Rect(self.position[0], self.position[1], settings.GRID_SIZE, settings.GRID_SIZE)
        pygame.draw.rect(screen, self.color, food_rect)