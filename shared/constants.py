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



UI_LANGUAGES = ["en","pt_br"]

UI_TEXT = [["ArqEx",
                        "Enter a starting directory path, absolute or relative, without quotes: ",
                        "Invalid path provided, try again: ",
                        "Program started at"],
                    ["ArqEx",
                     "Informe o path de diretorio inicial, absoluto ou relativo, sem aspas: ",
                     "O path fornecido é inválido, tente novamente:",
                     "Programa iniciado em"]]

ARQEX_SETTINGS_DEFAULT = {
        "language":"en",
        "arq_skip_directories":["__pycache__"],
        "arq_skip_files": ["settings.json", "project_utils.py", "arqex.py"]
    }

# debug
#print(SKIP_PROJECT_PATHS)