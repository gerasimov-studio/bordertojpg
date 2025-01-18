import argparse
import glob
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from settings_manager import SettingsManager
from image_processor import process_image
import constants


def parse_arguments():
    # Parse command-line arguments
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


def process_file(input_path, profile_settings):
    # Function to process a single file or directory
    if not os.path.exists(input_path):
        print(f"Error: Input path '{input_path}' does not exist.")
        return

    # If it's a directory, filter files by SUPPORTED_FORMATS
    if os.path.isdir(input_path):
        files = [f for f in glob.glob(os.path.join(input_path, "*")) if
                 f.split('.')[-1].lower() in constants.SUPPORTED_FORMATS]
        if not files:
            print(f"No supported files found in directory '{input_path}'.")
            return
        # Process each file in the directory
        for file in files:
            process_image(file, **profile_settings)
            print(f"Processed file: {file}")

    # If it's a file, process it
    elif os.path.isfile(input_path):
        process_image(input_path, **profile_settings)
        print(f"Processed file: {input_path}")

    else:
        print(f"Error: Input '{input_path}' is neither a valid file nor directory.")


def process_command(args, settings_manager):
    # Get profile settings from the profile manager
    profile_name = args.profile or settings_manager.user_settings.get("active_profile")
    profile_settings = settings_manager.load_profile(profile_name)
    if not profile_settings:
        print(f"Error: Profile '{profile_name}' not found.")
        return

    # Use ThreadPoolExecutor for concurrent file processing
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks to the thread pool for concurrent processing
        futures = []
        for input_path in args.input:
            futures.append(executor.submit(process_file, input_path, profile_settings))

        # Wait for all futures to complete and process them as they finish
        for future in as_completed(futures):
            future.result()  # Blocks until the file processing is done

    print(f"Image processing completed using profile '{profile_name}'.")


def settings_command(args, settings_manager):
    # Settings-related commands (list, set, create, delete profiles)
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

    # Program will exit after processing all files, no need to wait explicitly
    print("All tasks completed. Exiting the program.")


if __name__ == "__main__":
    main()