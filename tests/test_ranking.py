import json
from pathlib import Path
import unittest
from uuid import uuid4

from tetris.rank import Ranking
from tetris.settings import Setting


class RankingTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(__file__).parent / f".ranking-{uuid4().hex}.json"
        self.addCleanup(self.path.unlink, missing_ok=True)
        self.ranking = Ranking(Setting(), path=self.path)

    def test_missing_and_invalid_files_return_empty_ranking(self):
        self.assertEqual(self.ranking.load(), [])

        self.path.write_text("{not-json", encoding="utf-8")

        self.assertEqual(self.ranking.load(), [])

    def test_load_discards_invalid_rows(self):
        self.path.write_text(
            json.dumps(
                [
                    {"name": "Ada", "score": 300},
                    {"name": "", "score": 200},
                    {"name": "Grace", "score": "high"},
                    ["Linus", 100],
                ]
            ),
            encoding="utf-8",
        )

        self.assertEqual(self.ranking.load(), [{"name": "Ada", "score": 300}])

    def test_save_sorts_scores_and_keeps_top_five(self):
        for name, score in [
            ("A", 100),
            ("B", 600),
            ("C", 300),
            ("D", 500),
            ("E", 200),
            ("F", 400),
        ]:
            self.ranking.save(score, name)

        self.assertEqual(
            self.ranking.load(),
            [
                {"name": "B", "score": 600},
                {"name": "D", "score": 500},
                {"name": "F", "score": 400},
                {"name": "C", "score": 300},
                {"name": "E", "score": 200},
            ],
        )

    def test_save_normalizes_player_name(self):
        self.ranking.save(250, "A da-42!")

        self.assertEqual(
            self.ranking.load(),
            [{"name": "Ada42", "score": 250}],
        )

    def test_default_path_is_beside_tetris_module(self):
        ranking = Ranking(Setting())

        self.assertEqual(ranking.path.parent, Path(__file__).parents[1] / "tetris")


if __name__ == "__main__":
    unittest.main()
