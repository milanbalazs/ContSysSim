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

    # Mapping log levels to their 3-letter abbreviations and colors
    LEVEL_ABBREVIATIONS = {
        logging.DEBUG: "DBG",
        logging.INFO: "INF",
        logging.WARNING: "WAR",
        logging.ERROR: "ERR",
        logging.CRITICAL: "CRT",
    }

    # ANSI color codes for log levels
    LEVEL_COLORS = {
        logging.DEBUG: Fore.WHITE,
        logging.INFO: Fore.CYAN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.LIGHTRED_EX,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Customize the log level display with abbreviations and colors."""
        # Add level abbreviation and colorize it
        color = self.LEVEL_COLORS.get(record.levelno, "")
        record.levelname = (
            f"{color}"
            f"{self.LEVEL_ABBREVIATIONS.get(record.levelno, record.levelname[:3])}"
            f"{Style.RESET_ALL}"
        )

        # Add color if it is a console log
        color = self.LEVEL_COLORS.get(record.levelno, "")
        record.msg = f"{color}{record.msg}{Style.RESET_ALL}"  # Apply color to the message

        return super().format(record)


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


def get_logger(
    name: str,
    log_file: str = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    console_level: int = logging.INFO,
) -> logging.Logger:
    """
    Creates and configures a logger instance.

    Args:
        name (str): The name of the logger (usually __name__ of the module using it).
        log_file (str, optional): Path of the log file. Defaults to "<current_time>.log".
        console_level (int, optional): Logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a logger
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(console_level)

    # Check if the logger already has handlers (avoid duplicate handlers)
    if not logger.hasHandlers():
        # Create a file handler (rotates logs to avoid growing too large)
        # file_handler: RotatingFileHandler =
        #   RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Create a console handler for stdout
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)

        # Define a log format
        formatter = CustomFormatter(
            "[{asctime}].[{name}].[{levelname}] -> {message} \t || {module}:{funcName}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# This part is for just testing.
if __name__ == "__main__":
    logger_instance = get_logger(__name__)
    logger_instance.info("dasfd")
    logger_instance.warning("fffdf")
