import os
from pathlib import Path

import pygame


class TetrisUI:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.title_font = self._font(58, bold=True)
        self.heading_font = self._font(26, bold=True)
        self.body_font = self._font(20)
        self.small_font = self._font(16)
        self.number_font = self._font(32, bold=True)

    @staticmethod
    def _font(size, bold=False):
        font_name = "segoeuib.ttf" if bold else "segoeui.ttf"
        font_path = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / font_name
        font = pygame.font.Font(str(font_path) if font_path.exists() else None, size)
        font.set_bold(bold and not font_path.exists())
        return font

    def _text(self, value, font, color=None):
        return font.render(
            str(value),
            True,
            color or self.settings.text,
        )

    def _center_text(self, surface, center):
        self.screen.blit(surface, surface.get_rect(center=center))

    def _card(self, rect, color=None):
        pygame.draw.rect(
            self.screen,
            color or self.settings.panel,
            rect,
            border_radius=self.settings.card_radius,
        )
        pygame.draw.rect(
            self.screen,
            self.settings.border,
            rect,
            width=1,
            border_radius=self.settings.card_radius,
        )

    def _draw_block(self, x, y, color, size=None):
        block_size = size or self.settings.block_size
        rect = pygame.Rect(x + 2, y + 2, block_size - 4, block_size - 4)
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        highlight = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, 3)
        pygame.draw.rect(
            self.screen,
            tuple(min(channel + 28, 255) for channel in color),
            highlight,
            border_radius=2,
        )

    def draw_main_menu(self):
        self.screen.fill(self.settings.background)
        center_x = self.settings.total_screen_width // 2

        eyebrow = self._text("A MODERN CLASSIC", self.small_font, self.settings.accent)
        self._center_text(eyebrow, (center_x, 150))
        self._center_text(self._text("TETRIS", self.title_font), (center_x, 205))
        subtitle = self._text(
            "Build clean lines. Keep moving.",
            self.body_font,
            self.settings.text_muted,
        )
        self._center_text(subtitle, (center_x, 252))

        menu_rect = pygame.Rect(center_x - 150, 300, 300, 190)
        self._card(menu_rect)
        options = [
            ("1", "Start Game"),
            ("2", "Ranking"),
            ("3", "Quit"),
        ]
        for index, (key, label) in enumerate(options):
            y = menu_rect.y + 35 + index * 52
            badge = pygame.Rect(menu_rect.x + 24, y - 14, 32, 32)
            pygame.draw.rect(
                self.screen,
                self.settings.panel_highlight,
                badge,
                border_radius=8,
            )
            self._center_text(
                self._text(key, self.small_font, self.settings.accent),
                badge.center,
            )
            self.screen.blit(
                self._text(label, self.body_font),
                (menu_rect.x + 72, y - 10),
            )

        hint = self._text(
            "Use number keys to select",
            self.small_font,
            self.settings.text_muted,
        )
        self._center_text(hint, (center_x, 535))

    def draw_game(self, core, paused=False):
        self.screen.fill(self.settings.background)
        self._draw_board(core)
        self._draw_sidebar(core)

        if paused:
            self._draw_overlay(
                "PAUSED",
                "Press Space to continue",
                self.settings.accent,
            )
        elif core.game_over:
            self._draw_overlay(
                "GAME OVER",
                f"Score {core.score}  |  R Restart  M Save  Q Quit",
                self.settings.danger,
            )

    def _draw_board(self, core):
        board_rect = pygame.Rect(
            self.settings.board_x,
            self.settings.board_y,
            self.settings.board_width,
            self.settings.board_height,
        )
        pygame.draw.rect(
            self.screen,
            self.settings.board_background,
            board_rect,
            border_radius=8,
        )

        for row in range(self.settings.grid_height + 1):
            y = self.settings.board_y + row * self.settings.block_size
            pygame.draw.line(
                self.screen,
                self.settings.grid_line,
                (self.settings.board_x, y),
                (self.settings.board_x + self.settings.board_width, y),
            )
        for column in range(self.settings.grid_width + 1):
            x = self.settings.board_x + column * self.settings.block_size
            pygame.draw.line(
                self.screen,
                self.settings.grid_line,
                (x, self.settings.board_y),
                (x, self.settings.board_y + self.settings.board_height),
            )

        for row_index, row in enumerate(core.grid):
            for column_index, color_index in enumerate(row):
                if color_index:
                    self._draw_grid_block(
                        column_index,
                        row_index,
                        self.settings.block_colors[color_index - 1],
                    )

        if not core.game_over:
            color = self.settings.block_colors[core.current_color - 1]
            for row_index, row in enumerate(core.current_shape):
                for column_index, cell in enumerate(row):
                    if cell:
                        self._draw_grid_block(
                            core.current_x + column_index,
                            core.current_y + row_index,
                            color,
                        )

        pygame.draw.rect(
            self.screen,
            self.settings.border,
            board_rect,
            width=2,
            border_radius=8,
        )

    def _draw_grid_block(self, column, row, color):
        if row < 0:
            return
        self._draw_block(
            self.settings.board_x + column * self.settings.block_size,
            self.settings.board_y + row * self.settings.block_size,
            color,
        )

    def _draw_sidebar(self, core):
        x = self.settings.sidebar_x
        width = self.settings.sidebar_width

        preview_rect = pygame.Rect(x, 20, width, 178)
        self._card(preview_rect)
        self.screen.blit(
            self._text("NEXT", self.small_font, self.settings.text_muted),
            (x + 16, 36),
        )
        self._draw_preview(core.next_shape, core.next_color, preview_rect)

        stats_rect = pygame.Rect(x, 214, width, 126)
        self._card(stats_rect)
        self.screen.blit(
            self._text("SCORE", self.small_font, self.settings.text_muted),
            (x + 16, 230),
        )
        self.screen.blit(
            self._text(core.score, self.number_font),
            (x + 16, 250),
        )
        level_label = self._text(
            f"LEVEL  {core.level}",
            self.small_font,
            self.settings.accent,
        )
        self.screen.blit(level_label, (x + 16, 306))

        controls_rect = pygame.Rect(x, 356, width, 264)
        self._card(controls_rect)
        self.screen.blit(
            self._text("CONTROLS", self.small_font, self.settings.text_muted),
            (x + 16, 372),
        )
        controls = [
            ("←  →", "Move"),
            ("↑", "Rotate"),
            ("↓", "Soft drop"),
            ("Space", "Pause"),
        ]
        for index, (key, label) in enumerate(controls):
            y = 414 + index * 46
            self.screen.blit(
                self._text(key, self.small_font, self.settings.text),
                (x + 16, y),
            )
            self.screen.blit(
                self._text(label, self.small_font, self.settings.text_muted),
                (x + 86, y),
            )

    def _draw_preview(self, shape, color_index, rect):
        cell_size = 24
        shape_width = len(shape[0]) * cell_size
        shape_height = len(shape) * cell_size
        start_x = rect.centerx - shape_width // 2
        start_y = rect.y + 100 - shape_height // 2
        color = self.settings.block_colors[color_index - 1]

        for row_index, row in enumerate(shape):
            for column_index, cell in enumerate(row):
                if cell:
                    self._draw_block(
                        start_x + column_index * cell_size,
                        start_y + row_index * cell_size,
                        color,
                        size=cell_size,
                    )

    def draw_ranking(self, rankings):
        self.screen.fill(self.settings.background)
        center_x = self.settings.total_screen_width // 2
        self._center_text(self._text("TOP SCORES", self.heading_font), (center_x, 82))
        subtitle = self._text(
            "Your five best local games",
            self.small_font,
            self.settings.text_muted,
        )
        self._center_text(subtitle, (center_x, 116))

        card = pygame.Rect(center_x - 190, 150, 380, 330)
        self._card(card)
        if not rankings:
            empty = self._text(
                "No scores yet",
                self.body_font,
                self.settings.text_muted,
            )
            self._center_text(empty, card.center)
        else:
            for index, entry in enumerate(rankings):
                y = card.y + 42 + index * 55
                rank_color = self.settings.accent if index == 0 else self.settings.text_muted
                self.screen.blit(
                    self._text(f"{index + 1:02}", self.small_font, rank_color),
                    (card.x + 28, y),
                )
                self.screen.blit(
                    self._text(entry["name"], self.body_font),
                    (card.x + 82, y - 4),
                )
                score = self._text(entry["score"], self.body_font)
                self.screen.blit(score, (card.right - 28 - score.get_width(), y - 4))

        hint = self._text(
            "Press M to return to menu",
            self.small_font,
            self.settings.text_muted,
        )
        self._center_text(hint, (center_x, 535))

    def _draw_overlay(self, title, subtitle, color):
        overlay = pygame.Surface(
            (self.settings.total_screen_width, self.settings.screen_height),
            pygame.SRCALPHA,
        )
        overlay.fill(self.settings.overlay)
        self.screen.blit(overlay, (0, 0))

        center_x = self.settings.total_screen_width // 2
        card = pygame.Rect(center_x - 215, 235, 430, 170)
        self._card(card, self.settings.panel)
        self._center_text(self._text(title, self.heading_font, color), (center_x, 285))
        self._center_text(
            self._text(subtitle, self.small_font, self.settings.text_muted),
            (center_x, 345),
        )

    def draw_name_prompt(self, name, score):
        self.screen.fill(self.settings.background)
        center_x = self.settings.total_screen_width // 2
        self._center_text(
            self._text("SAVE YOUR SCORE", self.heading_font),
            (center_x, 185),
        )
        self._center_text(
            self._text(f"Score {score}", self.body_font, self.settings.text_muted),
            (center_x, 225),
        )

        card = pygame.Rect(center_x - 180, 275, 360, 130)
        self._card(card)
        self.screen.blit(
            self._text("NAME · MAX 6", self.small_font, self.settings.text_muted),
            (card.x + 24, card.y + 20),
        )
        display_name = name or "_"
        self.screen.blit(
            self._text(display_name, self.number_font, self.settings.accent),
            (card.x + 24, card.y + 55),
        )
        hint = self._text(
            "Enter to save  |  Backspace to edit",
            self.small_font,
            self.settings.text_muted,
        )
        self._center_text(hint, (center_x, 455))
