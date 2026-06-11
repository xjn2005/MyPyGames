from copy import deepcopy
import random


class TetrisCore:
    """Owns Tetris board state and rules without depending on Pygame."""

    def __init__(self, settings, randomizer=None):
        self.settings = settings
        self.randomizer = randomizer or random
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
        self.reset()

    @property
    def fall_speed(self):
        index = min(self.level - 1, len(self.settings.level_speed) - 1)
        return self.settings.level_speed[index]

    def reset(self):
        self.grid = [
            [0 for _ in range(self.settings.grid_width)]
            for _ in range(self.settings.grid_height)
        ]
        self.score = 0
        self.level = 1
        self.game_over = False

        self.current_shape, self.current_color = self._random_piece()
        self.current_x = self._center_x(self.current_shape)
        self.current_y = 0
        self.next_shape, self.next_color = self._random_piece()

    def _random_piece(self):
        shape_index = self.randomizer.randrange(len(self.settings.block_shapes))
        return deepcopy(self.settings.block_shapes[shape_index]), shape_index + 1

    def _center_x(self, shape):
        return (self.settings.grid_width - len(shape[0])) // 2

    @staticmethod
    def rotate(shape):
        return [list(row) for row in zip(*shape[::-1])]

    def collides(self, shape, x, y):
        for row_index, row in enumerate(shape):
            for column_index, cell in enumerate(row):
                if not cell:
                    continue

                board_x = x + column_index
                board_y = y + row_index
                if (
                    board_x < 0
                    or board_x >= self.settings.grid_width
                    or board_y >= self.settings.grid_height
                ):
                    return True
                if board_y >= 0 and self.grid[board_y][board_x] != 0:
                    return True
        return False

    def move(self, delta_x, delta_y=0):
        new_x = self.current_x + delta_x
        new_y = self.current_y + delta_y
        if self.collides(self.current_shape, new_x, new_y):
            return False

        self.current_x = new_x
        self.current_y = new_y
        return True

    def rotate_current(self):
        rotated = self.rotate(self.current_shape)
        if self.collides(rotated, self.current_x, self.current_y):
            return False

        self.current_shape = rotated
        return True

    def merge_piece(self):
        for row_index, row in enumerate(self.current_shape):
            for column_index, cell in enumerate(row):
                if not cell:
                    continue

                board_x = self.current_x + column_index
                board_y = self.current_y + row_index
                if board_y >= 0:
                    self.grid[board_y][board_x] = self.current_color

    def clear_full_lines(self):
        remaining_rows = [
            row for row in self.grid if not all(cell != 0 for cell in row)
        ]
        lines_cleared = self.settings.grid_height - len(remaining_rows)
        empty_row = [0 for _ in range(self.settings.grid_width)]
        self.grid = [
            empty_row.copy() for _ in range(lines_cleared)
        ] + remaining_rows

        if lines_cleared:
            lines_cleared = min(lines_cleared, 4)
            score_multiplier = (0, 1, 1.5, 2, 3)
            self.score += int(
                lines_cleared
                * 100
                * score_multiplier[lines_cleared]
                * self.level
            )
            self.update_level()

        return lines_cleared

    def update_level(self):
        for index in range(len(self.settings.level_threshold) - 1, 0, -1):
            if self.score >= self.settings.level_threshold[index]:
                self.level = index + 1
                return
        self.level = 1

    def promote_next_piece(self):
        self.current_shape = deepcopy(self.next_shape)
        self.current_color = self.next_color
        self.current_x = self._center_x(self.current_shape)
        self.current_y = 0
        self.next_shape, self.next_color = self._random_piece()
        self.game_over = self.collides(
            self.current_shape,
            self.current_x,
            self.current_y,
        )

    def lock_piece(self):
        self.merge_piece()
        self.clear_full_lines()
        self.promote_next_piece()

    def step_down(self):
        if self.move(0, 1):
            return True

        self.lock_piece()
        return False
