import json
import os

class Translator:
    def __init__(self, default_lang = "en"):
        self.current_lang = default_lang
        self.dictionaries = {}
        self._load_langs()

    def _load_langs(self):
        locales_path =  "locales"

        for file in os.listdir(locales_path):
            if file.endswith(".json"):
                lang = file.split('.')[0]
                with open(f"{locales_path}/{file}", "r", encoding="utf-8") as f:
                    self.dictionaries[lang] = json.load(f)

    def switch_lang(self, new_lang):
        if new_lang in self.dictionaries:
            self.current_lang = new_lang
        else:
            raise ValueError(f"Language {new_lang} not supported yet.")

    def _(self, key, **kwargs):
        dictionary = self.dictionaries.get(self.current_lang, {})

        text = dictionary.get(key, f"[{key}]")

        if kwargs:
            return text.format(**kwargs)

        return text

_instance = Translator()

_ = _instance._
switch_lang = _instance.switch_lang