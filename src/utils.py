import os
import platform
from datetime import datetime
from constants import APP_NAME, DEFAULT_OUTPUT_PATTERN

def get_settings_directory():
    system = platform.system()
    if system == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", APP_NAME)
    elif system == "Windows":  # Windows
        return os.path.join(os.getenv("APPDATA"), APP_NAME)
    else:  # Linux/Unix
        return os.path.join(os.path.expanduser("~"), f".{APP_NAME.lower()}")


def generate_output_path(input_path, output_pattern=DEFAULT_OUTPUT_PATTERN, overwrite=False):
    """
    Generates an output path based on the given pattern and overwrite setting.

    :param input_path: Path to the input file.
    :param output_pattern: Naming pattern for the output file.
                           Supports placeholders:
                           - {filename}: Original file name without extension.
                           - {ext}: Original file extension.
                           - {timestamp}: Current timestamp in YYYYMMDD_HHMMSS format.
    :param overwrite: Whether to overwrite the input file.
    :return: The output file path.
    """
    dir_name, file_name = os.path.split(input_path)
    filename, ext = os.path.splitext(file_name)
    ext = ext.lstrip(".")  # Remove the dot for consistency

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    formatted_name = output_pattern.format(filename=filename, ext=ext, timestamp=timestamp)

    print(formatted_name)

    if overwrite:
        return input_path
    elif os.path.isabs(output_pattern):
        return os.path.join(output_pattern, f"{formatted_name}")
    else:
        return os.path.join(dir_name, f"{formatted_name}")