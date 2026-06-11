class Setting:
    def __init__(self):
        # Game rules
        self.block_size = 30
        self.grid_width = 10
        self.grid_height = 20
        self.fps = 60
        self.level_threshold = [0, 1000, 2500, 5000, 10000, 20000]
        self.level_speed = [500, 400, 300, 200, 150, 100]
        self.ranking_file = "tetris_ranking.json"
        self.max_ranking = 5

        self.block_shapes = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[0, 1, 0], [1, 1, 1]],
            [[0, 0, 1], [1, 1, 1]],
            [[1, 0, 0], [1, 1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [0, 1, 1]],
        ]

        # Layout
        self.outer_padding = 20
        self.board_x = 24
        self.board_y = 20
        self.board_width = self.grid_width * self.block_size
        self.board_height = self.grid_height * self.block_size
        self.sidebar_x = 344
        self.sidebar_width = 180
        self.screen_width = self.board_width
        self.screen_height = 640
        self.total_screen_width = 548
        self.card_radius = 14
        self.card_padding = 16

        # Modern dark palette
        self.background = (9, 11, 16)
        self.board_background = (17, 21, 29)
        self.panel = (23, 28, 38)
        self.panel_highlight = (31, 38, 51)
        self.text = (245, 247, 250)
        self.text_muted = (152, 162, 179)
        self.accent = (76, 141, 255)
        self.danger = (255, 93, 104)
        self.grid_line = (37, 44, 56)
        self.border = (49, 58, 73)
        self.overlay = (4, 6, 10, 210)

        self.block_colors = [
            (79, 209, 197),
            (246, 200, 95),
            (167, 139, 250),
            (245, 158, 91),
            (91, 143, 249),
            (92, 203, 138),
            (241, 109, 122),
        ]

        # Compatibility aliases for small external integrations.
        self.black = self.background
        self.white = self.text
        self.gray = self.text_muted
        self.light_gray = self.grid_line
        self.border_color = self.border
        self.red = self.danger
        self.blue = self.accent
