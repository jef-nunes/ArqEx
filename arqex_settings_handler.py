from typing import Dict
from shared.constants import *
from shared.type_alias import *
import shared.utils as utils

# arqex_settings: Dict = {}
#
# def load_settings() -> Void:
#    global arqex_settings
#    arqex_settings = utils.json_parse(ARQEX_SETTINGS_PATH)

def reset_to_default() -> Void:
    with open(ARQEX_SETTINGS_PATH, 'w') as x:
        pass
    utils.json_dump(ARQEX_SETTINGS_PATH,ARQEX_SETTINGS_DEFAULT)

def set_variable(key:str,value:any) -> Void:
    _settings = utils.json_parse(ARQEX_SETTINGS_PATH)
    if key in _settings:
        _settings.update({f"{key}":value})
        # erase old settings
        with open(ARQEX_SETTINGS_PATH, 'w') as x:
                pass
        # dump updated settings
        utils.json_dump(ARQEX_SETTINGS_PATH, _settings)
    else:
         print("Error on set_user_variable: Invalid key provided")
         exit(1)
    