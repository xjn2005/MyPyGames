import pygame
import sys
from settings import Setting
from food import Food
from snake import Snake
from obstacle import Obstacle
from screen import Screen

class Game:
    
    def __init__(self):
        pygame.init()
        self.settings = Setting()

        # 初始化窗口和时钟
        self.screen = pygame.display.set_mode((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game - Select Mode")
        self.clock = pygame.time.Clock()
        
        # 初始化字体
        self.font_large = pygame.font.Font(self.settings.FONT_MAIN, self.settings.FONT_LARGE_SIZE)
        self.font_normal = pygame.font.Font(self.settings.FONT_MAIN, self.settings.FONT_NORMAL_SIZE)
        self.font_small = pygame.font.Font(self.settings.FONT_MAIN, self.settings.FONT_SMALL_SIZE)

        # 初始化游戏对象
        self.snake = Snake(self.settings)
        self.food = Food()
        self.obstacle = Obstacle(self.settings)
        
        # 初始化屏幕渲染
        self.screen_renderer = Screen(self)
        
        # 添加游戏逻辑定时
        self.game_logic_event = pygame.USEREVENT + 1
        
        # 初始化游戏状态
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.mode = None
        self.menu_state = "splash" 
        
        # 障碍物变换相关变量
        self.obstacle_change_interval = self.settings.OBSTACLE_CHANGE_INTERVAL
        self.last_obstacle_change_time = pygame.time.get_ticks()
        self.obstacle_change_timer = 0

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == self.game_logic_event and self.menu_state == "playing" and not self.paused and not self.game_over:
                self.update_game_logic()
            
            elif event.type == pygame.KEYDOWN:
                if self.menu_state == "splash":
                    # 从启动画面按任意键进入模式选择
                    self.menu_state = "mode_selection"
                if self.menu_state == "mode_selection":
                    self._handle_mode_selection(event)
                elif self.menu_state == "playing":
                    self._handle_playing(event)
                elif self.menu_state == "game_over":
                    self._handle_game_over(event)
    
    def update_game_logic(self):
        """更新游戏逻辑（蛇移动、碰撞检测等）"""
        self.snake.move(self.mode)
        
        if self.snake.check_collision(self.obstacle.segments, self.mode):
            self.game_over = True
            self.menu_state = "game_over"
            return
        
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.score += 10 * self.level
            
            if self.score >= self.level * self.settings.LEVEL_UP_THRESHOLD:
                self.level_up()
            
            self.food.generate(self.snake.body, self.obstacle.segments, self.mode, self.settings)
        
        if self.mode == "endless_obstacle":
            current_time = pygame.time.get_ticks()
            time_since_last_change = current_time - self.last_obstacle_change_time
            
            self.obstacle_change_timer = max(0, self.obstacle_change_interval - time_since_last_change)
            
            if time_since_last_change >= self.obstacle_change_interval:
                self.obstacle.generate(self.snake.body, self.food.position)
                self.last_obstacle_change_time = current_time
    
    def level_up(self):
        """升级"""
        self.level += 1
        print(f"升级！当前等级：{self.level}")
        
        new_interval = max(
            self.settings.INITIAL_LOGIC_INTERVAL - (self.level - 1) * self.settings.LOGIC_INTERVAL_DECREASE, 
            self.settings.MIN_LOGIC_INTERVAL
        )
        pygame.time.set_timer(self.game_logic_event, new_interval)
    
    def _handle_mode_selection(self, event):
        if event.key == pygame.K_1:
            self.mode = "classic"
            self.start_game()
        elif event.key == pygame.K_2:
            self.mode = "endless_obstacle"
            self.start_game()
        elif event.key == pygame.K_3:
            pygame.quit()
            sys.exit()
    
    def _handle_playing(self, event):
        if event.key == pygame.K_UP:
            self.snake.change_direction(self.settings.UP)
        elif event.key == pygame.K_DOWN:
            self.snake.change_direction(self.settings.DOWN)
        elif event.key == pygame.K_LEFT:
            self.snake.change_direction(self.settings.LEFT)
        elif event.key == pygame.K_RIGHT:
            self.snake.change_direction(self.settings.RIGHT)
        elif event.key == pygame.K_SPACE:
            self.paused = not self.paused
        elif event.key == pygame.K_ESCAPE:
            self.menu_state = "mode_selection"
    
    def _handle_game_over(self, event):
        if event.key == pygame.K_SPACE:
            self.start_game()
        elif event.key == pygame.K_m:
            self.menu_state = "mode_selection"
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    
    def start_game(self):
        """开始游戏"""
        self.snake = Snake(self.settings)
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        
        self.food.generate(self.snake.body, self.obstacle.segments, self.mode, self.settings)
        
        if self.mode == "endless_obstacle":
            self.obstacle.generate(self.snake.body, self.food.position)
            self.last_obstacle_change_time = pygame.time.get_ticks()
            self.obstacle_change_timer = 0
        
        pygame.time.set_timer(self.game_logic_event, self.settings.INITIAL_LOGIC_INTERVAL)
        
        self.menu_state = "playing"
    
    def run(self):
        while True:
            self.handle_events()
            self.screen_renderer.draw()
            self.clock.tick(self.settings.FPS)  

if __name__ == "__main__":
    game = Game()
    game.run()