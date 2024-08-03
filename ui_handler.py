from os import system
from pathlib import Path
from shared.constants import *
from shared.type_alias import *
from shared.utils import json_parse, json_read_value
from arqex_stats import ArqexStats

class UserInterface:
    # index of selected language
    language_list: List = UI_LANGUAGES
    # languages codes: en, pt_br...
    selected_language_code: str = json_read_value(ARQEX_SETTINGS_PATH,"selected_language_code")
    # language index on cls.languages list
    selected_language_index: int = language_list.index(json_read_value(ARQEX_SETTINGS_PATH,"selected_language_code"))
    # interface texts in each language
    # row: language
    # column: text
    ui_text: Matrix = UI_TEXT
    @classmethod
    def set_language(cls, language_code: int) -> Void:
        if language_code not in cls.language_list:
            try:
                cls.selected_language_code = language_code
                cls.selected_language_index = cls.language_list.index(language_code)
                _settings = json_parse(ARQEX_SETTINGS_PATH)
                _settings["selected_language_code"] = language_code
            except Exception as e:
                print(e)
                exit(1)
            settings = _settings
            cls.language = language_code
        else:
            print("Error - Invalid language index")

    @classmethod
    def option_new_search(cls):
        starting_path = input(cls.ui_text[cls.selected_language_index][1]).strip()
        while not Path(starting_path).exists():
            starting_path = input(cls.ui_text[cls.selected_language_index][2]).strip()
        ArqexStats.start_new_search(starting_path)

    @classmethod
    def main_menu(cls):
        print("\n Arq Explorer \n")

    # Start application interface
    @classmethod
    def start_cli(cls) -> Void:
        system("cls || clear")
        #cls.main_menu()
        cls.option_new_search()
