import json
import os
from pathlib import Path

LOCALES_PATH = Path(__file__).parent.parent / 'locales'
DEFAULT_LANG = 'en'

class Translator:
    def __init__(self) -> None:
        self.dictionaries: dict[str, dict] = {}
        self._load_langs()

    def _load_langs(self) -> None:
        for file in os.listdir(LOCALES_PATH):
            if file.endswith(".json"):
                lang = os.path.splitext(file)[0]
                with open(LOCALES_PATH / file, "r", encoding="utf-8") as f:
                    self.dictionaries[lang] = json.load(f)

    def translate(self, lang:str, key:str, **kwargs) -> str:
        dictionary = self.dictionaries.get(lang) or self.dictionaries.get(DEFAULT_LANG, {})
        text = dictionary.get(key) or self.dictionaries.get(DEFAULT_LANG, {}).get(key, f"[{key}]")

        if kwargs:
            try:
                return text.format(**kwargs)
            except (KeyError, IndexError):
                return text

        return text