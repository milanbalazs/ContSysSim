"""Visualization Module.

This module provides the `Visualisations` class, which is responsible for generating
various plots to visualize resource utilization (CPU, RAM, Disk, and Bandwidth) of
containers, nodes, and data centers in a simulated Docker Swarm
environment using SimPy.

The class offers multiple static methods to generate time-series plots showing the
historical usage of resources, allowing for better monitoring and analysis of
containerized workloads.

Classes:
    Visualisations: Handles visualization of CPU, RAM, Disk, and Bandwidth usage
                    for containers, Nodes, and data centers.

Example:
    >>> from cont_sys_sim.visualizations import Visualisations
    >>> from cont_sys_sim.container import Container
    >>> import simpy
    >>> env = simpy.Environment()
    >>> container = Container(env, "AppContainer", cpu=2, ram=1024, disk=2048, bw=100)
    >>> container.visualizations.visualize_container_usage(container)

Dependencies:
    - `matplotlib.pyplot` for visualization.
    - `simpy` for simulation environment (indirectly required).
    - `cont_sys_sim.container`, `cont_sys_sim.node`, and
      `cont_sys_sim.datacenter` for type hints.

Notes:
    - The class only contains static methods, so no instance is required.
    - If no containers or Nodes are available for visualization, exceptions are raised.
"""

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt

# Avoid circular import issue
if TYPE_CHECKING:  # Only imported for type hints
    from cont_sys_sim.container import Container
    from cont_sys_sim.node import Node
    from cont_sys_sim.datacenter import DataCenter


class Visualisations:
    """Handles visualization of CPU, RAM, and Disk usage for containers and Nodes."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def visualize_all_containers_on_node(node: "Node") -> None:
        """Visualizes CPU, RAM, and Disk usage of all containers running on a Node."""
        containers = node.containers
        num_containers = len(containers)

        if num_containers == 0:
            raise ValueError(f"Node '{node.name}' has no running containers to visualize.")

        _, axes = plt.subplots(nrows=num_containers, ncols=4, figsize=(18, 5 * num_containers))

        if num_containers == 1:
            axes = [axes]  # Ensure axes is iterable

        for i, container in enumerate(containers):
            axes[i][0].plot(
                container.time_history,
                container.cpu_usage_history,
                label="CPU Usage",
                marker="o",
                linestyle="-",
            )
            axes[i][0].axhline(
                float(container.cpu),
                color="red",
                linestyle="--",
                label=f"Max CPU ({format(container.cpu, '.2f')})",
            )
            axes[i][0].set_xlabel("Time")
            axes[i][0].set_ylabel("CPU Usage")
            axes[i][0].set_title(f"CPU Usage for Container: {container.name}")
            axes[i][0].legend()

            axes[i][1].plot(
                container.time_history,
                container.ram_usage_history,
                label="RAM Usage",
                marker="o",
                linestyle="-",
            )
            axes[i][1].axhline(
                container.ram, color="red", linestyle="--", label=f"Max RAM ({container.ram} MB)"
            )
            axes[i][1].set_xlabel("Time")
            axes[i][1].set_ylabel("RAM Usage (MB)")
            axes[i][1].set_title(f"RAM Usage for Container: {container.name}")
            axes[i][1].legend()

            axes[i][2].plot(
                container.time_history,
                container.disk_usage_history,
                label="Disk Usage",
                marker="o",
                linestyle="-",
            )
            axes[i][2].axhline(
                container.disk, color="red", linestyle="--", label=f"Max Disk ({container.disk} MB)"
            )
            axes[i][2].set_xlabel("Time")
            axes[i][2].set_ylabel("Disk Usage (MB)")
            axes[i][2].set_title(f"Disk Usage for Container: {container.name}")
            axes[i][2].legend()

            axes[i][3].plot(
                container.time_history,
                container.bw_usage_history,
                label="Bandwidth",
                marker="o",
                linestyle="-",
            )
            axes[i][3].axhline(
                container.bw,
                color="red",
                linestyle="--",
                label=f"Max Bandwidth ({container.bw} Mbps)",
            )
            axes[i][3].set_xlabel("Time")
            axes[i][3].set_ylabel("Bandwidth Usage (Mbps)")
            axes[i][3].set_title(f"Bandwidth Usage for Container: {container.bw}")
            axes[i][3].legend()

        plt.tight_layout()
        plt.show()

    @staticmethod
    def visualize_container_usage(container: "Container") -> None:
        """Visualizes CPU, RAM, Disk, and Bandwidth usage over time for a single container."""
        plt.figure(figsize=(20, 5))

        plt.subplot(1, 4, 1)
        plt.plot(
            container.time_history,
            container.cpu_usage_history,
            label="CPU Usage",
            marker="o",
            linestyle="-",
        )
        plt.axhline(
            float(container.cpu),
            color="red",
            linestyle="--",
            label=f"Max CPU ({format(container.cpu, '.2f')})",
        )
        plt.xlabel("Time")
        plt.ylabel("CPU Usage")
        plt.title(f"CPU Usage for Container: {container.name}")
        plt.legend()

        plt.subplot(1, 4, 2)
        plt.plot(
            container.time_history,
            container.ram_usage_history,
            label="RAM Usage",
            marker="o",
            linestyle="-",
        )
        plt.axhline(
            container.ram, color="red", linestyle="--", label=f"Max RAM ({container.ram} MB)"
        )
        plt.xlabel("Time")
        plt.ylabel("RAM Usage (MB)")
        plt.title(f"RAM Usage for Container: {container.name}")
        plt.legend()

        plt.subplot(1, 4, 3)
        plt.plot(
            container.time_history,
            container.disk_usage_history,
            label="Disk Usage",
            marker="o",
            linestyle="-",
        )
        plt.axhline(
            container.disk, color="red", linestyle="--", label=f"Max Disk ({container.disk} MB)"
        )
        plt.xlabel("Time")
        plt.ylabel("Disk Usage (MB)")
        plt.title(f"Disk Usage for Container: {container.name}")
        plt.legend()

        plt.subplot(1, 4, 4)
        plt.plot(
            container.time_history,
            container.bw_usage_history,
            label="Bandwidth Usage",
            marker="o",
            linestyle="-",
        )
        plt.axhline(
            container.bw, color="red", linestyle="--", label=f"Max BW ({container.bw} Mbps)"
        )
        plt.xlabel("Time")
        plt.ylabel("Bandwidth Usage (Mbps)")
        plt.title(f"Bandwidth Usage for Container: {container.name}")
        plt.legend()

        plt.tight_layout()
        plt.show()

    @staticmethod
    def visualize_node_usage(node: "Node") -> None:
        """Visualizes CPU, RAM, Disk, and Bandwidth usage over time for a single Node."""
        plt.figure(figsize=(20, 5))

        plt.subplot(1, 4, 1)
        plt.plot(
            node.time_history, node.cpu_usage_history, label="CPU Usage", marker="o", linestyle="-"
        )
        plt.plot(
            node.time_history,
            node.available_cpu_history,
            label=f"Available CPU (Max. {format(node.cpu, '.2f')})",
            color="red",
            linestyle="-",
        )
        plt.xlabel("Time")
        plt.ylabel("CPU Usage")
        plt.title(f"CPU Usage for Node: {node.name}")
        plt.legend()

        plt.subplot(1, 4, 2)
        plt.plot(
            node.time_history, node.ram_usage_history, label="RAM Usage", marker="o", linestyle="-"
        )
        plt.plot(
            node.time_history,
            node.available_ram_history,
            label=f"Available RAM (Max. {format(node.ram, '.2f')})",
            color="red",
            linestyle="-",
        )
        plt.xlabel("Time")
        plt.ylabel("RAM Usage (MB)")
        plt.title(f"RAM Usage for Node: {node.name}")
        plt.legend()

        plt.subplot(1, 4, 3)
        plt.plot(
            node.time_history,
            node.disk_usage_history,
            label="Disk Usage",
            marker="o",
            linestyle="-",
        )
        plt.plot(
            node.time_history,
            node.available_disk_history,
            label=f"Available Disk (Max. {format(node.disk, '.2f')})",
            color="red",
            linestyle="-",
        )
        plt.xlabel("Time")
        plt.ylabel("Disk Usage (MB)")
        plt.title(f"Disk Usage for Node: {node.name}")
        plt.legend()

        plt.subplot(1, 4, 4)
        plt.plot(
            node.time_history,
            node.bw_usage_history,
            label="Bandwidth Usage",
            marker="o",
            linestyle="-",
        )
        plt.plot(
            node.time_history,
            node.available_bw_history,
            label=f"Available BW (Max. {format(node.bw, '.2f')})",
            color="red",
            linestyle="-",
        )
        plt.xlabel("Time")
        plt.ylabel("Bandwidth Usage (Mbps)")
        plt.title(f"Bandwidth Usage for Node: {node.name}")
        plt.legend()

        plt.tight_layout()
        plt.show()

    @staticmethod
    def visualize_all_nodes_in_datacenter(datacenter: "DataCenter") -> None:
        """Visualizes CPU, RAM, and Disk usage of all Nodes in a DataCenter."""
        nodes: list["Node"] = datacenter.nodes
        num_nodes: int = len(nodes)

        if num_nodes == 0:
            raise ValueError("No Nodes available to visualize.")

        plt.figure(figsize=(15, 5 * num_nodes))

        for i, node in enumerate(nodes):
            plt.subplot(num_nodes, 4, i * 4 + 1)
            plt.plot(
                node.time_history,
                node.cpu_usage_history,
                label="CPU Usage",
                marker="o",
                linestyle="-",
            )
            plt.axhline(
                float(node.cpu),
                color="red",
                linestyle="--",
                label=f"Max CPU ({format(node.cpu, '.2f')})",
            )
            plt.xlabel("Time")
            plt.ylabel("CPU Usage")
            plt.title(f"CPU Usage for Node: {node.name}")
            plt.legend()

            plt.subplot(num_nodes, 4, i * 4 + 2)
            plt.plot(
                node.time_history,
                node.ram_usage_history,
                label="RAM Usage",
                marker="o",
                linestyle="-",
            )
            plt.axhline(node.ram, color="red", linestyle="--", label=f"Max RAM ({node.ram} MB)")
            plt.xlabel("Time")
            plt.ylabel("RAM Usage (MB)")
            plt.title(f"RAM Usage for Node: {node.name}")
            plt.legend()

            plt.subplot(num_nodes, 4, i * 4 + 3)
            plt.plot(
                node.time_history,
                node.disk_usage_history,
                label="Disk Usage",
                marker="o",
                linestyle="-",
            )
            plt.axhline(node.disk, color="red", linestyle="--", label=f"Max Disk ({node.disk} MB)")
            plt.xlabel("Time")
            plt.ylabel("Disk Usage (MB)")
            plt.title(f"Disk Usage for Node: {node.name}")
            plt.legend()

            plt.subplot(num_nodes, 4, i * 4 + 4)
            plt.plot(
                node.time_history,
                node.bw_usage_history,
                label="Bandwidth Usage",
                marker="o",
                linestyle="-",
            )
            plt.axhline(
                node.bw, color="red", linestyle="--", label=f"Max Bandwidth ({node.bw} Mbps)"
            )
            plt.xlabel("Time")
            plt.ylabel("Bandwidth Usage (Mbps)")
            plt.title(f"Bandwidth Usage for Node: {node.name}")
            plt.legend()

        plt.tight_layout()
        plt.show()
