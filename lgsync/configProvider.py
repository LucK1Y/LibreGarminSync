from Interfaces import IConfigRepository
from entities import Settings
import configparser
from pathlib import Path
from typing import Optional


class IniFileConfigProvider(IConfigRepository):

    def __init__(self, config_file: Path) -> None:
        assert config_file is not None, "Config file path cannot be None"

        self.config = configparser.ConfigParser()
        if config_file.exists():
            self.config.read(config_file)
            self.settings = Settings.from_config(self.config)
        else:
            print(f"Warning: Config file {config_file} does not exist.")

        self.config_file = config_file

        print(self.settings.__dict__)

    def get_settings(self) -> Settings:
        if not hasattr(self, "settings"):
            raise ValueError("Settings have not been loaded yet.")

        return self.settings

    def save_settings(self, settings: Settings) -> None:
        self.config["Paths"] = {}
        self.config["Paths"]["remote_fit_directory"] = str(
            settings.remote_fit_directory
        )
        self.config["Paths"]["local_fit_directory"] = str(settings.local_fit_directory)
        self.config["Paths"]["gpx_directory"] = str(settings.gpx_directory)
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)
