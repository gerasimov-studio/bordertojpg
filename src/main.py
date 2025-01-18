import argparse
import os
from settings_manager import SettingsManager
from image_processor import process_image


def parse_arguments():
    parser = argparse.ArgumentParser(description="Image processing application.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Process command
    process_parser = subparsers.add_parser("process", help="Process an image.")
    process_parser.add_argument("input", help="Path to the input image.")
    process_parser.add_argument("--profile", help="Processing profile to use.")
    process_parser.add_argument("--output", help="Path to save the processed image.")

    # Settings command
    settings_parser = subparsers.add_parser("settings", help="Manage settings and profiles.")
    settings_parser.add_argument("action", choices=["list-profiles", "set-profile", "create-profile", "delete-profile"])
    settings_parser.add_argument("--name", help="Profile name for create, set, or delete.")

    return parser.parse_args()


def process_command(args, settings_manager):
    input_path = args.input
    output_path = args.output
    profile_name = args.profile or settings_manager.user_settings.get("active_profile")

    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist.")
        return

    profile_settings = settings_manager.load_profile(profile_name)
    if not profile_settings:
        print(f"Error: Profile '{profile_name}' not found.")
        return

    output_path = output_path or f"{os.path.splitext(input_path)[0]}_processed.jpg"
    process_image(input_path, output_path, **profile_settings)
    print(f"Image processed and saved to '{output_path}' using profile '{profile_name}'.")


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