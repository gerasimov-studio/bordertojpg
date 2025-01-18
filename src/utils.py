import os
import platform
from constants import APP_NAME

def get_settings_directory():
    system = platform.system()
    if system == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", APP_NAME)
    elif system == "Windows":  # Windows
        return os.path.join(os.getenv("APPDATA"), APP_NAME)
    else:  # Linux/Unix
        return os.path.join(os.path.expanduser("~"), f".{APP_NAME.lower()}")