import pygame
from settings import Setting

class Screen:

    def __init__(self, game_instance):
        self.game = game_instance
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        
        self.font_large = game_instance.font_large
        self.font_normal = game_instance.font_normal
        self.font_small = game_instance.font_small
        self.game_area_top = self.settings.UI_PANEL_HEIGHT

    def draw(self):
        self.screen.fill(self.settings.BACKGROUND_COLOR)

        if self.game.menu_state == "splash":
            self._draw_splash()
        elif self.game.menu_state == "mode_selection":
            self._draw_mode_selection()
        elif self.game.menu_state == "playing":
            self._draw_playing()
        elif self.game.menu_state == "game_over":
            self._draw_game_over()
        
        pygame.display.flip()

    def _draw_splash(self):
        """绘制启动画面"""
        title_font = pygame.font.Font(self.settings.FONT_TITLE, self.settings.FONT_TITLE_SIZE)
        snake_title = title_font.render("SNAKE", True, (255, 255, 255)) # 白色
        snake_title_rect = snake_title.get_rect(center=(self.settings.SCREEN_WIDTH / 2, self.settings.SCREEN_HEIGHT / 2))
        self.screen.blit(snake_title, snake_title_rect)

        # 2. 绘制提示文字
        prompt_text = self.font_small.render("Press any key to continue...", True, self.settings.COLOR_TEXT)

        prompt_text_rect = prompt_text.get_rect(center=(snake_title_rect.centerx, snake_title_rect.bottom + 20))
        self.screen.blit(prompt_text, prompt_text_rect)

    def _draw_mode_selection(self):
        """绘制模式选择菜单"""
        # 定义所有要显示的文本
        sub_title = self.font_normal.render("Select Game Mode", True, self.settings.COLOR_TEXT)
        mode1_text = self.font_small.render("1. Classic Mode", True, self.settings.COLOR_TEXT)
        mode2_text = self.font_small.render("2. Endless Obstacle Mode", True, self.settings.COLOR_TEXT)
        quit_text = self.font_small.render("3. Quit", True, self.settings.COLOR_TEXT)

        # 计算所有文本和间距的总高度，用于垂直居中
        # 文本高度
        sub_title_height = sub_title.get_height()
        mode1_height = mode1_text.get_height()
        mode2_height = mode2_text.get_height()
        quit_height = quit_text.get_height()
        
        # 文本之间的间距
        spacing = 30
        
        # 总高度
        total_height = sub_title_height + spacing + mode1_height + spacing + mode2_height + spacing + quit_height

        # 计算起始Y坐标，使整个菜单垂直居中
        start_y = (self.settings.SCREEN_HEIGHT - total_height) // 2

        # 绘制副标题
        sub_title_x = self.settings.SCREEN_WIDTH // 2 - sub_title.get_width() // 2
        self.screen.blit(sub_title, (sub_title_x, start_y))

        # 绘制各个选项，依次向下排列
        current_y = start_y + sub_title_height + spacing
        
        mode1_x = self.settings.SCREEN_WIDTH // 2 - mode1_text.get_width() // 2
        self.screen.blit(mode1_text, (mode1_x, current_y))
        
        current_y += mode1_height + spacing
        
        mode2_x = self.settings.SCREEN_WIDTH // 2 - mode2_text.get_width() // 2
        self.screen.blit(mode2_text, (mode2_x, current_y))
        
        current_y += mode2_height + spacing
        
        quit_x = self.settings.SCREEN_WIDTH // 2 - quit_text.get_width() // 2
        self.screen.blit(quit_text, (quit_x, current_y))


    def _draw_playing(self):
        """绘制游戏进行中的界面"""
        # 1. 绘制游戏场景（蛇、食物、障碍物等）
        self._draw_game_scene()
        
        # 2. 绘制顶部的用户界面（分数、等级等）
        self._draw_ui_panel()
        
        # 3. 绘制其他覆盖元素（暂停、倒计时）
        self._draw_overlay_elements()

    def _draw_game_over(self):
        """绘制游戏结束界面"""
        # 1. 先绘制游戏结束前的最后一帧场景
        self._draw_game_scene()
        
        # 2. 绘制顶部UI
        self._draw_ui_panel()
        
        # 3. 绘制游戏结束遮罩和文本
        mask = pygame.Surface((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        mask.fill(self.settings.COLOR_GAME_OVER_MASK)
        self.screen.blit(mask, (0, 0))
        
        game_over_text = self.font_large.render("Game Over", True, self.settings.COLOR_TEXT)
        final_score_text = self.font_small.render(f"Final Score: {self.game.score}", True, self.settings.COLOR_TEXT)
        final_level_text = self.font_small.render(f"Final Level: {self.game.level}", True, self.settings.COLOR_TEXT)
        restart_text = self.font_small.render("Press SPACE to restart", True, self.settings.COLOR_TEXT)
        menu_text = self.font_small.render("Press M to return to menu", True, self.settings.COLOR_TEXT)
        quit_text = self.font_small.render("Press ESC to quit", True, self.settings.COLOR_TEXT)
        
        # 让文本在游戏区域内居中
        text_y_offset = self.game_area_top + (self.settings.SCREEN_HEIGHT - self.game_area_top) // 2
        
        self.screen.blit(game_over_text, (self.settings.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, text_y_offset - 100))
        self.screen.blit(final_score_text, (self.settings.SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, text_y_offset - 50))
        self.screen.blit(final_level_text, (self.settings.SCREEN_WIDTH // 2 - final_level_text.get_width() // 2, text_y_offset - 20))
        self.screen.blit(restart_text, (self.settings.SCREEN_WIDTH // 2 - restart_text.get_width() // 2, text_y_offset + 30))
        self.screen.blit(menu_text, (self.settings.SCREEN_WIDTH // 2 - menu_text.get_width() // 2, text_y_offset + 60))
        self.screen.blit(quit_text, (self.settings.SCREEN_WIDTH // 2 - quit_text.get_width() // 2, text_y_offset + 90))

    def _draw_game_scene(self):
        """专门绘制游戏核心场景（网格、蛇、食物、障碍物）"""
        self._draw_grid()
        
        if self.game.mode == "endless_obstacle":
            self.game.obstacle.draw(self.screen)
        
        self.game.snake.draw(self.screen)
        self.game.food.draw(self.screen, self.settings)

    def _draw_ui_panel(self):
        """绘制顶部的UI信息栏"""
        # 1. 绘制一个背景板，让UI更清晰
        panel_rect = pygame.Rect(0, 0, self.settings.SCREEN_WIDTH, self.game_area_top)
        pygame.draw.rect(self.screen, self.settings.COLOR_UI_PANEL, panel_rect)

        # 2. 绘制UI文本
        score_text = self.font_small.render(f"Score: {self.game.score}", True, self.settings.COLOR_TEXT)
        level_text = self.font_small.render(f"Level: {self.game.level}", True, self.settings.COLOR_TEXT)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 35))
        
        mode_name = "Classic" if self.game.mode == "classic" else "Endless Obstacle"
        mode_text = self.font_small.render(f"Mode: {mode_name}", True, self.settings.COLOR_TEXT)
        self.screen.blit(mode_text, (self.settings.SCREEN_WIDTH - mode_text.get_width() - 10, 20))

    def _draw_overlay_elements(self):
        """绘制覆盖在游戏场景上的临时元素（如暂停、倒计时）"""
        if self.game.mode == "endless_obstacle" and self.game.obstacle_change_timer > 0:
            seconds_left = int(self.game.obstacle_change_timer / 1000) + 1
            timer_text = self.font_small.render(f"Obstacles change in: {seconds_left}s", True, self.settings.COLOR_TEXT)
            self.screen.blit(timer_text, (self.settings.SCREEN_WIDTH // 2 - timer_text.get_width() // 2, self.game_area_top + 10))
        
        if self.game.paused:
            pause_text = self.font_normal.render("PAUSED", True, self.settings.COLOR_PAUSE)
            self.screen.blit(pause_text, (self.settings.SCREEN_WIDTH // 2 - pause_text.get_width() // 2, self.game_area_top + (self.settings.SCREEN_HEIGHT - self.game_area_top) // 2))

    def _draw_grid(self):
        """绘制网格背景 (只在游戏区域内)"""
        for x in range(0, self.settings.SCREEN_WIDTH, self.settings.GRID_SIZE):
            pygame.draw.line(self.screen, self.settings.COLOR_GRID_LINE, (x, self.game_area_top), (x, self.settings.SCREEN_HEIGHT))
        for y in range(self.game_area_top, self.settings.SCREEN_HEIGHT, self.settings.GRID_SIZE):
            pygame.draw.line(self.screen, self.settings.COLOR_GRID_LINE, (0, y), (self.settings.SCREEN_WIDTH, y))