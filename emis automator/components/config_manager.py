import pathlib
import collections.abc
from typing import Union, Any
from file_utils import normalize_path
from data_utils import compare_two_words

import json
# import openpyxl
# import sqlite3


class JsonTwin:
    def __init__(self, source: Union[str, pathlib.Path, dict, list, 'JsonTwin'] = None, root: 'JsonTwin' = None):
        self._data: dict | list = None
        self._root: JsonTwin = root
        self.file_path: str = None
        # self.base_directory = pathlib.Path(__file__).parent

        if isinstance(source, JsonTwin):
            self._data = source._data
            if not self._root:
                self._root = source
        elif isinstance(source, Union[str, pathlib.Path]):
            self.file_path = normalize_path(source)
            self._load_or_create()
        elif isinstance(source, Union[dict, list]):
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
        if self.file_path:
            # Ensure folder exists before writing
            # self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=4)

    def get(self, key: Union[str, int] = None, strict: bool = False) -> Any:
        """
        Retrieves a value. Returns a new JsonTwin for dicts/lists
        to allow chaining (e.g., twin.get('a').get('b')).
        """
        if key is None:
            return self._data
        if not isinstance(self._data, collections.abc.Iterable):
            return None

        result: Any = None
        if isinstance(self._data, dict):
            if key in self._data.keys():
                result = self._data[key]

            if not strict and not result:
                for k in self._data.keys():
                    if compare_two_words(key, k):
                        result = self._data[k]
        elif isinstance(self._data, list):
            if key in range(len(self._data)):
                result = self._data[key]

        if isinstance(result, (dict, list)):
            result = JsonTwin(result, self)

        return result

    def super_get(self, key: Union[str, int]) -> Any:
        """
        Retrieves a value. Key is searched across all JsonTwin. Returns a new JsonTwin for dicts.
        """
        if isinstance(self._data, dict):
            if key in self._data.keys():
                return self.get(key)
            for k in self._data.keys():
                if isinstance(self.get(k), JsonTwin):
                    return self.get(k).super_get(key)

        if isinstance(self._data, list) and isinstance(key, int):
            if key < len(self._data):
                return self.get(key)
            for k in range(len(self._data)+1):
                if isinstance(self.get(k), JsonTwin):
                    return self.get(k).super_get(key)
        return None

    def set(self, key: Union[str, int], value: Any, autosave: bool = True) -> None:
        """Sets a value."""
        # setdefault creates the section dict if it doesn't exist
        if not self._data:
            if isinstance(key, int):
                self._data = []
            else:
                self._data = {}
        if isinstance(self._data, dict):
            if isinstance(value, dict):
                self._data.setdefault(key, {})
            elif isinstance(value, list):
                self._data.setdefault(key, [])
            else:
                self._data.setdefault(key, "")
        elif isinstance(self._data, list):
            if len(self._data) <= key:
                self._data.append(value)

        self._data[key] = value
        if autosave:
            self._save()

    def super_set(self, keys: list[str], value: Any) -> None:
        if not keys:
            return
    
        if len(keys) == 1:
            self.set(keys[0], value, autosave=False)
        else:
            # 1. Ensure the next level is a dictionary without wiping existing data
            if keys[0] not in self._data or not isinstance(self._data[keys[0]], dict):
                self._data[keys[0]] = {}
            
            # 2. Get the next level as a Twin so it can handle the next recursion
            next_level: JsonTwin = self.get(keys[0])
            next_level.super_set(keys[1:], value)

    def pull(self, source: 'JsonTwin' | dict, autosave: bool = True) -> None:
        try:
            self._data = source._data
        except AttributeError:
            self._data = source
        self._save() if autosave else None

    def keys(self):
        return self._data.keys()

    def super_keys(self):
        raw_keys = self.keys()
        current_layer_keys: set[str] = set(raw_keys)
        all_keys: set[str] = current_layer_keys.copy()

        for k in current_layer_keys:
            if isinstance(self.get(k), JsonTwin):
                all_keys.update(self.get(k).super_keys())

        return all_keys

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


# class ExcelTableCopy():
#     def __init__(self, source: Union[str, pathlib.Path], sheet_identifier: Union[str, int] = None):
#         self.file_path: str = str(source)
#         self._sheet_identifier: Union[str, int] = sheet_identifier
#         self.sheet_name: str = None
#         self.sheet_index: int = None
#         self._workbook: openpyxl.Workbook = None
#         self._data: list[list] = [] # for future use of A1, B1, A2 syntax

#         if self._sheet_identifier:
#             if isinstance(self._sheet_identifier, int):
#                 self.sheet_index = self._sheet_identifier
#                 self.sheet_name = self._workbook.sheetnames[self._sheet_identifier]
#             else:
#                 self.sheet_name = self._sheet_identifier
#                 self.sheet_index = self._workbook.sheetnames.index(self._sheet_identifier)
#         else:
#             self.sheet_index = 0
#             self.sheet_name = self._workbook.sheetnames[0]

#     def _load(self):
#         try:
#             self._workbook = openpyxl.load_workbook(self.file_path)
#         except FileNotFoundError:
#             self._workbook = openpyxl.Workbook()

#         # Map sheet names to data keys
#         self._data = [name for name in self._workbook.sheetnames]

#     def _load_sheet_data(self):
#         """Converts a sheet's rows into a list of dictionaries."""
#         sheet = self._workbook[self.sheet_name]
#         headers = [cell.value for cell in sheet[1]]
#         data = []
#         for row in sheet.iter_rows(min_row=2, values_only=True):
#             data.append(dict(zip(headers, row)))
#         self._data = data

#     def get(self, full_cell_address: str = None, row_index: int = None, column_index: int = None) -> Any:
#         """Returns the value of a cell."""
#         if full_cell_address:
#             return self._workbook[self.sheet_name][full_cell_address].value
#         if row_index and column_index:
#             return self._workbook[self.sheet_name][row_index][column_index].value
#         return None

#     def set(self, sheet_name: str, data: List[Dict[str, Any]], autosave: bool = True):
#         """Expects a list of dicts to write to a sheet."""
#         if sheet_name not in self._workbook.sheetnames:
#             self._workbook.create_sheet(sheet_name)
        
#         sheet = self._workbook[sheet_name]
#         sheet.delete_rows(1, sheet.max_row) # Clear existing

#         if data:
#             headers = list(data[0].keys())
#             sheet.append(headers)
#             for row in data:
#                 sheet.append([row.get(h) for h in headers])
        
#         if autosave:
#             self._save()

#     def __getitem__(self, key): return self.get(key)


# class DataBaseTwin:
#     def __init__(self, twin):
#         pass


# if __name__ == "__main__":

    # path: str = "test.json"
    # twin = JsonTwin(path)
    # print(twin.super_keys())

    # path: str = "test.json"
    # twin0 = JsonTwin(path)
    # twin1 = twin0("1_test_data")
    # twin1.super_set(["constants", "One_ID_login_url", "ultra scope", "pen the penguin"], "https://one.id")
    # twin2 = twin1("1_2_test_data")
    # twin2.super_set(["constants", "One_ID_login_url"], "https://one.id")

    # twin1._save()
    # print(twin0.file_path)
    # print(twin0.to_beautiful_string())
    # print(twin1.to_beautiful_string())
    # print(twin2.to_beautiful_string())