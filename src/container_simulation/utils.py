"""Utility Module.

This module provides helper functions for common unit conversions used in
the container simulation framework.
"""

import logging
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)


class CustomFormatter(logging.Formatter):
    """Custom formatter to display abbreviated log levels with optional colors."""

    LEVEL_ABBREVIATIONS = {
        logging.DEBUG: "DBG",
        logging.INFO: "INF",
        logging.WARNING: "WAR",
        logging.ERROR: "ERR",
        logging.CRITICAL: "CRT",
    }

    LEVEL_COLORS = {
        logging.DEBUG: Fore.WHITE,
        logging.INFO: Fore.CYAN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.LIGHTRED_EX,
    }

    def __init__(self, use_colors: bool = True):
        """Initialize the formatter.

        Args:
            use_colors (bool): Whether to use colors in the log output.
        """
        super().__init__(
            "[{asctime}].[{name}].[{levelname}] -> {message} \t || {module}:{funcName}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
        )
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        """Customize the log level display with abbreviations and optional colors."""
        level_abbr = self.LEVEL_ABBREVIATIONS.get(record.levelno, record.levelname[:3])

        # Use colors only if enabled
        if self.use_colors:
            color = self.LEVEL_COLORS.get(record.levelno, "")
            levelname_colored = f"{color}{level_abbr}{Style.RESET_ALL}"
            msg_colored = f"{color}{record.msg}{Style.RESET_ALL}"
        else:
            levelname_colored = level_abbr
            msg_colored = record.msg

        # Avoid modifying `record` directly to prevent issues in file logs
        log_message = super().format(record)
        log_message = log_message.replace(record.levelname, levelname_colored, 1)
        log_message = log_message.replace(record.msg, msg_colored, 1)

        return log_message


def gb_to_mb(gb: float) -> int:
    """Converts gigabytes (GB) to megabytes (MB).

    This function multiplies the given GB value by 1024 to obtain the equivalent
    amount in MB.

    Args:
        gb (float): The size in gigabytes to be converted.

    Returns:
        int: The equivalent size in megabytes (MB).
    """
    return int(gb * 1024)


class LoggerManager:
    """Manages the logger instance with configurable log file paths."""

    def __init__(self, default_log_file: str = None):
        """Initialize the LoggerManager with default settings.

        Args:
            default_log_file (str): Default log file path (if not provided).
        """
        if default_log_file is None:
            default_log_file = f"simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        self.logger = logging.getLogger("ContainerSim")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        # Default handlers
        self.console_handler = self._create_console_handler()
        self.file_handler = self._create_file_handler(default_log_file)

        # Attach handlers to the logger
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)

    @staticmethod
    def _create_console_handler() -> logging.Handler:
        """Creates a console handler with colored output."""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(CustomFormatter(use_colors=True))
        return console_handler

    @staticmethod
    def _create_file_handler(log_file: str) -> logging.Handler:
        """Creates a file handler without colored output."""
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(CustomFormatter(use_colors=False))
        return file_handler

    def update_log_file(self, new_log_file: str) -> None:
        """Update the log file path dynamically.

        Args:
            new_log_file (str): New log file path to use.
        """
        # Remove the old file handler
        self.logger.removeHandler(self.file_handler)

        # Create a new file handler with the updated path
        self.file_handler = self._create_file_handler(new_log_file)
        self.logger.addHandler(self.file_handler)

        # Log the change
        self.logger.info(f"Log file updated to: {new_log_file}")


# Initialize a shared LoggerManager
_LOGGER_MANAGER = LoggerManager()


def get_logger() -> logging.Logger:
    """Returns the shared logger instance."""
    return _LOGGER_MANAGER.logger


def update_log_file(new_log_file: str) -> None:
    """Update the log file path for the shared logger."""
    _LOGGER_MANAGER.update_log_file(new_log_file)


# This part is for just testing.
if __name__ == "__main__":
    logger_instance = get_logger()
    logger_instance.info("dasfd")
    logger_instance.warning("fffdf")
