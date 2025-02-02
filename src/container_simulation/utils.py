"""Utility Module.

This module provides helper functions for common unit conversions used in
the container simulation framework.
"""


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
