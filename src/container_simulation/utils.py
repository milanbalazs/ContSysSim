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


def _create_logger() -> logging.Logger:
    """
    Creates a singleton logger instance for the framework.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a logger
    logger: logging.Logger = logging.getLogger("ContainerSim")

    if logger.hasHandlers():
        return logger  # Prevent multiple handlers from being added

    logger.setLevel(logging.DEBUG)  # Ensure all levels are captured

    # Ensure no propagation to the root logger (avoid duplicate logs)
    logger.propagate = False

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Show only INFO+ in console

    # File handler (ensures logs are written to a file)
    log_file = f"simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)  # Capture all logs in the file

    # Apply formatters
    console_handler.setFormatter(CustomFormatter(use_colors=True))
    file_handler.setFormatter(CustomFormatter(use_colors=False))  # Disable colors

    # Attach handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# **Global Singleton Logger**
LOGGER = _create_logger()


def get_logger() -> logging.Logger:
    """Returns the shared singleton logger instance."""
    return LOGGER


# This part is for just testing.
if __name__ == "__main__":
    logger_instance = get_logger(__name__)
    logger_instance.info("dasfd")
    logger_instance.warning("fffdf")
