import argparse
import glob
import os
from settings_manager import SettingsManager
from image_processor import process_image
import constants


def parse_arguments():
    parser = argparse.ArgumentParser(description="Image processing application.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Process command
    process_parser = subparsers.add_parser("process", help="Process an image.")
    process_parser.add_argument("input", nargs="+", help="Path to the input image.")
    process_parser.add_argument("--profile", help="Processing profile to use.")

    # Settings command
    settings_parser = subparsers.add_parser("settings", help="Manage settings and profiles.")
    settings_parser.add_argument("action", choices=["list-profiles", "set-profile", "create-profile", "delete-profile"])
    settings_parser.add_argument("--name", help="Profile name for create, set, or delete.")

    return parser.parse_args()


def process_command(args, settings_manager):
    input_path = args.input
    profile_name = args.profile or settings_manager.user_settings.get("active_profile")

    profile_settings = settings_manager.load_profile(profile_name)
    if not profile_settings:
        print(f"Error: Profile '{profile_name}' not found.")
        return

    for input_path in args.input:
        # Проверяем, что input_path — строка
        if not isinstance(input_path, str):
            print(f"Error: Invalid input path type '{type(input_path)}'. Expected a string.")
            continue

        if not os.path.exists(input_path):
            print(f"Error: Input path '{input_path}' does not exist.")
            continue

        # Если это директория, фильтруем файлы по SUPPORTED_FORMATS
        if os.path.isdir(input_path):
            files = [f for f in glob.glob(os.path.join(input_path, "*")) if
                     f.split('.')[-1].lower() in constants.SUPPORTED_FORMATS]
            if not files:
                print(f"No supported files found in directory '{input_path}'.")
                continue
            for file in files:
                process_image(file, **profile_settings)
                print(f"Processed file: {file}")

        # Если это файл, обрабатываем его
        elif os.path.isfile(input_path):
            process_image(input_path, **profile_settings)
            print(f"Processed file: {input_path}")

        else:
            print(f"Error: Input '{input_path}' is neither a valid file nor directory.")

    print(f"Image processed and saved using profile '{profile_name}'.")


def settings_command(args, settings_manager):
    if args.action == "list-profiles":
        profiles = settings_manager.list_profiles()
        print("Available profiles:")
        for profile in profiles:
            print(f" - {profile}")

    elif args.action == "set-profile":
        settings_manager.set_active_profile(args.name)
        print(f"Active profile set to '{args.name}'.")

    elif args.action == "create-profile":
        settings_manager.create_profile(args.name)
        print(f"Profile '{args.name}' created.")

    elif args.action == "delete-profile":
        try:
            settings_manager.delete_profile(args.name)
            print(f"Profile '{args.name}' deleted.")
        except ValueError as e:
            print(e)


def main():
    """
    Main function to handle CLI arguments and dispatch commands.
    """
    args = parse_arguments()
    settings_manager = SettingsManager()

    if args.command == "process":
        process_command(args, settings_manager)
    elif args.command == "settings":
        settings_command(args, settings_manager)
    else:
        print("Error: No command specified. Use '--help' for available commands.")


if __name__ == "__main__":
    main()