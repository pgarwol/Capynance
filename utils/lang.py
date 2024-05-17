import configparser
from utils.enums import DBFields
from pathlib import Path
from typing import Optional


def read_lang_file(language: str, section: str) -> dict:
    """
    Reads a language file and returns translations as a dictionary.

    Args:
        language (str): The language code to read translations for.

    Returns:
        dict: A dictionary containing translations for the specified language.

    Raises:
        FileNotFoundError: If the language file is not found.
    """
    translations = {}
    config = configparser.ConfigParser()
    try:
        config.read(
            Path(f"{DBFields.RELATIVE_DB_PATH}lang_{language}.properties"),
            encoding="utf-8",
        )
    except FileNotFoundError:
        config.read(
            Path(f"{DBFields.RELATIVE_DB_PATH}lang_en.properties"),
            encoding="utf-8",
        )
    finally:
        if section in config:
            translations[section] = {}
            for key, value in config[section].items():
                translations[section][key] = value
            print(translations)
            return translations[section]


class Lang:
    default_lang = "pl"  #  TODO: make it "static"

    def __init__(
        self,
        section: str,
        language: Optional[str] = default_lang,
    ):
        self.section = section
        self.translations = read_lang_file(
            language=language, section=self.section.lower()
        )

    def __getitem__(self, key: str):
        _ERROR_MSG = f"???{key}???"
        if isinstance(key, str) and self.translations is not None:
            return (
                self.translations.get(key) if key in self.translations else _ERROR_MSG
            )
        else:
            return _ERROR_MSG

    def change_language(self, language: str):
        self.translations = read_lang_file(
            language=language, section=self.section.lower()
        )
