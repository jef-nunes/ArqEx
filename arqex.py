import platform
#import time
#from datetime import datetime
#from hashlib import sha256
from os import listdir, path, system #, stat
from pathlib import Path
from pprint import pprint
from typing import Dict, List #, Tuple, Optional
from project_utils import *

ARQEX_DB_PATH = "arqex_db.json"
DEFAULT_SETTINGS = {
        "language":"en",
        "arq_skip_directories":["__pycache__"],
        "arq_skip_files": ["settings.json", "project_utils.py", "arqex.py"]
    }

settings: Dict = {}

def reset_settings():
    global settings
    settings = DEFAULT_SETTINGS

def load_settings():
    global settings
    _source = "settings.json"
    language: str = json_read_value(_source,"language")
    arq_skip_directories: List[str] = json_read_value(_source,"arq_skip_directories")
    arq_skip_files: List[str] = json_read_value(_source,"arq_skip_files")
    settings.update({"language":language, "skip_directories":arq_skip_directories, "skip_files":arq_skip_files})

def update_database(search_results: List):
    is_empty = False
    # if arqex_db.json not found
    # create a new file
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
        json_dump(ARQEX_DB_PATH, _dump)
    else:
        old_database: Dict = json_parse(ARQEX_DB_PATH)
        new_database: Dict = old_database
        new_database.update({x_key_name:x_value})
        json_dump(ARQEX_DB_PATH, new_database)
    print("Arqex database updated")

def get_file_properties(path_arq: str) -> Dict[str, any]:
    metadata_dict = fetch_metadata(path_arq)
    size_value, size_unit = get_size_tuple(path_arq)
    size_value = round(size_value, 2)
    fmt_size = f"{size_value} {size_unit}"
    hash = hash_sum(path_arq)
    abs_path = path.abspath(path_arq)
    new_dict = metadata_dict
    if new_dict["creation_time"] is None:
        new_dict["creation_time"] = "?"
    new_dict.update({"size_fmt": fmt_size, "hash": hash, "path_absolute": abs_path})
    return new_dict
    
def start_new_search(starting_dir: str = "./") -> None:
    
    starting_dir = path.abspath(starting_dir)
    directories_to_search: List[str] = [starting_dir]

    found_files: List[str] = []

    print("Program started at {}\n".format(get_time()))

    while directories_to_search:
        current_dir = directories_to_search.pop(0)
        print("Searching archives and directories in {}".format(current_dir))

        try:
            # List all items in the directory
            for element in listdir(current_dir):
                element_abs_path = path.join(current_dir, element)
            #  print(f"Element: {element}, Abs path: {element_abs_path}")
                # is directory?
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
     #   print("\n")
     #   pprint(rel)
    update_database(relatory)

def start_cli():
    system("cls || clear")
    #print(settings)
    print("\n Arq Explorer \n")
    print("")
    starting_path = input("Enter a starting path (absolute or relative) without quotes: ").strip()
    while not Path(starting_path).exists():
        starting_path = input("Invalid path provided, try again: ").strip()
    start_new_search(starting_path)

if __name__ == "__main__":
    if platform.system() != "Linux":
        print("Error: This app is only supported on Linux")
        exit(1)
    else:
        load_settings()
        start_cli()
