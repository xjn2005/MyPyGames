import os
from pathlib import Path
import unittest
from uuid import uuid4

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from tetris.tetris import TetrisGame


class TetrisGameControllerTests(unittest.TestCase):
    def setUp(self):
        ranking_path = Path(__file__).parent / f".game-ranking-{uuid4().hex}.json"
        self.addCleanup(ranking_path.unlink, missing_ok=True)
        self.game = TetrisGame(headless=True, ranking_path=ranking_path)
        pygame.event.clear()

    def tearDown(self):
        pygame.event.clear()
        pygame.quit()

    @staticmethod
    def post_key(key):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key, unicode=""))

    def test_main_menu_starts_a_fresh_game(self):
        self.game.core.score = 900
        self.post_key(pygame.K_1)

        self.game.handle_events()

        self.assertEqual(self.game.menu_state, "playing")
        self.assertEqual(self.game.core.score, 0)

    def test_main_menu_opens_ranking_and_ranking_returns_to_menu(self):
        self.post_key(pygame.K_2)
        self.game.handle_events()
        self.assertEqual(self.game.menu_state, "ranking")

        self.post_key(pygame.K_m)
        self.game.handle_events()
        self.assertEqual(self.game.menu_state, "main")

    def test_space_toggles_pause(self):
        self.game.menu_state = "playing"
        self.post_key(pygame.K_SPACE)
        self.game.handle_events()
        self.assertTrue(self.game.paused)

        self.post_key(pygame.K_SPACE)
        self.game.handle_events()
        self.assertFalse(self.game.paused)

    def test_arrow_keys_move_and_rotate_current_piece(self):
        self.game.menu_state = "playing"
        self.game.core.current_shape = [[1, 1, 1, 1]]
        self.game.core.current_x = 3
        self.game.core.current_y = 0

        self.post_key(pygame.K_LEFT)
        self.post_key(pygame.K_UP)
        self.post_key(pygame.K_DOWN)
        self.game.handle_events()

        self.assertEqual(self.game.core.current_x, 2)
        self.assertEqual(self.game.core.current_shape, [[1], [1], [1], [1]])
        self.assertEqual(self.game.core.current_y, 1)

    def test_game_over_state_is_synchronized_from_core(self):
        self.game.menu_state = "playing"
        self.game.core.game_over = True

        self.game.handle_events()

        self.assertEqual(self.game.menu_state, "game_over")

    def test_restart_resets_game(self):
        self.game.menu_state = "game_over"
        self.game.core.score = 500
        self.game.core.game_over = True
        self.post_key(pygame.K_r)

        self.game.handle_events()

        self.assertEqual(self.game.menu_state, "playing")
        self.assertEqual(self.game.core.score, 0)
        self.assertFalse(self.game.core.game_over)


if __name__ == "__main__":
    unittest.main()
