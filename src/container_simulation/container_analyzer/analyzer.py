import time
from typing import Optional
from datetime import datetime
from statistics import mean

from container_simulation.container_analyzer.container_analyzer import ContainerAnalyzer
from container_simulation.container_analyzer.service_analyzer import ServiceAnalyzer


class ContainerizedSystemAnalyzer:
    def __init__(
        self,
        time_window: int = 20,
        period: float = 0.1,
        swarm_mode: bool = False,
        entries: Optional[list[str]] = None,
    ):
        self.time_window = time_window
        self.period = period
        self.entries = entries or ["cpu", "ram", "disk", "bw"]
        if swarm_mode:
            self.analyzer: ServiceAnalyzer = ServiceAnalyzer()
        else:
            self.analyzer: ContainerAnalyzer = ContainerAnalyzer()

    def parse_timestamp(self, timestamp: str) -> datetime:
        """Parse the ISO 8601 timestamp from Docker stats, handling nanoseconds."""
        timestamp = timestamp.rstrip("Z")  # Remove 'Z' if present
        parts = timestamp.split(".")  # Split timestamp at decimal

        if len(parts) == 2 and len(parts[1]) > 6:
            # Convert nanoseconds to microseconds by truncating extra digits
            timestamp = f"{parts[0]}.{parts[1][:6]}"

        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")

    def get_cpu_cores_used(self, stat: dict) -> float:
        """Calculate the number of CPU cores actively used."""
        precpu_stats = stat["precpu_stats"]
        cpu_stats = stat["cpu_stats"]

        total_usage_diff = (
            cpu_stats["cpu_usage"]["total_usage"] - precpu_stats["cpu_usage"]["total_usage"]
        )
        system_usage_diff = cpu_stats["system_cpu_usage"] - precpu_stats["system_cpu_usage"]
        online_cpus = cpu_stats["online_cpus"]

        return (
            round((total_usage_diff / system_usage_diff) * online_cpus, 3)
            if system_usage_diff > 0
            else 0.0
        )

    def get_ram_usage_mb(self, stat: dict) -> float:
        """Calculate RAM usage in MB."""
        memory_stats = stat["memory_stats"]
        memory_usage = memory_stats["usage"]  # Bytes

        return round(memory_usage / (1024**2), 2)  # Convert to MB

    def get_total_network_usage(self, start_stat: dict, end_stat: dict) -> dict:
        """
        Calculate the total network data used (MB) within a time window.

        Returns:
        - dict : Total network usage in MB.
        """
        networks_start = start_stat.get("networks", {})
        networks_end = end_stat.get("networks", {})

        if not networks_start or not networks_end:
            print("WARNING: No network data available.")
            return {"total_rx_mb": 0.0, "total_tx_mb": 0.0}

        # Auto-detect the first available network interface
        network_interface = next(iter(networks_start), None)
        if not network_interface:
            print("WARNING: No network interfaces found.")
            return {"total_rx_mb": 0.0, "total_tx_mb": 0.0}

        print(f"DEBUG: Using network interface: {network_interface}")

        # Extract data
        rx_start = networks_start.get(network_interface, {}).get("rx_bytes", 0)
        tx_start = networks_start.get(network_interface, {}).get("tx_bytes", 0)
        rx_end = networks_end.get(network_interface, {}).get("rx_bytes", 0)
        tx_end = networks_end.get(network_interface, {}).get("tx_bytes", 0)

        print(f"DEBUG: Network RX start: {rx_start} bytes, end: {rx_end} bytes")  # Debugging
        print(f"DEBUG: Network TX start: {tx_start} bytes, end: {tx_end} bytes")  # Debugging

        total_rx = max(rx_end - rx_start, 0) / (1024**2)  # Convert bytes to MB
        total_tx = max(tx_end - tx_start, 0) / (1024**2)  # Convert bytes to MB

        return {
            "total_rx_mb": round(total_rx, 2),
            "total_tx_mb": round(total_tx, 2),
        }

    def analyze_container_performance(
        self,
        container_or_service_id: Optional[str] = None,
        container_or_service_name: Optional[str] = None,
    ) -> dict:
        """Collect data over a time window and compute total resource consumption values."""
        start_time = time.time()
        cpu_cores_samples = []
        ram_usage_samples = []
        disk_usage_samples = []

        # Get initial stats
        start_stat = self.analyzer.get_stats(container_or_service_id, container_or_service_name)

        while (time.time() - start_time) < self.time_window:
            time.sleep(self.period)
            current_stat = self.analyzer.get_stats(
                container_or_service_id, container_or_service_name
            )

            # CPU and RAM usage
            cpu_cores_samples.append(self.get_cpu_cores_used(current_stat))
            ram_usage_samples.append(self.get_ram_usage_mb(current_stat))

            # Disk Usage (instead of R/W speed)
            disk_usage_samples.append(self.analyzer.get_disk_usage(container_or_service_id))

        # Get final stats after the time window
        end_stat = self.analyzer.get_stats(container_or_service_id, container_or_service_name)

        # Compute total network usage
        total_network_usage = self.get_total_network_usage(start_stat, end_stat)

        return {
            "average_cpu_cores": round(mean(cpu_cores_samples), 3),
            "average_ram_usage_mb": round(mean(ram_usage_samples), 2),
            "average_disk_usage_mb": round(mean(disk_usage_samples), 2),
            "total_network_rx_mb": total_network_usage["total_rx_mb"],
            "total_network_tx_mb": total_network_usage["total_tx_mb"],
        }


if __name__ == "__main__":
    analyzer = ContainerizedSystemAnalyzer(time_window=20, period=0.1)
    result = analyzer.analyze_container_performance("0800b9b5426c")

    print(f"Average CPU Usage: {result['average_cpu_cores']} cores")
    print(f"Average RAM Usage: {result['average_ram_usage_mb']} MB")
    print(f"Average Disk Space Used: {result['average_disk_usage_mb']} MB")
    print(f"Total Network RX: {result['total_network_rx_mb']} MB")
    print(f"Total Network TX: {result['total_network_tx_mb']} MB")
