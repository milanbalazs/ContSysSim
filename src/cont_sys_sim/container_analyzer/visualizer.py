"""
Container Resource Usage Visualizer

This module provides functionality for visualizing resource usage data of Docker
containers and Swarm services. It parses a JSON file containing CPU, RAM, Disk,
and Network usage statistics over time and generates plots to analyze trends.

Features:
    - Load resource usage data from a JSON file.
    - Generate time-series plots for CPU, RAM, Disk, and Network usage.
    - Support for multiple containers and services.
    - CLI support for specifying the JSON file dynamically.

Classes:
    - ContainerResourceVisualizer: Loads and visualizes resource usage data.

Functions:
    - main(): Parses CLI arguments and starts the visualization.

Usage Example:
    Run the script with a JSON file path:

    ```
    python container_visualizer.py --json_file path/to/your/json_file.json
    ```

    This will generate plots for each monitored container/service.
"""

import json
import os
import matplotlib.pyplot as plt
from typing import Any, Optional
from logging import Logger

from cont_sys_sim.utils import get_logger

LOGGER: Logger = get_logger()


class ContainerResourceVisualizer:
    """
    Visualizes resource usage for Docker containers or Swarm services.

    Attributes:
        data (dict): Parsed JSON data containing resource usage statistics.
    """

    def __init__(self, data_file: Optional[str] = None, data: Optional[dict] = None) -> None:
        """
        Initializes the visualizer by loading resource usage data.

        Args:
            data_file (Optional[str]): Path to the JSON file containing resource usage data.
            data (Optional[dict]): The data itself.
        """
        if not data_file and not data:
            error_msg: str = "The 'data_file' or 'data' should be set!"
            LOGGER.error(error_msg)
            raise AttributeError(error_msg)
        if data_file and data:
            LOGGER.warning(
                "Both of 'data_file', 'data' parameters are set! " "The Json file will be used!"
            )
        if data_file:
            self.data: dict[str, Any] = self._load_data(data_file)
        else:
            self.data: dict[str, Any] = data

    @staticmethod
    def _load_data(data_file: str) -> dict[str, Any]:
        """
        Loads the JSON resource usage data.

        Args:
            data_file (str): Path to the JSON file containing resource usage data.

        Returns:
            dict: Parsed JSON data.
        """
        if not os.path.exists(data_file):
            error_msg: str = "File '{data_file}' not found."
            LOGGER.error(error_msg)
            raise FileNotFoundError(error_msg)

        with open(data_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def plot_resource_usage(self, entity_name: str) -> None:
        """
        Plots the resource usage (CPU, RAM, Disk, Network RX/TX) for a given entity.

        Args:
            entity_name (str): The name of the container or service.
        """
        if entity_name not in self.data:
            raise ValueError(f"Entity '{entity_name}' not found in data.")

        entity_data: dict[str, Any] = self.data[entity_name]
        metrics: list[tuple[str, str]] = [
            ("cpu_cores_samples", "CPU Usage (Cores)"),
            ("ram_usage_samples", "RAM Usage (MB)"),
            ("disk_usage_samples", "Disk Usage (MB)"),
            ("rx_usage_samples", "Network RX (MB)"),
            ("tx_usage_samples", "Network TX (MB)"),
        ]

        plt.figure(figsize=(10, 6))
        plt.suptitle(f"Resource Usage for {entity_name}", fontsize=14, fontweight="bold")

        for i, (key, label) in enumerate(metrics, start=1):
            plt.subplot(3, 2, i)
            self._plot_single_metric(entity_data, key, label)

        plt.tight_layout(rect=(0.0, 0.0, 1.0, 0.95))
        plt.show()

    @staticmethod
    def _plot_single_metric(entity_data: dict[str, Any], metric_key: str, y_label: str) -> None:
        """
        Plots a single metric (e.g., CPU usage) for a given entity.

        Args:
            entity_data (dict): The resource usage data for the entity.
            metric_key (str): The key representing the metric in the data.
            y_label (str): The label for the Y-axis.
        """
        if metric_key not in entity_data:
            plt.title(f"{y_label} - No Data Available")
            return

        samples: dict = entity_data[metric_key]
        timestamps: list = sorted(samples.keys(), key=float)  # Ensure timestamps are sorted
        values: list = [samples[t] for t in timestamps]

        plt.plot(timestamps, values, marker="o", linestyle="-", markersize=4)
        plt.xlabel("Time (s)")
        plt.ylabel(y_label)
        plt.grid(True)

    def visualize_all(self) -> None:
        """
        Generates plots for all monitored containers/services.
        """
        for entity_name in self.data.keys():
            self.plot_resource_usage(entity_name)


if __name__ == "__main__":
    import argparse

    def main() -> None:
        """
        Parses command-line arguments and runs the visualizer.
        """
        parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Visualize resource usage data for Docker containers or Swarm services."
        )
        parser.add_argument(
            "--json_file",
            type=str,
            help="Path to the JSON file containing resource usage data.",
        )

        args: argparse.Namespace = parser.parse_args()
        json_file_path: str = args.json_file

        try:
            visualizer: ContainerResourceVisualizer = ContainerResourceVisualizer(json_file_path)
            visualizer.visualize_all()
        except Exception as unexpected_error:
            print(f"Error: {unexpected_error}")

    main()
