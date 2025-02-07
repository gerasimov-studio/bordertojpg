# Application-level constants
APP_NAME = "EasyFrame"
VERSION = "0.1.0"
SUPPORTED_FORMATS = ["jpg"]

# Logging settings
LOG_FILE_MAX_SIZE = 1 * 1024 * 1024  # 1 MB
LOG_BACKUP_COUNT = 5  # Keep up to 5 backup files
LOGS_DIR_NAME = "logs"  # Name of the logs directory

# Default settings for initial profile creation
DEFAULT_MAX_WORKERS = 4
DEFAULT_BORDER_COLOR = (255, 255, 255)  # White
DEFAULT_PROFILE = "basic_profile"
DEFAULT_MODE = "border_size"  # Can be "border_size" or "output_size"
DEFAULT_BORDER_SIZE = "5%"
DEFAULT_OUTPUT_SIZE = (1080, 1080)
DEFAULT_MIN_BORDER = 0
DEFAULT_OUTPUT_PATTERN = "{filename}_processed.{ext}"
DEFAULT_ALLOW_OVERWRITE = False

# File paths for settings
USER_CONFIG_FILENAME = "user_settings.json"
PROFILES_DIR_NAME = "profiles"