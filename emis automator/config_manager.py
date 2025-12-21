
import json
# import os
import sys

class ConfigManager:
    def __init__(self, config_path='config.json'):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"Файл конфигурации не найден по пути {config_path}")
            sys.exit(1)

        # Credentials
        self.LOGIN = self.config["credentials"]["login"]
        self.PASSWORD = self.config["credentials"]["password"]

        # Automation Settings
        self.TOPICS_FILE_PATH = self.config["automation_settings"]["TOPICS_FILE_PATH"]
        self.START_CELL = self.config["automation_settings"]["START_CELL"]
        self.START_FROM_LINE = self.config["automation_settings"]["START_FROM_LINE"]
        self.END_ON_LINE = self.config["automation_settings"]["END_ON_LINE"]
        self.MODE = self.config["automation_settings"]["MODE"]
        self.TOPICS_FOLDER = self.config["automation_settings"]["TOPICS_FOLDER"]
        self.HOMEWORK_FOLDER = self.config["automation_settings"]["HOMEWORK_FOLDER"]

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
