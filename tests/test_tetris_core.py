import unittest

from tetris.core import TetrisCore
from tetris.settings import Setting


class SequenceRandom:
    def __init__(self, values):
        self.values = iter(values)

    def randrange(self, stop):
        return next(self.values) % stop


class TetrisCoreTests(unittest.TestCase):
    def setUp(self):
        self.settings = Setting()
        self.core = TetrisCore(
            self.settings,
            randomizer=SequenceRandom([0, 1, 2, 3, 4, 5, 6]),
        )

    def test_rotate_clockwise(self):
        self.assertEqual(
            self.core.rotate([[1, 0], [1, 1]]),
            [[1, 1], [1, 0]],
        )

    def test_collision_detects_walls_floor_and_settled_blocks(self):
        self.assertTrue(self.core.collides([[1]], -1, 0))
        self.assertTrue(self.core.collides([[1]], 0, self.settings.grid_height))

        self.core.grid[5][4] = 1
        self.assertTrue(self.core.collides([[1]], 4, 5))
        self.assertFalse(self.core.collides([[1]], 3, 5))

    def test_merge_piece_writes_color_to_grid(self):
        self.core.current_shape = [[1, 1], [0, 1]]
        self.core.current_color = 3
        self.core.current_x = 4
        self.core.current_y = 5

        self.core.merge_piece()

        self.assertEqual(self.core.grid[5][4:6], [3, 3])
        self.assertEqual(self.core.grid[6][5], 3)

    def test_clear_single_line_uses_existing_score_rule(self):
        self.core.grid[-1] = [1] * self.settings.grid_width

        cleared = self.core.clear_full_lines()

        self.assertEqual(cleared, 1)
        self.assertEqual(self.core.score, 100)
        self.assertEqual(self.core.grid[0], [0] * self.settings.grid_width)

    def test_clear_multiple_lines_uses_existing_score_rule(self):
        self.core.level = 2
        self.core.grid[-2:] = [
            [1] * self.settings.grid_width,
            [1] * self.settings.grid_width,
        ]

        cleared = self.core.clear_full_lines()

        self.assertEqual(cleared, 2)
        self.assertEqual(self.core.score, 600)

    def test_score_threshold_updates_level(self):
        self.core.score = 5_000

        self.core.update_level()

        self.assertEqual(self.core.level, 4)
        self.assertEqual(self.core.fall_speed, 200)

    def test_next_piece_is_promoted_and_replaced(self):
        next_shape = self.core.next_shape
        next_color = self.core.next_color

        self.core.promote_next_piece()

        self.assertEqual(self.core.current_shape, next_shape)
        self.assertEqual(self.core.current_color, next_color)
        self.assertNotEqual(self.core.next_shape, next_shape)

    def test_step_down_locks_piece_and_spawns_the_next_piece(self):
        self.core.current_shape = [[1, 1]]
        self.core.current_color = 4
        self.core.current_x = 4
        self.core.current_y = self.settings.grid_height - 1
        expected_next = self.core.next_shape

        moved = self.core.step_down()

        self.assertFalse(moved)
        self.assertEqual(self.core.grid[-1][4:6], [4, 4])
        self.assertEqual(self.core.current_shape, expected_next)

    def test_blocked_spawn_marks_game_over(self):
        self.core.grid[0] = [1] * self.settings.grid_width

        self.core.promote_next_piece()

        self.assertTrue(self.core.game_over)


if __name__ == "__main__":
    unittest.main()
