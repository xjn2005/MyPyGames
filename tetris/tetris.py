import pygame
import random
import json
import os
import sys  
from settings import Setting

def load_ranking(settings):
    if not os.path.exists(settings.ranking_file):
        return []
    try:
        with open(settings.ranking_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_ranking(new_score, new_name, settings):
    rankings = load_ranking(settings)
    rankings.append({"name": new_name, "score": new_score})
    rankings = sorted(rankings, key=lambda x: -x["score"])[:settings.max_ranking]
    with open(settings.ranking_file, "w", encoding="utf-8") as f:
        json.dump(rankings, f, ensure_ascii=False, indent=2)

def get_player_name(screen, font, settings):
    name = ""
    input_active = True
    while input_active:
        screen.fill(settings.black)
        prompt_text = font.render("Enter your name (max 6 chars):", True, settings.white)
        prompt_rect = prompt_text.get_rect(center=(settings.total_screen_width//2, settings.screen_height//2 - 50))
        screen.blit(prompt_text, prompt_rect)
        name_text = font.render(name, True, settings.blue)
        name_rect = name_text.get_rect(center=(settings.total_screen_width//2, settings.screen_height//2))
        screen.blit(name_text, name_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 6 and event.unicode.isalnum():
                    name = name + event.unicode
        
        pygame.display.flip()
    return name.strip()

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.settings = Setting()
        self.screen = pygame.display.set_mode((self.settings.total_screen_width, self.settings.screen_height))
        pygame.display.set_caption("俄罗斯方块")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 24)

        self.fall_event = pygame.USEREVENT + 1

        self.grid = []
        self.current_shape = []
        self.current_color = 0
        self.current_x = 0
        self.current_y = 0
        self.next_shape = []
        self.next_color = 0
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.menu_state = "main"

        self._init_game_state()

    def _init_game_state(self):
        self.grid = [[0 for _ in range(self.settings.grid_width)] for _ in range(self.settings.grid_height)]
        self._spawn_new_shape()
        self._spawn_next_shape()
        self.level = 1
        self._update_fall_speed()
        self.score = 0
        self.game_over = False
        self.paused = False

    def _spawn_new_shape(self):
        self.current_shape = self.next_shape if self.next_shape else self.settings.block_shapes[random.randint(0, 6)]
        self.current_color = self.next_color if self.next_color else random.randint(1, 7)
        self.current_x = (self.settings.grid_width - len(self.current_shape[0])) // 2
        self.current_y = 0
        if self._check_collision(self.current_shape, self.current_x, self.current_y):
            self.game_over = True
            self.menu_state = "game_over"

    def _spawn_next_shape(self):
        shape_idx = random.randint(0, len(self.settings.block_shapes)-1)
        self.next_shape = self.settings.block_shapes[shape_idx]
        self.next_color = shape_idx + 1

    def _check_collision(self, shape, x, y):
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    new_x = x + col_idx
                    new_y = y + row_idx
                    if new_x < 0 or new_x >= self.settings.grid_width or new_y >= self.settings.grid_height:
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x] != 0:
                        return True
        return False

    def _rotate_shape(self, shape):
        return [list(row) for row in zip(*shape[::-1])]

    def _merge_shape(self):
        for row_idx, row in enumerate(self.current_shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    new_x = self.current_x + col_idx
                    new_y = self.current_y + row_idx
                    if new_y >= 0:
                        self.grid[new_y][new_x] = self.current_color

    def _clear_full_lines(self):
        new_grid = []
        lines_cleared = 0
        for row in self.grid:
            if all(cell != 0 for cell in row):
                lines_cleared += 1
            else:
                new_grid.append(row)
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(self.settings.grid_width)])
        if lines_cleared > 0:
            score_multiplier = [0, 1, 1.5, 2, 3]
            lines_cleared = min(lines_cleared, 4)
            self.score += int(lines_cleared * 100 * score_multiplier[lines_cleared] * self.level)
            self._check_level_up()
        self.grid = new_grid

    def _check_level_up(self):
        for i in range(len(self.settings.level_threshold)-1, 0, -1):
            if self.score >= self.settings.level_threshold[i] and self.level < i+1:
                self.level = i+1
                self._update_fall_speed()
                print(f"升级！当前等级：{self.level}，下落速度：{self.settings.level_speed[self.level-1]}ms")
                break

    def _update_fall_speed(self):
        speed = self.settings.level_speed[min(self.level-1, len(self.settings.level_speed)-1)]
        pygame.time.set_timer(self.fall_event, speed)

    def _draw_grid(self):
        grid_start_x = 0
        grid_start_y = 0
        # 绘制网格线
        for y in range(self.settings.grid_height + 1):
            y_pos = grid_start_y + y * self.settings.block_size
            pygame.draw.line(
                self.screen, self.settings.light_gray,
                (grid_start_x, y_pos),
                (grid_start_x + self.settings.grid_width * self.settings.block_size, y_pos),
                2
            )
        for x in range(self.settings.grid_width + 1):
            x_pos = grid_start_x + x * self.settings.block_size
            pygame.draw.line(
                self.screen, self.settings.light_gray,
                (x_pos, grid_start_y),
                (x_pos, grid_start_y + self.settings.grid_height * self.settings.block_size),
                2
            )
        # 绘制已落地方块
        for y in range(self.settings.grid_height):
            for x in range(self.settings.grid_width):
                color_idx = self.grid[y][x]
                if color_idx != 0:
                    color = self.settings.block_colors[color_idx - 1]
                    rect_x = grid_start_x + x * self.settings.block_size + 2
                    rect_y = grid_start_y + y * self.settings.block_size + 2
                    rect_w = self.settings.block_size - 4
                    rect_h = self.settings.block_size - 4
                    pygame.draw.rect(self.screen, color, (rect_x, rect_y, rect_w, rect_h))
        # 绘制当前下落方块
        for row_idx, row in enumerate(self.current_shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    rect_x = grid_start_x + (self.current_x + col_idx) * self.settings.block_size + 2
                    rect_y = grid_start_y + (self.current_y + row_idx) * self.settings.block_size + 2
                    rect_w = self.settings.block_size - 4
                    rect_h = self.settings.block_size - 4
                    color = self.settings.block_colors[self.current_color - 1]
                    pygame.draw.rect(self.screen, color, (rect_x, rect_y, rect_w, rect_h))

    def _draw_preview(self):
        # 绘制预览区边框
        pygame.draw.rect(
            self.screen, self.settings.light_gray,
            (self.settings.preview_x, self.settings.preview_y, self.settings.preview_width, self.settings.preview_height)
        )
        pygame.draw.rect(
            self.screen, self.settings.border_color,
            (self.settings.preview_x, self.settings.preview_y, self.settings.preview_width, self.settings.preview_height),
            3
        )
        # 预览文字
        preview_text = self.small_font.render("Next Piece", True, self.settings.white)
        self.screen.blit(preview_text, (self.settings.preview_x + 20, self.settings.preview_y - 30))
        # 绘制预览方块
        preview_inner_x = self.settings.preview_x + self.settings.preview_padding
        preview_inner_y = self.settings.preview_y + self.settings.preview_padding
        shape_width = len(self.next_shape[0]) * self.settings.block_size
        shape_height = len(self.next_shape) * self.settings.block_size
        offset_x = preview_inner_x + (self.settings.preview_width - 2*self.settings.preview_padding - shape_width) // 2
        offset_y = preview_inner_y + (self.settings.preview_height - 2*self.settings.preview_padding - shape_height) // 2

        for row_idx, row in enumerate(self.next_shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    rect_x = offset_x + col_idx * self.settings.block_size + 1
                    rect_y = offset_y + row_idx * self.settings.block_size + 1
                    rect_w = self.settings.block_size - 2
                    rect_h = self.settings.block_size - 2
                    color = self.settings.block_colors[self.next_color - 1]
                    pygame.draw.rect(self.screen, color, (rect_x, rect_y, rect_w, rect_h))

    def _draw_ui(self):
        score_text = self.font.render(f"Score: {int(self.score)}", True, self.settings.white)
        level_text = self.font.render(f"Level: {self.level}", True, self.settings.white)
        # 预览区下方坐标
        score_y = self.settings.preview_y + self.settings.preview_height + 20
        level_y = self.settings.preview_y + self.settings.preview_height + 60
        self.screen.blit(score_text, (self.settings.preview_x, score_y))
        self.screen.blit(level_text, (self.settings.preview_x, level_y))

        # 暂停提示
        if self.paused and not self.game_over:
            pause_text = self.font.render("Paused", True, self.settings.gray)
            self.screen.blit(pause_text, (self.settings.screen_width//2 - 40, self.settings.screen_height//2))

        # 游戏结束提示
        if self.game_over:
            mask = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
            mask.fill((0, 0, 0, 180))
            self.screen.blit(mask, (0, 0))

            game_over_text = self.large_font.render("Game Over!", True, self.settings.red)
            final_score_text = self.font.render(f"Final Score: {int(self.score)}", True, self.settings.white)
            tip_text = self.small_font.render("R: Restart | M: Menu | Q: Quit", True, self.settings.light_gray)

            game_over_rect = game_over_text.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//3))
            final_score_rect = final_score_text.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2))
            tip_rect = tip_text.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height*2//3))

            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(final_score_text, final_score_rect)
            self.screen.blit(tip_text, tip_rect)

        self._draw_preview()

    def _draw_main_menu(self):
        self.screen.fill(self.settings.black)
        title_text = pygame.font.Font(None, 48).render("Tetris", True, self.settings.blue)
        self.screen.blit(title_text, (self.settings.total_screen_width//2 - 60, self.settings.screen_height//2 - 100))
        
        start_text = self.font.render("1. Start Game", True, self.settings.white)
        rank_text = self.font.render("2. Ranking", True, self.settings.white)
        quit_text = self.font.render("3. Quit", True, self.settings.white)
        
        self.screen.blit(start_text, (self.settings.total_screen_width//2 - 80, self.settings.screen_height//2))
        self.screen.blit(rank_text, (self.settings.total_screen_width//2 - 80, self.settings.screen_height//2 + 50))
        self.screen.blit(quit_text, (self.settings.total_screen_width//2 - 80, self.settings.screen_height//2 + 100))

    def _draw_ranking(self):
        self.screen.fill(self.settings.black)
        rank_title = self.font.render("Top 5 Ranking", True, self.settings.blue)
        self.screen.blit(rank_title, (self.settings.total_screen_width//2 - 90, 50))
        
        rankings = load_ranking(self.settings)
        if not rankings:
            no_rank_text = self.small_font.render("No scores yet!", True, self.settings.gray)
            self.screen.blit(no_rank_text, (self.settings.total_screen_width//2 - 60, self.settings.screen_height//2))
        else:
            for i, rank in enumerate(rankings):
                rank_text = self.font.render(f"{i+1}. {rank['name']:6s} {rank['score']}", True, self.settings.white)
                self.screen.blit(rank_text, (self.settings.total_screen_width//2 - 100, 150 + i*50))
        
        back_text = self.small_font.render("Press M to return to menu", True, self.settings.light_gray)
        self.screen.blit(back_text, (self.settings.total_screen_width//2 - 100, self.settings.screen_height - 50))

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  

            # 方块自动下落事件
            if event.type == self.fall_event and self.menu_state == "playing" and not self.paused and not self.game_over:
                if not self._check_collision(self.current_shape, self.current_x, self.current_y + 1):
                    self.current_y += 1
                else:
                    self._merge_shape()
                    self._clear_full_lines()
                    self._spawn_new_shape()
                    self._spawn_next_shape()

            # 键盘事件
            if event.type == pygame.KEYDOWN:
                if self.menu_state == "main":
                    if event.key == pygame.K_1:
                        self.menu_state = "playing"
                    elif event.key == pygame.K_2:
                        self.menu_state = "ranking"
                    elif event.key == pygame.K_3:
                        pygame.quit()
                        sys.exit()  
                elif self.menu_state == "ranking":
                    if event.key == pygame.K_m:
                        self.menu_state = "main"
                elif self.menu_state == "playing":
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_LEFT and not self.paused:
                        if not self._check_collision(self.current_shape, self.current_x - 1, self.current_y):
                            self.current_x -= 1
                    elif event.key == pygame.K_RIGHT and not self.paused:
                        if not self._check_collision(self.current_shape, self.current_x + 1, self.current_y):
                            self.current_x += 1
                    elif event.key == pygame.K_DOWN and not self.paused:
                        if not self._check_collision(self.current_shape, self.current_x, self.current_y + 1):
                            self.current_y += 1
                    elif event.key == pygame.K_UP and not self.paused:
                        rotated_shape = self._rotate_shape(self.current_shape)
                        if not self._check_collision(rotated_shape, self.current_x, self.current_y):
                            self.current_shape = rotated_shape
                elif self.menu_state == "game_over":
                    if event.key == pygame.K_r:
                        self._init_game_state()
                        self.menu_state = "playing"
                    elif event.key == pygame.K_m:
                        name = get_player_name(self.screen, self.font, self.settings)
                        save_ranking(int(self.score), name, self.settings)
                        self.menu_state = "main"
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()  
    def run(self):
        while True:
            self._handle_events()
            self.screen.fill(self.settings.black)
            if self.menu_state == "main":
                self._draw_main_menu()
            elif self.menu_state == "ranking":
                self._draw_ranking()
            elif self.menu_state in ["playing", "game_over"]:
                self._draw_grid()
                self._draw_ui()
            pygame.display.flip()
            self.clock.tick(self.settings.fps)


if __name__ == "__main__":
    game = TetrisGame()
    game.run()