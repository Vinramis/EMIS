import json
import os


class JsonTwin:
    def __init__(self, twin_path: str = None):
        self.twin_path: str = twin_path
        self._configuration: dict[str, dict[str]] = {}

        if self.twin_path:
            try:
                with open(self.twin_path, "r", encoding="utf-8") as f:
                    self._configuration = json.load(f)
            except FileNotFoundError:
                self.create_twin_file()
                with open(self.twin_path, "r", encoding="utf-8") as f:
                    self._configuration = json.load(f)

        # # Constants
        # self.ONE_ID_LOGIN_URL = "https://litsey.edu.uz/login"
        # self.ONE_ID_BUTTON_SELECTOR = "#root > div > div > div > main > div > div > a"
        # self.LOGIN_FIELD_PLACEHOLDER = "Loginni kiriting"
        # self.PASSWORD_FIELD_PLACEHOLDER = "Parolni kiriting"
        # self.LOGIN_BUTTON_TEXT = "Kirish"
        # self.SUCCESS_URL = "https://litsey.edu.uz"
        # self.NEW_TOPIC_URL = "https://litsey.edu.uz/teacher/topics/add"

        # # Selectors
        # self.TOPICS_PREFIX = "#topics_"
        # self.TOPIC_NAME_SUFFIX = "_name"
        # self.TOPIC_FILE_SUFFIX = "_topic_file"
        # self.HOMEWORK_FILE_SUFFIX = "_homework_file"
        # self.ADD_LINE_BUTTON = ".Full"

    def get(
        self, section: str = None, key: str = None
    ) -> str | dict[str, str] | dict[str, dict[str]]:
        """
        Returns the value of the configuration item.
        """
        if section:
            if key:
                return self._configuration[section][key]
            return self._configuration[section]
        return self._configuration

    def create_twin_file(self) -> str:
        """
        Creates a new twin file.
        """
        self._configuration = {}
        os.mkdir(os.path.dirname(self.twin_path))
        return self.twin_path

    def sync(self) -> None:
        """
        Syncs the configuration with the twin file.
        """
        with open(self.twin_path, "w", encoding="utf-8") as f:
            json.dump(self._configuration, f, ensure_ascii=False, indent=4)
