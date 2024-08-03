from datetime import datetime
from os import listdir, path, system, name as os_name
from pathlib import Path
from pprint import pprint
from typing import Dict, List
from arqex_data import ArqexData
from shared.type_alias import *
from shared.constants import *
import shared.utils as utils

class ArqexStats:
    @classmethod
    def file_properties(cls, path_arq: str) -> Dict[str, any]:
        metadata_dict = utils.fetch_metadata(path_arq)
        size_value, size_unit = utils.get_size_tuple(path_arq)
        size_value = round(size_value, 2)
        fmt_size = f"{size_value} {size_unit}"
        hash = utils.hash_sum(path_arq)
        if os_name == "posix":
            abs_path = Path(path_arq).resolve()
        elif os_name == "nt":
            abs_path = str(Path(path_arq).resolve())
        new_dict = metadata_dict
        if new_dict["creation_time"] is None:
            new_dict["creation_time"] = "?"
        new_dict.update({"size_fmt": fmt_size, "hash": hash, "path_absolute": abs_path})
        return new_dict
    
    @classmethod
    def start_new_search(cls, starting_dir: str = "./")  -> Void:     
        starting_dir = path.abspath(starting_dir)
        directories_to_search: List[str] = [starting_dir]
        found_files: List[str] = []
        print("Program started at {}\n".format(utils.get_time()))
        while directories_to_search:
            current_dir = directories_to_search.pop(0)
            print("Searching files and directories in {}".format(current_dir))
            try:
                for element in listdir(current_dir):
                    element_abs_path = Path(path.join(current_dir, element)).resolve()
                    # is directory
                    if element_abs_path.is_dir():
                        if element_abs_path not in SKIP_PROJECT_PATHS:
                            print("Found a directory at {}".format(element_abs_path))
                            directories_to_search.append(element_abs_path)
                        else:
                            pass
                    # is file
                    else:
                        if element_abs_path not in SKIP_PROJECT_PATHS:
                            found_files.append(element_abs_path)
                        else:
                            pass
            except Exception as e:
                print(f"Error accessing directory {current_dir}: {e}")
        print("\nSearch completed\n")
        relatory_list: List = []
        for file_path in found_files:
            file_property = cls.file_properties(file_path)
            relatory_list.append(file_property)
        ArqexData.update_relatory(relatory_list)