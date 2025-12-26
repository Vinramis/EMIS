import json
import pathlib

class JsonTwin:
    def __init__(self, twin: str | dict | list = None):
        self._configuration = {}
        
        if isinstance(twin, (str, pathlib.Path)):
            # If it's a path, resolve it and load the file
            base_path = pathlib.Path(__file__).parent.resolve()
            self.twin = base_path / twin
            
            try:
                if self.twin.exists():
                    with open(self.twin, "r", encoding="utf-8") as f:
                        self._configuration = json.load(f)
                else:
                    self.create_twin_file()
            except (FileNotFoundError, json.JSONDecodeError):
                self.create_twin_file()
        else:
            # If it's already data (dict/list), just hold it
            self.twin = None 
            self._configuration = twin

    def get(self, key=None):
        if key is None:
            return self._configuration
        
        value = self._configuration[key]
        
        # Only return a new JsonTwin if the value is a dictionary/list
        # If it's a string, int, or bool, return the actual value
        if isinstance(value, (dict, list)):
            return JsonTwin(value)
        return value

    def set(self, section, key, value) -> None:
        if not isinstance(self._configuration, dict):
            raise TypeError("Cannot set a key on a non-dictionary object")
            
        if section not in self._configuration:
            self._configuration[section] = {}
        self._configuration[section][key] = value
        
        # Only sync if this instance is linked to a file
        if self.twin:
            self.sync()

    def create_twin_file(self):
        self._configuration = {}
        if self.twin:
            self.twin.parent.mkdir(parents=True, exist_ok=True)
            self.sync()
        return self.twin

    def sync(self) -> None:
        if self.twin:
            with open(self.twin, "w", encoding="utf-8") as f:
                json.dump(self._configuration, f, ensure_ascii=False, indent=4)