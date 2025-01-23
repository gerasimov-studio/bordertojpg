import os
import json
import constants
from utils import get_settings_directory


class SettingsManager:
    def __init__(self):
        # Paths and directories
        self.base_dir = get_settings_directory()
        self.user_config_path = os.path.join(self.base_dir, constants.USER_CONFIG_FILENAME)
        self.profiles_dir = str(os.path.join(self.base_dir, constants.PROFILES_DIR_NAME))

        # Ensure directories exist
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.profiles_dir, exist_ok=True)

        # Initialize files
        self._initialize_files()

        # Load user settings and active profile
        self.user_settings = self._load_json(self.user_config_path)
        active_profile_name = self.user_settings.get("active_profile", constants.DEFAULT_PROFILE)
        self.active_profile = self.load_profile(active_profile_name)

    def list_profiles(self):
        """Return a list of available profiles."""
        return [os.path.splitext(p)[0] for p in os.listdir(self.profiles_dir) if p.endswith(".json")]

    def load_profile(self, profile_name):
        """Public method to load a profile."""
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        if os.path.exists(profile_path):
            return self._load_json(profile_path)
        return None

    def create_profile(self, profile_name, default_data=None):
        """Create a new profile with optional default data."""
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        if os.path.exists(profile_path):
            raise ValueError(f"Profile '{profile_name}' already exists.")
        data = default_data or {
            "mode": constants.DEFAULT_MODE,  # Changed from "scenario" to "mode"
            "border_color": constants.DEFAULT_BORDER_COLOR,
            "border_size": constants.DEFAULT_BORDER_SIZE,
            "output_size": constants.DEFAULT_OUTPUT_SIZE,
            "min_border": constants.DEFAULT_MIN_BORDER,
            "output_pattern": constants.DEFAULT_OUTPUT_PATTERN,
            "allow_overwrite": constants.DEFAULT_ALLOW_OVERWRITE,
        }
        self._save_json(profile_path, data)

    def delete_profile(self, profile_name):
        """Delete a profile, and switch to default if it's active."""
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        if os.path.exists(profile_path):
            if profile_name == self.user_settings.get("active_profile"):
                # If the profile is active, switch to the default profile
                self.set_active_profile(constants.DEFAULT_PROFILE)
                print(f"Active profile '{profile_name}' deleted. Switched to default profile.")
            os.remove(profile_path)
        else:
            raise ValueError(f"Profile '{profile_name}' does not exist.")

    def set_active_profile(self, profile_name):
        """Set the active profile."""
        if profile_name != self.user_settings.get("active_profile"):
            if not self.load_profile(profile_name):
                raise ValueError(f"Profile '{profile_name}' does not exist.")
            self.user_settings["active_profile"] = profile_name
            self._save_json(self.user_config_path, self.user_settings)
            self.active_profile = self.load_profile(profile_name)

    # Private methods remain unchanged (_load_json, _save_json, _initialize_files)
    def _initialize_files(self):
        """Initialize user settings and the default profile."""
        if not os.path.exists(self.user_config_path):
            self._save_json(self.user_config_path, {
                "active_profile": constants.DEFAULT_PROFILE,
                "max_workers": constants.DEFAULT_MAX_WORKERS
            })

        # Create default profile if not present
        default_profile_path = os.path.join(self.profiles_dir, f"{constants.DEFAULT_PROFILE}.json")
        if not os.path.exists(default_profile_path):
            self._save_json(default_profile_path, {
                "mode": constants.DEFAULT_MODE,  # Changed from "scenario" to "mode"
                "border_color": constants.DEFAULT_BORDER_COLOR,
                "border_size": constants.DEFAULT_BORDER_SIZE,
                "output_size": constants.DEFAULT_OUTPUT_SIZE,
                "min_border": constants.DEFAULT_MIN_BORDER,
                "overwrite": constants.DEFAULT_ALLOW_OVERWRITE,
                "output_pattern": constants.DEFAULT_OUTPUT_PATTERN,
            })

    @staticmethod
    def _load_json(path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    @staticmethod
    def _save_json(path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)