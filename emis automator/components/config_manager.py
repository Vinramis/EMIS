import pathlib
from file_utils import noramlize_path

import json
import openpyxl
import sqlite3

class JsonTwin:

    def __init__(self, twin: dict | list | str = None):
        # 1. Initialize core attributes
        self._configuration = None
        self.twin_path = None

        if isinstance(twin, (str, pathlib.Path)):
            # Handle File Paths
            # base_path = pathlib.Path(__file__).parent.resolve()
            # self.twin_path = base_path / twin
            self.twin_path = noramlize_path(twin)
            self._load_from_file()
        elif isinstance(twin, (dict, list)):
            # Handle Raw Data
            self._configuration = twin
        elif twin is None:
            self._configuration = {}

    def _load_from_file(self):
        try:
            if self.twin_path and pathlib.Path(self.twin_path).exists():
                with open(self.twin_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Ensure we are storing the raw dict/list, not a string
                    self._configuration = data if data is not None else {}
            else:
                self.create_twin_file()
        except (json.JSONDecodeError, FileNotFoundError):
            self.create_twin_file()

    def get(self, key=None):
        """
        Safely retrieves a value. If the value is a dict/list, 
        returns a new JsonTwin instance for chaining.
        """
        if key is None:
            return self._configuration
        
        # Ensure we are acting on a dictionary before subscripting
        if not isinstance(self._configuration, dict):
            print(self._configuration)
            return None
            
        value = self._configuration.get(key)
        
        if isinstance(value, (dict, list)):
            return JsonTwin(value)
        return value

    def set(self, section, key, value) -> None:
        if not isinstance(self._configuration, dict):
            self._configuration = {}
            
        if section not in self._configuration:
            self._configuration[section] = {}
            
        self._configuration[section][key] = value
        
        # Only sync if this instance is the root (has a file path)
        if self.twin_path:
            self.sync()

    def create_twin_file(self):
        self._configuration = {}
        if self.twin_path:
            self.twin_path.parent.mkdir(parents=True, exist_ok=True)
            self.sync()

    def sync(self) -> None:
        if self.twin_path:
            with open(self.twin_path, "w", encoding="utf-8") as f:
                json.dump(self._configuration, f, ensure_ascii=False, indent=4)

    def __call__(self, key):
        return self.get(key)

    def __str__(self):
        return str(self._configuration)

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
