import os
import logging
from logging.handlers import RotatingFileHandler
from utils import get_settings_directory
import constants


class AppLogger:
    """
    A class to handle application logging with rotation.
    """

    def __init__(self):
        # Get the base directory for logs using get_settings_directory()
        self.logs_dir = os.path.join(get_settings_directory(), constants.LOGS_DIR_NAME)
        os.makedirs(self.logs_dir, exist_ok=True)  # Create logs directory if it doesn't exist
        self.log_file = os.path.join(self.logs_dir, "app.log")
        self._setup_logging()

    def _setup_logging(self):
        """
        Configures logging with rotation using constants from constants.py.
        """
        logging.basicConfig(
            level=logging.DEBUG,  # Log everything (DEBUG and above)
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                RotatingFileHandler(
                    self.log_file,
                    maxBytes=constants.LOG_FILE_MAX_SIZE,  # Use constant for max file size
                    backupCount=constants.LOG_BACKUP_COUNT,  # Use constant for backup count
                    encoding="utf-8"
                ),
                logging.StreamHandler()  # Print logs to the console
            ]
        )
        logging.info("Logging setup complete. Log file: %s", self.log_file)

    @staticmethod
    def info(message):
        """Log an info message."""
        logging.info(message)

    @staticmethod
    def debug(message):
        """Log a debug message."""
        logging.debug(message)

    @staticmethod
    def warning(message):
        """Log a warning message."""
        logging.warning(message)

    @staticmethod
    def error(message):
        """Log an error message."""
        logging.error(message)

    @staticmethod
    def critical(message):
        """Log a critical message."""
        logging.critical(message)

    @staticmethod
    def exception(message):
        """Log an exception with traceback."""
        logging.exception(message)