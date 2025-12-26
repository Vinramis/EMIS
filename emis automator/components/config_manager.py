
import json
import os

class ConfigManager:
    def __init__(self, config_path='config.json'):
        self.origin_config_path = config_path

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.configuration = json.load(f)
        except FileNotFoundError:
            # If config.json doesn't exist, create it
            self.create_config()
        # except json.JSONDecodeError:
        #     # If config.json is invalid, create it
        #     self.create_config()

        # Credentials
        self.credentials = self.get("credentials")
        self.LOGIN = self.credentials.get("login")
        self.PASSWORD = self.credentials.get("password")
        self.VALIDITY = self.credentials.get("validity")

        # Automation Settings
        self.automation_settings = self.get("automation_settings")
        self.TOPICS_FILE_PATH = self.automation_settings.get("TOPICS_FILE_PATH")
        self.INPUT_DATA_DB_PATH = self.automation_settings.get("INPUT_DATA_DB_PATH")
        self.CLASSWORK_FOLDER = self.automation_settings.get("CLASSWORK_FOLDER")
        self.HOMEWORK_FOLDER = self.automation_settings.get("HOMEWORK_FOLDER")
        self.START_CELL = self.automation_settings.get("START_CELL")
        self.START_FROM_LINE = self.automation_settings.get("START_FROM_LINE")
        self.END_ON_LINE = self.automation_settings.get("END_ON_LINE")
        self.MODE = self.automation_settings.get("MODE")

        # Constants
        self.ONE_ID_LOGIN_URL = "https://litsey.edu.uz/login"
        self.ONE_ID_BUTTON_SELECTOR = "#root > div > div > div > main > div > div > a"
        self.LOGIN_FIELD_PLACEHOLDER = "Loginni kiriting"
        self.PASSWORD_FIELD_PLACEHOLDER = "Parolni kiriting"
        self.LOGIN_BUTTON_TEXT = "Kirish"
        self.SUCCESS_URL = "https://litsey.edu.uz"
        self.NEW_TOPIC_URL = "https://litsey.edu.uz/teacher/topics/add"
        
        # Selectors
        self.TOPICS_PREFIX = "#topics_"
        self.TOPIC_NAME_SUFFIX = "_name"
        self.TOPIC_FILE_SUFFIX = "_topic_file"
        self.HOMEWORK_FILE_SUFFIX = "_homework_file"
        self.ADD_LINE_BUTTON = ".Full"

    def get(self, section, key=None):
        if key:
            return self.configuration[section][key]
        return self.configuration[section]

    def create_config(self):
        self.configuration = {
            "credentials": {
                "login": "",
                "password": "",
                "validity": 0
            },
            "automation_settings": {
                "TOPICS_FILE_PATH": "",
                "INPUT_DATA_DB_PATH": "",
                "CLASSWORK_FOLDER": "",
                "HOMEWORK_FOLDER": "",
                "START_CELL": "",
                "START_FROM_LINE": 0,
                "END_ON_LINE": 0,
                "MODE": ""
            }
        }
        os.mkdir(os.path.dirname(self.origin_config_path))

    def sync_config(self):
        self.configuration["credentials"] = {
            "login": self.LOGIN,
            "password": self.PASSWORD,
            "validity": self.VALIDITY
        }
        self.configuration["automation_settings"] = {
            "TOPICS_FILE_PATH": self.TOPICS_FILE_PATH,
            "INPUT_DATA_DB_PATH": self.INPUT_DATA_DB_PATH,
            "CLASSWORK_FOLDER": self.CLASSWORK_FOLDER,
            "HOMEWORK_FOLDER": self.HOMEWORK_FOLDER,
            "START_CELL": self.START_CELL,
            "START_FROM_LINE": self.START_FROM_LINE,
            "END_ON_LINE": self.END_ON_LINE,
            "MODE": self.MODE
        }

        with open(self.origin_config_path, 'w', encoding='utf-8') as f:
            json.dump(self.configuration, f, ensure_ascii=False, indent=4)
