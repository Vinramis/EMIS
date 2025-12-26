import json
import pathlib


class JsonTwin:
    def __init__(self, twin: str | dict = None):
        if isinstance(twin, str):
            base_path = pathlib.Path(__file__).parent.resolve()
            self.twin = base_path / twin
        else:
            self.twin = twin
        self._configuration = {}

        if isinstance(self.twin, str):
            try:
                with open(self.twin, "r", encoding="utf-8") as f:
                    self._configuration = json.load(f)
            except FileNotFoundError:
                self.create_twin_file()
                with open(self.twin, "r", encoding="utf-8") as f:
                    self._configuration = json.load(f)
        else:
            self._configuration = twin

    def get(self, key=None):
        """
        Returns the value of the configuration item.
        """
        if key:
            return JsonTwin(self._configuration[key])
        return self._configuration

    def set(self, section, key, value) -> None:
        """
        Sets the value of the configuration item.
        """
        if section not in self._configuration:
            self._configuration[section] = {}
        self._configuration[section][key] = value
        self.sync()

    def create_twin_file(self) -> str:
        """
        Creates a new twin file.
        """
        self._configuration = {}
        pathlib.Path(self.twin).parent.mkdir(parents=True, exist_ok=True)
        return self.twin

    def sync(self) -> None:
        """
        Syncs the configuration with the twin file.
        """
        with open(self.twin, "w", encoding="utf-8") as f:
            json.dump(self._configuration, f, ensure_ascii=False, indent=4)
