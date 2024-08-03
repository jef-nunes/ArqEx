from os import system
from pathlib import Path
from shared.type_alias import *

class UserInterface:
    # User interface
    #
    # supported languages 
    LANGUAGES = ["en","pt_br"]
    # index of selected language
    language = 0
    # interface texts in each language
    # row: language
    # column: text
    UI_TEXT: matrix = [["ArqEx",
                        "Enter a starting directory path, absolute or relative, without quotes: ",
                        "Invalid path provided, try again: ",
                        "Program started at"],
                    ["ArqEx",
                     "Informe o path de diretorio inicial, absoluto ou relativo, sem aspas: ",
                     "O path fornecido é inválido, tente novamente:",
                     "Programa iniciado em"]]
    @classmethod
    def set_language(cls, index: int) -> void:
        if cls.LANGUAGES[index] is not None:
            try:
                _settings = settings
                _settings["language"] = cls.LANGUAGES[index]
            except Exception as e:
                print(e)
                exit(1)
            settings = _settings
            cls.language = index
        else:
            print("Error - Invalid language index")

    # Start application interface
    @classmethod
    def start_cli(cls):
        system("cls || clear")
        #print(settings)
        print("\n Arq Explorer \n")
        starting_path = input(cls.UI_TEXT[cls.language][1]).strip()
        while not Path(starting_path).exists():
            starting_path = input(cls.UI_TEXT[cls.language][2]).strip()
        start_new_search(starting_path)
