# Application-level constants
APP_NAME = "EasyFrame"
VERSION = "0.1.0"
SUPPORTED_FORMATS = ["jpg"]

# Default settings for initial profile creation
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