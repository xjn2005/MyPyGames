import json
from pathlib import Path


class Ranking:
    def __init__(self, settings, path=None):
        self.settings = settings
        self.path = (
            Path(path)
            if path is not None
            else Path(__file__).resolve().parent / settings.ranking_file
        )

    @staticmethod
    def normalize_name(name):
        return "".join(character for character in str(name) if character.isalnum())[:6]

    def load(self):
        try:
            raw_rankings = json.loads(self.path.read_text(encoding="utf-8"))
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            return []

        if not isinstance(raw_rankings, list):
            return []

        rankings = []
        for entry in raw_rankings:
            if not isinstance(entry, dict):
                continue

            name = entry.get("name")
            score = entry.get("score")
            if not isinstance(name, str) or type(score) is not int:
                continue

            normalized_name = self.normalize_name(name)
            if not normalized_name:
                continue
            rankings.append({"name": normalized_name, "score": score})

        rankings.sort(key=lambda entry: entry["score"], reverse=True)
        return rankings[: self.settings.max_ranking]

    def save(self, new_score, new_name):
        name = self.normalize_name(new_name)
        if not name:
            raise ValueError("Player name must contain a letter or number.")

        rankings = self.load()
        rankings.append({"name": name, "score": int(new_score)})
        rankings.sort(key=lambda entry: entry["score"], reverse=True)
        rankings = rankings[: self.settings.max_ranking]

        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(f"{self.path.suffix}.tmp")
        temporary_path.write_text(
            json.dumps(rankings, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary_path.replace(self.path)
