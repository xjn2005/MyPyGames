import os

import pygame

try:
    from .core import TetrisCore
    from .rank import Ranking
    from .settings import Setting
    from .ui import TetrisUI
except ImportError:
    from core import TetrisCore
    from rank import Ranking
    from settings import Setting
    from ui import TetrisUI


class TetrisGame:
    def __init__(self, headless=False, ranking_path=None):
        if headless:
            os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

        pygame.init()
        self.settings = Setting()
        self.screen = pygame.display.set_mode(
            (self.settings.total_screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.fall_event = pygame.USEREVENT + 1

        self.core = TetrisCore(self.settings)
        self.ranking = Ranking(self.settings, path=ranking_path)
        self.ui = TetrisUI(self.screen, self.settings)

        self.running = True
        self.paused = False
        self.menu_state = "main"
        self._set_fall_timer()

    def _set_fall_timer(self):
        pygame.time.set_timer(self.fall_event, self.core.fall_speed)

    def start_game(self):
        self.core.reset()
        self.paused = False
        self.menu_state = "playing"
        self._set_fall_timer()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                continue

            if (
                event.type == self.fall_event
                and self.menu_state == "playing"
                and not self.paused
                and not self.core.game_over
            ):
                old_speed = self.core.fall_speed
                self.core.step_down()
                if self.core.fall_speed != old_speed:
                    self._set_fall_timer()
                continue

            if event.type != pygame.KEYDOWN:
                continue

            if self.menu_state == "main":
                self._handle_main_menu_key(event.key)
            elif self.menu_state == "ranking":
                if event.key == pygame.K_m:
                    self.menu_state = "main"
            elif self.menu_state == "playing":
                self._handle_playing_key(event.key)
            elif self.menu_state == "game_over":
                self._handle_game_over_key(event.key)

        if self.menu_state == "playing" and self.core.game_over:
            self.menu_state = "game_over"
            self.paused = False

    def _handle_main_menu_key(self, key):
        if key == pygame.K_1:
            self.start_game()
        elif key == pygame.K_2:
            self.menu_state = "ranking"
        elif key == pygame.K_3:
            self.running = False

    def _handle_playing_key(self, key):
        if key == pygame.K_SPACE:
            self.paused = not self.paused
            return
        if self.paused:
            return

        if key == pygame.K_LEFT:
            self.core.move(-1)
        elif key == pygame.K_RIGHT:
            self.core.move(1)
        elif key == pygame.K_DOWN:
            self.core.move(0, 1)
        elif key == pygame.K_UP:
            self.core.rotate_current()

    def _handle_game_over_key(self, key):
        if key == pygame.K_r:
            self.start_game()
        elif key == pygame.K_m:
            name = self.get_player_name()
            if name:
                self.ranking.save(self.core.score, name)
                self.menu_state = "main"
        elif key == pygame.K_q:
            self.running = False

    def get_player_name(self):
        name = ""
        while self.running:
            self.ui.draw_name_prompt(name, self.core.score)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None
                if event.type != pygame.KEYDOWN:
                    continue
                if event.key == pygame.K_RETURN and name:
                    return name
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                    continue

                character = getattr(event, "unicode", "")
                if len(name) < 6 and character.isalnum():
                    name += character

            self.clock.tick(self.settings.fps)
        return None

    def draw(self):
        if self.menu_state == "main":
            self.ui.draw_main_menu()
        elif self.menu_state == "ranking":
            self.ui.draw_ranking(self.ranking.load())
        elif self.menu_state in {"playing", "game_over"}:
            self.ui.draw_game(self.core, paused=self.paused)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.settings.fps)
        pygame.quit()


if __name__ == "__main__":
    TetrisGame().run()
