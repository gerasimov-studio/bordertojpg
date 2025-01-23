import argparse
import glob
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
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

    return parser


def process_file(file_path, profile_settings):
    """
    Processes a single file using the provided profile settings.
    """
    try:
        # Call the main image processing function
        process_image(file_path, **profile_settings)
        print(f"Processed file: {file_path}")
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")


def process_command(input_paths, settings_manager, profile_name=constants.DEFAULT_PROFILE):
    # Get profile settings from the profile manager
    profile_settings = settings_manager.load_profile(profile_name)
    if not profile_settings:
        print(f"Error: Profile '{profile_name}' not found.")
        return

    # Get max_workers from profile settings or use a default value
    max_workers = settings_manager.user_settings.get("max_workers", constants.DEFAULT_MAX_WORKERS)

    # Collect all files to process
    files_to_process = []
    for input_path in input_paths:
        if not os.path.exists(input_path):
            print(f"Error: Input path '{input_path}' does not exist.")
            continue

        if os.path.isdir(input_path):
            # Collect supported files from the directory
            files = [f for f in glob.glob(os.path.join(input_path, "*")) if
                     f.split('.')[-1].lower() in constants.SUPPORTED_FORMATS]
            if not files:
                print(f"No supported files found in directory '{input_path}'.")
            else:
                files_to_process.extend(files)
        elif os.path.isfile(input_path):
            files_to_process.append(input_path)
        else:
            print(f"Error: Input '{input_path}' is neither a valid file nor directory.")

    if not files_to_process:
        print("No files to process.")
        return

    # Use ThreadPoolExecutor for concurrent file processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks to the thread pool for concurrent processing
        futures = [executor.submit(process_image, file, **profile_settings) for file in files_to_process]

        # Wait for all futures to complete and process them as they finish
        for future in as_completed(futures):
            try:
                future.result()  # Blocks until the file processing is done
            except Exception as e:
                print(f"Error processing file: {e}")

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
    Main entry point of the application.
    Handles both CLI and drag-and-drop/context menu execution.
    """
    settings_manager = SettingsManager()
    profile_name = settings_manager.user_settings.get("active_profile", constants.DEFAULT_PROFILE)

    # Initialize argument parser
    parser = parse_arguments()  # Correctly assign the parser object
    if len(sys.argv) > 1:
        args = parser.parse_args()  # Parse the arguments from command-line input

        if args.command == "process":
            # Process command with files or folders
            input_paths = args.input or []
            if not input_paths:
                print("Error: No input files or folders provided.")
                return
            process_command(input_paths, settings_manager, args.profile or profile_name)

        elif args.command == "settings":
            # Settings-related command
            settings_command(args, settings_manager)

        else:
            parser.print_help()  # Display help if the command is not recognized

    else:
        # If no command is specified, check for drag-and-drop files
        input_paths = sys.argv[1:]  # Collect paths passed via drag-and-drop
        if input_paths:
            process_command(input_paths, settings_manager, profile_name)
        else:
            print("Error: No input files or folders provided. Use '--help' for usage details.")

if __name__ == "__main__":
    main()