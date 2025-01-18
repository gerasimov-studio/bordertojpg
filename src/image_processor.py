from PIL import Image, ImageOps
import constants
from utils import generate_output_path


def process_image(input_path, **profile_settings):
    """
    Adds a border to an image. Supports different modes.

    :param input_path: Path to the source image.
    :param profile_settings: Current profile parameters.
    """
    # Extract parameters from the profile
    mode = profile_settings.get("mode", constants.DEFAULT_MODE)
    overwrite = profile_settings.get("overwrite", constants.DEFAULT_ALLOW_OVERWRITE)
    output_pattern = profile_settings.get("output_pattern", constants.DEFAULT_OUTPUT_PATTERN)

    img = Image.open(input_path)

    # Define valid modes and their required/optional arguments
    mode_args = {
        "output_size": {
            "required": ["output_size"],
            "optional": ["min_border"]
        },
        "border_size": {
            "required": ["border_size"],
            "optional": []
        }
    }

    # Validate the mode
    if mode not in mode_args:
        raise ValueError(f"Invalid mode: {mode}. Supported modes are: {', '.join(mode_args.keys())}")

    # Filter arguments based on the mode
    filtered_profile_settings = filter_profile_settings(
        profile_settings,
        required_keys=mode_args[mode]["required"],
        optional_keys=mode_args[mode]["optional"]
    )

    # Initialize borders
    borders = None

    # Select mode
    if mode == "output_size":
        target_size = filtered_profile_settings["output_size"]
        min_border = filtered_profile_settings.get("min_border", constants.DEFAULT_MIN_BORDER)

        # Resize the image and calculate borders
        resized_img, new_size = resize_image(img, target_size, min_border)
        borders = calculate_borders_for_output_size(new_size, target_size)

        # Update the image to the resized version
        img = resized_img
    elif mode == "border_size":
        borders = calculate_borders_for_border_size(img, **filtered_profile_settings)

    # Apply the border
    img_with_border = apply_border(img, borders, tuple(profile_settings.get("border_color", constants.DEFAULT_BORDER_COLOR)))

    output_path = generate_output_path(input_path, output_pattern, overwrite)

    # Save the result
    img_with_border.save(output_path, format="JPEG", quality=95, subsampling=0)


def resize_image(img, target_size, min_border=0):
    """
    Resizes the image to fit within the target size, considering a minimum border width.

    :param img: The source image (PIL.Image).
    :param target_size: The target size (width, height) or a single value for the larger side.
    :param min_border: Minimum border width.
    :return: Resized image and its new dimensions (width, height).
    """
    img_width, img_height = img.size

    if isinstance(target_size, int):  # Single value: scale by the larger side
        scale = target_size / max(img_width, img_height)
        new_width, new_height = map(make_even, (int(img_width * scale), int(img_height * scale)))
    elif isinstance(target_size, (tuple, list)) and len(target_size) == 2:  # Tuple (width, height)
        target_width, target_height = map(make_even, target_size)
        scale = min(
            (target_width - 2 * min_border) / img_width,
            (target_height - 2 * min_border) / img_height
        )
        new_width, new_height = map(make_even, (int(img_width * scale), int(img_height * scale)))
    else:
        raise ValueError("target_size must be an int or a tuple (width, height)")

    # Resize the image
    img_resized = img.resize((new_width, new_height), Image.LANCZOS)

    return img_resized, (new_width, new_height)


def calculate_borders_for_output_size(new_size, output_size):
    """
    Calculates the border dimensions for the output size mode.

    :param new_size: The size of the resized image (width, height).
    :param output_size: The target image size (including the border), tuple (width, height).
    :return: A tuple of borders (left, top, right, bottom).
    """
    new_width, new_height = new_size
    output_width, output_height = output_size

    # Calculate the border dimensions
    left_border = (output_width - new_width) // 2
    top_border = (output_height - new_height) // 2
    right_border = output_width - new_width - left_border
    bottom_border = output_height - new_height - top_border

    return left_border, top_border, right_border, bottom_border


def calculate_borders_for_border_size(img, border_size):
    """
    Calculates the border dimensions for the border-size border mode.

    :param img: The source image (PIL.Image).
    :param border_size: The size of the border, which can be:
                        - A single value (int or percentage, e.g., "10" or "10%").
                        - Two values (horizontal, vertical, e.g., "10,20" or "10%,20").
                        - Four values (left, top, right, bottom, e.g., "10,20,30,40" or combinations like "10,10%,20,20%").
    :return: A tuple of borders (left, top, right, bottom).
    """
    img_width, img_height = img.size

    def to_pixels(value, reference):
        """Converts a value to pixels. Supports percentages (e.g., "10%") and integers."""
        if isinstance(value, str) and value.endswith('%'):
            return make_even(int(float(value.strip('%')) / 100 * reference))
        elif value.isdigit():
            return make_even(int(value))
        else:
            raise ValueError(f"Invalid border size value: {value}")

    # Split and process border_size
    if isinstance(border_size, str):
        parts = border_size.split(',')
    elif isinstance(border_size, (tuple, list)):
        parts = [str(p) for p in border_size]
    else:
        parts = [str(border_size)]

    # Handle different lengths of parts
    if len(parts) == 1:
        border = to_pixels(parts[0], max(img_width, img_height))
        left_border = top_border = right_border = bottom_border = border
    elif len(parts) == 2:
        left_border = right_border = to_pixels(parts[0], img_width)
        top_border = bottom_border = to_pixels(parts[1], img_height)
    elif len(parts) == 4:
        left_border = to_pixels(parts[0], img_width)
        top_border = to_pixels(parts[1], img_height)
        right_border = to_pixels(parts[2], img_width)
        bottom_border = to_pixels(parts[3], img_height)
    else:
        raise ValueError("border_size must contain 1, 2, or 4 values (pixels or percentages).")

    return left_border, top_border, right_border, bottom_border


def apply_border(img, borders, border_color):
    """
    Applies the border to the image.

    :param img: The source image (PIL.Image).
    :param borders: A tuple of borders (left, top, right, bottom).
    :param border_color: The color of the border (RGB tuple).
    :return: The image with the added border.
    """
    left_border, top_border, right_border, bottom_border = borders
    return ImageOps.expand(
        img,
        border=(left_border, top_border, right_border, bottom_border),
        fill=border_color
    )


def filter_profile_settings(profile_settings, required_keys=None, optional_keys=None, required=True):
    """
    Filters a dictionary of keyword arguments, validating required and optional keys.

    :param profile_settings: Dictionary of keyword arguments to filter.
    :param required_keys: List of keys that are required.
    :param optional_keys: List of keys that are optional.
    :param required: Whether to enforce the presence of required keys.
    :return: A dictionary containing only the allowed keys.
    """
    required_keys = required_keys or []
    optional_keys = optional_keys or []

    # Check for missing required keys
    if required:
        missing_keys = [key for key in required_keys if key not in profile_settings]
        if missing_keys:
            raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")

    # Filter and include only valid keys
    filtered_profile_settings = {
        key: value for key, value in profile_settings.items()
        if key in required_keys or key in optional_keys
    }

    return filtered_profile_settings


def make_even(value):
    """
    Rounds the value to the nearest even number.

    :param value: An integer.
    :return: The nearest even number.
    """
    return value if value % 2 == 0 else value + 1