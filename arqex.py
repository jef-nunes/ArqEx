from datetime import datetime
from os import listdir, path, system
from pathlib import Path
from types import NoneType
from typing import Dict, List
from shared.type_alias import *
from shared.constants import *
import shared.utils as utils

settings: Dict = {}

def reset_settings() -> void:
    global settings
    settings = DEFAULT_SETTINGS

def load_settings() -> void:
    global settings
    try:
        _source = ARQEX_DB_PATH
        _settings: Dict = utils.json_parse(_source)
    except Exception as e:
        print(e)
        exit(1)
    settings = _settings

def update_database(search_results: List) -> void:
    is_empty = False
    if not path.isfile(ARQEX_DB_PATH):
        is_empty = True
        with open(ARQEX_DB_PATH, 'w') as file:
            pass
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    x_key_name = f"search_{timestamp}"
    x_value = search_results
    _dump = {x_key_name:x_value}
    if is_empty:
        utils.json_dump(ARQEX_DB_PATH, _dump)
    else:
        old_database: Dict = utils.json_parse(ARQEX_DB_PATH)
        new_database: Dict = old_database
        new_database.update({x_key_name:x_value})
        utils.json_dump(ARQEX_DB_PATH, new_database)
    print("Arqex database updated")

def get_file_properties(path_arq: str) -> Dict[str, any]:
    metadata_dict = utils.fetch_metadata(path_arq)
    size_value, size_unit = utils.get_size_tuple(path_arq)
    size_value = round(size_value, 2)
    fmt_size = f"{size_value} {size_unit}"
    hash = utils.hash_sum(path_arq)
    abs_path = path.abspath(path_arq)
    new_dict = metadata_dict
    if new_dict["creation_time"] is None:
        new_dict["creation_time"] = "?"
    new_dict.update({"size_fmt": fmt_size, "hash": hash, "path_absolute": abs_path})
    return new_dict
    
def start_new_search(starting_dir: str = "./")  -> void:
    
    starting_dir = path.abspath(starting_dir)
    directories_to_search: List[str] = [starting_dir]

    found_files: List[str] = []

    print("Program started at {}\n".format(utils.get_time()))

    while directories_to_search:
        current_dir = directories_to_search.pop(0)
        print("Searching archives and directories in {}".format(current_dir))

        try:
            for element in listdir(current_dir):
                element_abs_path = path.join(current_dir, element)
                if Path(element_abs_path).is_dir():
                    if all(x not in settings["skip_directories"] for x in (element, element_abs_path)):
                        print("Found a directory at {}".format(element_abs_path))
                        directories_to_search.append(element_abs_path)
                else:
                    if all(x not in settings["skip_files"] for x in (element, element_abs_path)):
                        found_files.append(element_abs_path)
        except Exception as e:
            print(f"Error accessing directory {current_dir}: {e}")
    print("\nSearch completed\n")
    relatory: List = []

    for file_path in found_files:
        file_property = get_file_properties(file_path)
        relatory.append(file_property)
    update_database(relatory)
