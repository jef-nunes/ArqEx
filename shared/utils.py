from datetime import datetime
from hashlib import sha256
import json
from os import path, stat
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

def json_parse(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def json_dump(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def json_read_value(file_path: str, key: str, default: Optional[Any] = None) -> Any:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(key, default)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return default

def hash_sum(target: str) -> str:
    # print("Hash sum calculation in progress for {}".format(target))
    hash_object = sha256()
    with open(target, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            hash_object.update(block)
    return hash_object.hexdigest()

def get_time() -> str:
    return datetime.now().strftime("%H:%M:%S")

def fmt_datetime(dt: Optional[datetime]) -> str:
    if dt is None:
        return "N/A"
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def fetch_metadata(path_arq: str) -> Dict[str, Optional[any]]:
    try:
        _stat = stat(path_arq)
        new_dict = {
            "name": path.basename(path_arq),
            "size_bytes": _stat.st_size,
            "permissions": oct(_stat.st_mode & 0o777),
            "creation_time": fmt_datetime(datetime.fromtimestamp(_stat.st_ctime)),
            "last_access_time": fmt_datetime(datetime.fromtimestamp(_stat.st_atime)),
            "last_modify_time": fmt_datetime(datetime.fromtimestamp(_stat.st_mtime))
        }

    except Exception as e:
        print(e)
        exit(1)

    return new_dict

def get_size_tuple(target_path: str) -> Tuple[float, str]:
    try:
        size = float(path.getsize(target_path))
    except Exception as e:
        print(e)
        exit(1)
    if size < 1024:
        return size, "bytes"
    elif size < 1024 * 1024:
        return size / 1024, "KB"
    elif size < 1024 * 1024 * 1024:
        return size / (1024 * 1024), "MB"
    else:
        return size / (1024 * 1024 * 1024), "GB"
