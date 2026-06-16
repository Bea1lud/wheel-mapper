# core/config.py

import os


class Config:

    APP_NAME = "WheelMapper"
    VERSION = "0.1"

    UPDATE_INTERVAL = 50

    PROFILES_DIR = "profiles"

    DEFAULT_PROFILE = "nfs.json"

    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 650

    APPEARANCE_MODE = "dark"
    COLOR_THEME = "blue"

    LEFT_ENTER = 0.12
    LEFT_EXIT = 0.07

    RIGHT_ENTER = 0.12
    RIGHT_EXIT = 0.07

    ALPHA = 0.20

    AUTO_CALIB_TIME = 3.0
    AUTO_CALIB_ZONE = 0.03
    AUTO_CALIB_ALPHA = 0.03

    GAS_THRESHOLD = -0.35
    GAS_HYSTERESIS = 0.08

    @classmethod
    def create_folders(cls):

        os.makedirs(
            cls.PROFILES_DIR,
            exist_ok=True
        )