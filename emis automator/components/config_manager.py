import pathlib
from typing import Union, Dict, Any
from file_utils import normalize_path

import json
import openpyxl
import sqlite3


class JsonTwin:
    def __init__(self, source: Union[str, pathlib.Path, Dict, 'JsonTwin'] = None, root: 'JsonTwin' = None):
        self._data: Dict = {}
        self._root = root
        self.file_path = None
        self.base_directory = pathlib.Path(__file__).parent

        if isinstance(source, JsonTwin):
            self._data = source._data
            self._root = source
        elif isinstance(source, (str, pathlib.Path)):
            self.file_path = normalize_path(source)
            self._load_or_create()
        elif isinstance(source, dict):
            self._data = source

    def _load_or_create(self):
        """Try to load the file; if missing or corrupt, initialize a new one."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._save()

    def _save(self):
        """Sync to disk if a file path is configured."""
        if self._root:
            self._root._save()
        elif self.file_path:
            # Ensure folder exists before writing
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                print("before")
                json.dump(self._data, f, ensure_ascii=False, indent=4)
                print("after")

    def _concatenate(entries: list) -> dict: # entries=["a", "b", "c", "d", "e"]
        """Makes a nested dictionary from given entries."""
        result = {}
        for i in range(len(entries)):
            result = {entries[i]: result}
        return result

    def get(self, key: str = None) -> Any:
        """
        Retrieves a value. Returns a new JsonTwin for dicts/lists
        to allow chaining (e.g., twin.get('a').get('b')).
        """
        if key is None:
            return self._data

        # safely get value, default to None if _data is not a dict
        val = self._data[key] if isinstance(self._data, dict) else None

        if isinstance(val, (dict, list)):
            return JsonTwin(val)
        return val

    def super_get(self, key: str) -> Any:
        """
        Retrieves a value. Returns a new JsonTwin for dicts.
        """
        if key in self._data.keys():
            return self.get(key)
        for k in self._data.keys():
            if isinstance(self.get(k), JsonTwin):
                return self.get(k).super_get(key)
        return None

    def set(self, key: str, value: Any) -> None:
        """Sets a value."""
        # setdefault creates the section dict if it doesn't exist
        # if isinstance(value, dict):
        #     self._data.setdefault(key, {})
        # else:
        #     self._data.setdefault(key, "")
        self._data[key] = value
        self._save()

    # def super_set(self, keys: list[str], value: Any, entry_autofind: bool = False, current_strike: int = 0, best_strike: int = 0) -> None:
    #     """Sets a value. Creates path if it doesn't exist."""

    #     # if best_strike < current_strike:
    #     #     best_strike = current_strike
    #     # if entry_autofind:
    #     #     entry = self.super_get(keys[0])

    #     if len(keys) == 1:
    #         self.set(keys[0], value)
    #         return
    #     self.set(keys[0], {keys[1]: ""}) 
    #     self.super_set(keys[1:], value)

    def __getitem__(self, key):
        """Allows using twin['key'] syntax."""
        return self.get(key)

    def __call__(self, key):
        """Allows using twin('key') syntax."""
        return self.get(key)

    def __setitem__(self, key, value):
        """Allows using twin['key'] = value syntax."""
        self.set(key, value)

    def to_string(self, beautiful: bool = True, indent: int = 4):
        """Returns a string representation of the JsonTwin."""
        return json.dumps(self._data, indent=indent) if beautiful else str(self._data)

    def to_beautiful_string(self, indent: int = 4):
        """Returns a string representation of the JsonTwin in a beautiful format."""
        return self.to_string(True, indent)

    def __str__(self):
        """Allows using print(twin) syntax."""
        return self.to_string()

    def __dict__(self):
        """Allows using dict(twin) syntax."""
        return self._data


class ExcelTableTwin:
    def __init__(self, twin):
        pass


class DataBaseTwin:
    def __init__(self, twin):
        pass


if __name__ == "__main__":
    # Test
    web = JsonTwin("web.json")
    print(web)
    selectors = web("constants")
    print(selectors)
    print(selectors("One_ID_login_url"))
