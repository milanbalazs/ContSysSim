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

    def get_disk_io_mb(self, current_stat: dict, previous_stat: dict) -> dict:
        """Calculate disk read/write speed in MB per second."""
        t1 = self.parse_timestamp(current_stat["read"])
        t0 = self.parse_timestamp(previous_stat["read"])
        delta_t = (t1 - t0).total_seconds()

        if delta_t <= 0:
            return {"read_speed_mbps": 0.0, "write_speed_mbps": 0.0}

        # Get disk I/O values safely
        def get_disk_value(stats, op):
            return (
                sum(
                    item["value"]
                    for item in stats.get("io_service_bytes_recursive", [])
                    if item["op"] == op
                )
                if stats.get("io_service_bytes_recursive")
                else 0
            )

        read_bytes_now = get_disk_value(current_stat["blkio_stats"], "read")
        write_bytes_now = get_disk_value(current_stat["blkio_stats"], "write")

        read_bytes_prev = get_disk_value(previous_stat["blkio_stats"], "read")
        write_bytes_prev = get_disk_value(previous_stat["blkio_stats"], "write")

        read_speed = (read_bytes_now - read_bytes_prev) / (1024**2 * delta_t)  # Convert to MB/s
        write_speed = (write_bytes_now - write_bytes_prev) / (
            1024**2 * delta_t
        )  # Convert to MB/s

        return {
            "read_speed_mbps": round(read_speed, 2),
            "write_speed_mbps": round(write_speed, 2),
        }

    def get_network_bandwidth_mb(self, current_stat: dict, previous_stat: dict) -> dict:
        """Calculate network receive and transmit speed in MB per second."""
        t1 = self.parse_timestamp(current_stat["read"])
        t0 = self.parse_timestamp(previous_stat["read"])
        delta_t = (t1 - t0).total_seconds()

        if delta_t <= 0:
            return {"rx_speed_mbps": 0.0, "tx_speed_mbps": 0.0}

        rx_bytes_now = current_stat["networks"]["eth0"]["rx_bytes"]
        tx_bytes_now = current_stat["networks"]["eth0"]["tx_bytes"]

        rx_bytes_prev = previous_stat["networks"]["eth0"]["rx_bytes"]
        tx_bytes_prev = previous_stat["networks"]["eth0"]["tx_bytes"]

        rx_speed = (rx_bytes_now - rx_bytes_prev) / (1024**2 * delta_t)  # Convert to MB/s
        tx_speed = (tx_bytes_now - tx_bytes_prev) / (1024**2 * delta_t)  # Convert to MB/s

        return {
            "rx_speed_mbps": round(rx_speed, 2),
            "tx_speed_mbps": round(tx_speed, 2),
        }

    def analyze_container_performance(
        self,
        container_or_service_id: Optional[str] = None,
        container_or_service_name: Optional[str] = None,
    ) -> dict:
        """Collect data over a time window and compute average exact resource consumption values."""
        start_time = time.time()
        cpu_cores_samples = []
        ram_usage_samples = []
        disk_usage_samples = []
        net_rx_samples = []
        net_tx_samples = []

        previous_stat = self.analyzer.get_stats(container_or_service_id, container_or_service_name)

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

            # Network Bandwidth
            net_bw = self.get_network_bandwidth_mb(current_stat, previous_stat)

            net_rx_samples.append(net_bw["rx_speed_mbps"])
            net_tx_samples.append(net_bw["tx_speed_mbps"])

            previous_stat = current_stat  # Update previous stat for next iteration

        return {
            "average_cpu_cores": round(mean(cpu_cores_samples), 3),
            "average_ram_usage_mb": round(mean(ram_usage_samples), 2),
            "average_disk_usage_mb": round(mean(disk_usage_samples), 2),
            "average_network_rx_mbps": round(mean(net_rx_samples), 2),
            "average_network_tx_mbps": round(mean(net_tx_samples), 2),
        }


if __name__ == "__main__":
    analyzer = ContainerizedSystemAnalyzer(time_window=20, period=0.1)
    result = analyzer.analyze_container_performance("0800b9b5426c")

    print(f"Average CPU Usage: {result['average_cpu_cores']} cores")
    print(f"Average RAM Usage: {result['average_ram_usage_mb']} MB")
    print(f"Average Disk Space Used: {result['average_disk_usage_mb']} MB")
    print(f"Average Network RX Speed: {result['average_network_rx_mbps']} MB/s")
    print(f"Average Network TX Speed: {result['average_network_tx_mbps']} MB/s")
