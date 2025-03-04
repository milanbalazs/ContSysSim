"""
Containerized System Analyzer

This module provides functionality for monitoring and analyzing the resource usage
of Docker containers and Swarm services. It collects CPU, RAM, Disk, and Network
statistics over a specified time window and computes average resource consumption.

Classes:
    - ContainerizedSystemAnalyzer: Monitors and analyzes container/service resource usage.

Functions:
    - parse_timestamp(timestamp: str) -> datetime: Parses and converts an ISO 8601 timestamp.
    - get_cpu_cores_used(stat: dict) -> float: Computes the number of CPU cores actively used.
    - get_ram_usage_mb(stat: dict) -> float: Retrieves RAM usage in MB.
    - get_total_network_usage(start_stat: dict, end_stat: dict) -> dict: Calculates network usage.
    - analyze_container_performance(container_or_service_id: Optional[str],
        container_or_service_name: Optional[str]) -> dict:
            Collects resource usage statistics over a time window and computes averages.

Usage Example:
    analyzer = ContainerizedSystemAnalyzer(time_window=20, period=0.1)
    result = analyzer.analyze_container_performance("0800b9b5426c")

    print(f"Average CPU Usage: {result['average_cpu_cores']} cores")
    print(f"Average RAM Usage: {result['average_ram_usage_mb']} MB")
    print(f"Average Disk Space Used: {result['average_disk_usage_mb']} MB")
    print(f"Total Network RX: {result['average_rx_mb']} MB")
    print(f"Total Network TX: {result['average_tx_mb']} MB")
"""


import time
from typing import Optional
from datetime import datetime
from statistics import mean
from logging import Logger

from container_simulation.utils import get_logger
from container_simulation.container_analyzer.container_analyzer import ContainerAnalyzer
from container_simulation.container_analyzer.service_analyzer import ServiceAnalyzer

LOGGER: Logger = get_logger()


class ContainerizedSystemAnalyzer:
    """
    Analyzes resource consumption of Docker containers or
    Swarm services over a specified time window.
    This class collects CPU, RAM, Disk, and Network usage statistics and computes averages.

    Attributes:
        time_window (int): The total duration (in seconds) for monitoring.
        period (float): The interval (in seconds) between each measurement.
        entries (list[str]): A list of resource metrics to monitor (e.g., "cpu", "ram", "disk"...).
        analyzer (ContainerAnalyzer | ServiceAnalyzer):
            The appropriate analyzer instance based on swarm mode.
    """

    def __init__(
        self,
        time_window: int = 20,
        period: float = 0.1,
        swarm_mode: bool = False,
        entries: Optional[list[str]] = None,
    ) -> None:
        """
        Initializes the containerized system analyzer.

        Args:
            time_window (int, optional): Duration (in seconds) to monitor
                the container/service.
            period (float, optional): Sampling interval (in seconds) between measurements.
            swarm_mode (bool, optional): Whether to analyze a Swarm service instead of a container.
            entries (Optional[list[str]], optional): List of metrics to track
                (default: ["cpu", "ram", "disk", "bw"]).
        """
        self.time_window: int = time_window
        self.period: float = period
        self.entries: list[str] = entries or ["cpu", "ram", "disk", "bw"]
        if swarm_mode:
            self.analyzer: ServiceAnalyzer = ServiceAnalyzer()
        else:
            self.analyzer: ContainerAnalyzer = ContainerAnalyzer()

    @staticmethod
    def parse_timestamp(timestamp: str) -> datetime:
        """
        Parses an ISO 8601 timestamp and converts it to a datetime object.
        Handles nanoseconds by truncating them to microseconds.

        Args:
            timestamp (str): The timestamp string in ISO 8601 format.

        Returns:
            datetime: Parsed datetime object.
        """
        timestamp: str = timestamp.rstrip("Z")  # Remove 'Z' if present
        parts: list[str] = timestamp.split(".")  # Split timestamp at decimal

        if len(parts) == 2 and len(parts[1]) > 6:
            # Convert nanoseconds to microseconds by truncating extra digits
            timestamp: str = f"{parts[0]}.{parts[1][:6]}"

        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")

    @staticmethod
    def get_cpu_cores_used(stat: dict) -> float:
        """
        Calculates the number of CPU cores actively used by the container or service.

        Args:
            stat (dict): The statistics dictionary retrieved from Docker.

        Returns:
            float: The number of CPU cores actively used.
        """
        precpu_stats: dict = stat["precpu_stats"]
        cpu_stats: dict = stat["cpu_stats"]

        total_usage_diff: float = (
            cpu_stats["cpu_usage"]["total_usage"] - precpu_stats["cpu_usage"]["total_usage"]
        )
        system_usage_diff: float = cpu_stats["system_cpu_usage"] - precpu_stats["system_cpu_usage"]
        online_cpus: float = cpu_stats["online_cpus"]

        return (
            round((total_usage_diff / system_usage_diff) * online_cpus, 3)
            if system_usage_diff > 0
            else 0.0
        )

    @staticmethod
    def get_ram_usage_mb(stat: dict) -> float:
        """
        Calculates the RAM usage of the container/service in megabytes (MB).

        Args:
            stat (dict): The statistics dictionary retrieved from Docker.

        Returns:
            float: RAM usage in MB.
        """
        memory_stats: dict = stat["memory_stats"]
        memory_usage: int = memory_stats["usage"]  # Bytes

        return round(memory_usage / (1024**2), 2)  # Convert to MB

    @staticmethod
    def get_total_network_usage(start_stat: dict, end_stat: dict) -> dict:
        """
        Computes the total network data used (MB) within the monitoring window.

        Args:
            start_stat (dict): Initial network statistics.
            end_stat (dict): Final network statistics.

        Returns:
            dict: A dictionary containing:
                - "total_rx_mb" (float): Total received data in MB.
                - "total_tx_mb" (float): Total transmitted data in MB.
        """
        networks_start: dict = start_stat.get("networks", {})
        networks_end: dict = end_stat.get("networks", {})

        if not networks_start or not networks_end:
            LOGGER.warning("No network data available. 0 (zero) will be used!")
            return {"total_rx_mb": 0.0, "total_tx_mb": 0.0}

        # Auto-detect the first available network interface
        network_interface: str = next(iter(networks_start), None)
        if not network_interface:
            LOGGER.warning("No network interfaces found. 0 (zero) will be used!")
            return {"total_rx_mb": 0.0, "total_tx_mb": 0.0}

        LOGGER.debug(f"DEBUG: Using network interface: {network_interface}")

        # Extract data
        rx_start: int = networks_start.get(network_interface, {}).get("rx_bytes", 0)
        tx_start: int = networks_start.get(network_interface, {}).get("tx_bytes", 0)
        rx_end: int = networks_end.get(network_interface, {}).get("rx_bytes", 0)
        tx_end: int = networks_end.get(network_interface, {}).get("tx_bytes", 0)

        LOGGER.debug(f"DEBUG: Network RX start: {rx_start} bytes, end: {rx_end} bytes")  # Debugging
        LOGGER.debug(f"DEBUG: Network TX start: {tx_start} bytes, end: {tx_end} bytes")  # Debugging

        total_rx: float = max(rx_end - rx_start, 0) / (1024**2)  # Convert bytes to MB
        total_tx: float = max(tx_end - tx_start, 0) / (1024**2)  # Convert bytes to MB

        return {
            "total_rx_mb": round(total_rx, 2),
            "total_tx_mb": round(total_tx, 2),
        }

    def analyze_container_performance(
        self,
        container_or_service_id: Optional[str] = None,
        container_or_service_name: Optional[str] = None,
    ) -> dict:
        """
        Collects resource usage statistics for a Docker container
            or Swarm service over a time window.

        Args:
            container_or_service_id (Optional[str], optional): The container or service ID.
            container_or_service_name (Optional[str], optional): The container or service name.

        Returns:
            dict: A dictionary containing:
                - "average_cpu_cores" (float): Average CPU cores used.
                - "average_ram_usage_mb" (float): Average RAM usage in MB.
                - "average_disk_usage_mb" (float): Average disk usage in MB.
                - "average_rx_mb" (float): Average network received data in MB.
                - "average_tx_mb" (float): Average network transmitted data in MB.
                - "samples_cpu" (dict): CPU usage samples over time.
                - "samples_ram" (dict): RAM usage samples over time.
                - "samples_disk" (dict): Disk usage samples over time.
                - "samples_rx" (dict): Network RX samples over time.
                - "samples_tx" (dict): Network TX samples over time.
        """
        start_time: float = time.time()
        cpu_cores_samples: dict = {}
        ram_usage_samples: dict = {}
        disk_usage_samples: dict = {}
        rx_usage_samples: dict = {}
        tx_usage_samples: dict = {}

        # Get initial stats
        previous_stat: dict = self.analyzer.get_stats(
            container_or_service_id, container_or_service_name
        )

        sample_tick: float = 0

        while (time.time() - start_time) < self.time_window:
            current_stat: dict = self.analyzer.get_stats(
                container_or_service_id, container_or_service_name
            )

            # CPU and RAM usage
            cpu_cores_samples[str(sample_tick)] = self.get_cpu_cores_used(current_stat)
            ram_usage_samples[str(sample_tick)] = self.get_ram_usage_mb(current_stat)

            # Disk Usage (instead of R/W speed)
            disk_usage_samples[str(sample_tick)] = self.analyzer.get_disk_usage(
                container_or_service_id
            )

            # Extract network stats
            networks_current = current_stat.get("networks", {})
            networks_previous = previous_stat.get("networks", {})

            # Auto-detect the first available network interface
            network_interface: str = next(iter(networks_current), None)

            if network_interface and network_interface in networks_previous:
                rx_now = networks_current[network_interface].get("rx_bytes", 0)
                tx_now = networks_current[network_interface].get("tx_bytes", 0)

                rx_prev = networks_previous[network_interface].get("rx_bytes", 0)
                tx_prev = networks_previous[network_interface].get("tx_bytes", 0)

                # Calculate per-tick network usage
                rx_usage_samples[str(sample_tick)] = max(rx_now - rx_prev, 0) / (1024**2)  # MB
                tx_usage_samples[str(sample_tick)] = max(tx_now - tx_prev, 0) / (1024**2)  # MB

            # Update previous stat for next iteration
            previous_stat = current_stat

            sample_tick += self.period
            time.sleep(self.period)

        return {
            "average_cpu_cores": round(mean(cpu_cores_samples.values()), 3),
            "average_ram_usage_mb": round(mean(ram_usage_samples.values()), 2),
            "average_disk_usage_mb": round(mean(disk_usage_samples.values()), 2),
            "average_rx_mb": round(mean(rx_usage_samples.values()), 2),
            "average_tx_mb": round(mean(tx_usage_samples.values()), 2),
            "samples_cpu": cpu_cores_samples,
            "samples_ram": ram_usage_samples,
            "samples_disk": disk_usage_samples,
            "samples_rx": rx_usage_samples,
            "samples_tx": tx_usage_samples,
        }


if __name__ == "__main__":
    analyzer = ContainerizedSystemAnalyzer(time_window=20, period=0.1)
    result = analyzer.analyze_container_performance("0800b9b5426c")

    print(f"Average CPU Usage: {result['average_cpu_cores']} cores")
    print(f"Average RAM Usage: {result['average_ram_usage_mb']} MB")
    print(f"Average Disk Space Used: {result['average_disk_usage_mb']} MB")
    print(f"Total Network RX: {result['average_rx_mb']} MB")
    print(f"Total Network TX: {result['average_tx_mb']} MB")
