import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from tetris.core import TetrisCore
from tetris.settings import Setting
from tetris.ui import TetrisUI


class TetrisUISmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.settings = Setting()
        self.screen = pygame.display.set_mode(
            (self.settings.total_screen_width, self.settings.screen_height)
        )
        self.core = TetrisCore(self.settings)
        self.ui = TetrisUI(self.screen, self.settings)

    def test_all_primary_screens_draw_without_errors(self):
        self.ui.draw_main_menu()
        self.ui.draw_game(self.core, paused=False)
        self.ui.draw_game(self.core, paused=True)
        self.ui.draw_ranking([{"name": "ADA", "score": 500}])

        self.core.game_over = True
        self.ui.draw_game(self.core, paused=False)
        self.ui.draw_name_prompt("ADA", self.core.score)

        pygame.display.flip()


if __name__ == "__main__":
    unittest.main()
