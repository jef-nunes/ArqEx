# project_root/shared/constants.py
from pathlib import Path
from shared.utils import json_read_value

# project root path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# project_root/shared/
ARQEX_SETTINGS_PATH = (PROJECT_ROOT / "data" / "arqex_settings.json").resolve()
# project_root/data/
ARQEX_RELATORY_PATH = (PROJECT_ROOT / "data" / "arqex_relatory.json").resolve()

# skip project directories and files paths
SKIP_PROJECT_PATHS = []
_skip_dir = json_read_value(ARQEX_SETTINGS_PATH,"arqex_skip_project_directories")
_skip_file = json_read_value(ARQEX_SETTINGS_PATH,"arqex_skip_project_files")
for p in _skip_dir + _skip_file:
    _p = PROJECT_ROOT / p
    _p = _p.resolve()
    SKIP_PROJECT_PATHS.append(_p)
SKIP_PROJECT_PATHS = list(set(SKIP_PROJECT_PATHS))
ARQEX_SETTINGS_DEFAULT = {
    "ui_selected_language_code": "en",
    "ui_selected_language_index": 0,
    "arqex_search_base_path": None,
    "arqex_auto_save_relatory": True,
    "arqex_skip_project_directories":["__pycache__","data","shared"],
    "arqex_skip_project_files": ["main.py","arqex_data.py","arqex_stats.py","ui_handler.py","/data/arqex_db.json",
    "/shared/constants.py","/shared/arqex_settings.json", "/shared/utils.py"]
}

# debug
#print(SKIP_PROJECT_PATHS)