from datetime import datetime
from typing import Dict, List
from shared.constants import *
from shared.type_alias import *
import shared.utils as utils

class ArqexData:
    @classmethod
    def clear_relatory(cls) -> Void:
        with open(ARQEX_RELATORY_PATH, 'w') as x:
              pass
    @classmethod
    def update_relatory(cls, search_results: List[Dict[str, any]]) -> Void:
        if not ARQEX_RELATORY_PATH.parent.exists():
                data_dir = ARQEX_RELATORY_PATH.parent
                data_dir.mkdir(parents=True, exist_ok=True)
        if not ARQEX_RELATORY_PATH.is_file():
                ARQEX_RELATORY_PATH.touch()
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        x_key_name = f"search_{timestamp}"
        x_value = search_results
        _dump = {x_key_name: x_value}
        utils.json_dump(ARQEX_RELATORY_PATH, _dump)
        print("Arqex relatory updated")