from os import system
from pathlib import Path
from shared.constants import *
from shared.type_alias import *
from shared.utils import json_parse, json_read_value, json_dump
from arqex_stats import ArqexStats

logo_ascii_art: List[str] = [
    "     :::         :::::::::       ::::::::       ::::::::::     :::    ::: ",
    "   :+: :+:       :+:    :+:     :+:    :+:      :+:            :+:    :+: ",
    "  +:+   +:+      +:+    +:+     +:+    +:+      +:+             +:+  +:+  ",
    " +#++:++#++:     +#++:++#:      +#+    +:+      +#++:++#         +#++:+   ",
    " +#+     +#+     +#+    +#+     +#+  # +#+      +#+             +#+  +#+  ",
    " #+#     #+#     #+#    #+#     #+#   +#+       #+#            #+#    #+# ",
    " ###     ###     ###    ###      ###### ###     ##########     ###    ### "
    ]

term_style_red = "\033[48;2;20;0;0m\033[38;2;250;0;80m"
term_style_green = "\033[48;2;0;20;0m\033[38;2;0;250;120m"
term_style_blue = "\033[48;2;0;0;20m\033[38;2;0;120;250m"
term_style_reset = "\033[0m"

valid_main_menu_input_options: List[str] = ["0","1","2","3","Q","L"]

def print_logo_ascii_art() -> Void:
    colors = [
        (49, 99, 194),
        (48, 82, 195),
        (54, 60, 199),
        (54, 80, 199),
        (54, 60, 199),
        (48, 82, 195),
        (49, 99, 194)
    ]
    print("\n\n")
    for i in range(0,len(logo_ascii_art)):
        r,g,b = colors[i]
        print(f"   \033[48;2;0;0;20m \033[38;2;{r};{g};{b}m{logo_ascii_art[i]} \033[0m")
    print(f"{term_style_blue}\n\n")

class UserInterface:
    # index of selected language
    language_list: List = ["en","pt_br"]
    # languages codes: en, pt_br...
    selected_language_code: str = json_read_value(ARQEX_SETTINGS_PATH,"ui_selected_language_code")
    # language index on cls.languages list
    selected_language_index: int = json_read_value(ARQEX_SETTINGS_PATH,"ui_selected_language_index")
    # interface texts in each language
    # row: language
    # column: text
    ui_text: Matrix = [["English",
                        "Enter a starting directory path, absolute or relative, without quotes: ",
                        "Invalid path provided, try again: ",
                        "Program started at",
                        "Select menu item by command: ",
                        "Invalid option, try again: ",
                        "Select a language by index: \n 1: Portuguese (BR) \n [Enter]: Keep interface in english, return to main menu"],
                    ["Português brasileiro",
                     "Informe o path de diretorio inicial, absoluto ou relativo, sem aspas: ",
                     "O path fornecido é inválido, tente novamente:",
                     "Programa iniciado em",
                     "Para escolher um item do menu, digite o respectivo comando: ",
                     "Opção inválida, tente novamente: ",
                     "Escolha uma linguagem pelo indice: \n 0: Inglês \n [Enter]: Manter a interface em português, retornar ao menu principal"]]
    @classmethod
    def option_set_language(cls) -> Void:
        language_index = str(input(f"{cls.ui_text[cls.selected_language_index][6]}\n"))
        if language_index is None or len(language_index) is 0:
            cls.main_menu()
            return
        elif str(language_index).isdigit():
            language_index = int(language_index)
            while language_index not in [0,1] and language_index is not None:
                print(cls.ui_text[cls.selected_language_index][5])
                language_index = input(f"{cls.ui_text[cls.selected_language_index][6]}\n")
            if language_index is None or len(str(language_index)) is 0:
                cls.main_menu()
            if language_index < len(cls.language_list):
                try:
                    cls.selected_language_index = language_index
                    cls.selected_language_code = cls.language_list[language_index]
                    _settings = json_parse(ARQEX_SETTINGS_PATH)
                    _settings["ui_selected_language_index"] = cls.selected_language_index
                    _settings["ui_selected_language_code"] = cls.selected_language_code
                    with open(ARQEX_SETTINGS_PATH, 'w') as x:
                        pass
                    json_dump(ARQEX_SETTINGS_PATH,_settings)
                except Exception as e:
                    print(e)
                    json_dump(ARQEX_SETTINGS_PATH, ARQEX_SETTINGS_DEFAULT)
                    exit(1)
            else:
                print("Error - Invalid language")
                exit(1)
            cls.main_menu()
            return

    @classmethod
    def option_new_search(cls):
        starting_path = input(cls.ui_text[cls.selected_language_index][1]).strip()
        while not Path(starting_path).exists():
            starting_path = input(cls.ui_text[cls.selected_language_index][2]).strip()
        ArqexStats.start_new_search(starting_path)

    @classmethod
    def main_menu(cls):
        system("cls || clear")
       # print(cls.selected_language_index)
        print_logo_ascii_art()
        res = term_style_reset
        blue = term_style_blue

        if cls.selected_language_code == "en":

            print(blue)
            # display current settings
            print(f"\n\
             \r\r{res}      {blue}‖{res}   {blue}Interface language: {blue}English{res}\n\
             \r\r{res}      {blue}‖{res}   {blue}Base directory path (new search starts here):{res} {blue}{json_read_value(ARQEX_SETTINGS_PATH,'arqex_search_base_path')}{res}\n\
             \r\r{res}      {blue}‖{res}   {blue}Auto save relatory:{res} {blue}{json_read_value(ARQEX_SETTINGS_PATH,'arqex_auto_save_relatory')}{res}\n\
             \r\r{res}      {blue}‖{res}   {blue}(relatories are saved on \'./data\'){res}")
            print(res)
            # display main menu
            print(f"\n\
            \r\r{res}      {blue}___________________________________________________________________\n\
            \r\r{res}      {blue}|                                                                 |\n\
            \r\r{res}      {blue}|     0 : Select base directory                                   |\n\
            \r\r{res}      {blue}|     1 : Toggle relatory auto saving                             |\n\
            \r\r{res}      {blue}|          (its possible to save manually                         |\n\
            \r\r{res}      {blue}|           the relatory after a new search)                      |\n\
            \r\r{res}      {blue}|                                                                 |\n\
            \r\r{res}      {blue}|     2 : New default search                                      |\n\
            \r\r{res}      {blue}|     3 : New specific search                                     |\n\
            \r\r{res}      {blue}|         (find files with specific name, size and permissions)   |\n\
            \r\r{res}      {blue}|                                                                 |\n\
            \r\r{res}      {blue}|     L : Select language                                         |\n\
            \r\r{res}      {blue}|     Q : Terminate program                                       |\n\
            \r\r{res}      {blue}|_________________________________________________________________|")
            print(res)

        elif cls.selected_language_code == "pt_br":
            print(blue)
            # display current settings
            print(f"\n\
             \r\r{res}      {blue}‖{res}   {blue}Idioma de interface: {blue}Português brasileiro{res}\n\
             \r\r{res}      {blue}‖{res}   {blue}Path do diretório base (utilizado em novas varreduras):{res} {blue}{json_read_value(ARQEX_SETTINGS_PATH,'arqex_search_base_path')}{res}\n\
             \r\r{res}      {blue}‖{res}   {blue}Auto salvar relatório:{res} {blue}{json_read_value(ARQEX_SETTINGS_PATH,'arqex_auto_save_relatory')}{res}\n\
             \r\r{res}      {blue}‖{res}   {blue}(relatórios são salvos em \'./data\'){res}")
            print(res)
            print(f"\n\
            \r\r{res}      {blue}___________________________________________________________________\n\
            \r\r{res}      {blue}|                                                                 |\n\
            \r\r{res}      {blue}|     0 : Selecionar diretório base                               |\n\
            \r\r{res}      {blue}|     1 : Configurar salvamento automático de relatório           |\n\
            \r\r{res}      {blue}|          (existe a possibilidade de salvar manualmente          |\n\
            \r\r{res}      {blue}|           o relatório após uma nova varredura)                  |\n\
            \r\r{res}      {blue}|                                                                 |\n\
            \r\r{res}      {blue}|     2 : Nova varredura padrão                                   |\n\
            \r\r{res}      {blue}|     3 : Nova varredura específica                               |\n\
            \r\r{res}      {blue}|         (encontrar arquivos com nome,                           |\n\
            \r\r{res}      {blue}|          tamanho e permissões específicas)                      |\n\
            \r\r{res}      {blue}|                                                                 |\n\
            \r\r{res}      {blue}|     L : Selecionar idioma                                       |\n\
            \r\r{res}      {blue}|     Q : Encerrar programa                                       |\n\
            \r\r{res}      {blue}|_________________________________________________________________|")
            print(res)

        user_input = str(input(f"\n{res}\t{blue}{cls.ui_text[cls.selected_language_index][4]}{blue}"))
        while user_input not in valid_main_menu_input_options:
            user_input = str(input(f"\n{res}\t{blue}{cls.ui_text[cls.selected_language_index][5]}"))
        print({res})
        if user_input == "2":
            cls.option_new_search()
        elif user_input.upper() == "L":
            cls.option_set_language()


    # Start application interface
    @classmethod
    def start_cli(cls) -> Void:
        system("cls || clear")
        cls.main_menu()
        #cls.option_new_search()
