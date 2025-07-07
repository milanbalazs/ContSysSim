"""Visualization Module.

This module provides the `Visualisations` class, responsible for generating
plots to visualize resource utilization (CPU, RAM, Disk, Bandwidth) of
containers, nodes, and data centers in a simulated Docker Swarm environment.

Classes:
    Visualisations: Handles visualization of CPU, RAM, Disk, and Bandwidth usage
                    for containers, Nodes, and data centers.

Dependencies:
    - matplotlib.pyplot
    - simpy (indirectly)
    - cont_sys_sim.container, cont_sys_sim.node, cont_sys_sim.datacenter (type hints)
"""

from typing import TYPE_CHECKING
import matplotlib.pyplot as plt

# Avoid circular import issues for type hints
if TYPE_CHECKING:
    from cont_sys_sim.container import Container
    from cont_sys_sim.node import Node
    from cont_sys_sim.datacenter import DataCenter


class Visualisations:
    """Handles visualization of CPU, RAM, Disk, and Bandwidth usage for containers and Nodes."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def visualize_all_containers_on_node(node: "Node") -> None:
        """Visualizes CPU, RAM, Disk, and Bandwidth usage for
        all containers on a node in 2x2 layout per container."""
        containers = node.containers
        num_containers = len(containers)

        if num_containers == 0:
            raise ValueError(f"Node '{node.name}' has no running containers to visualize.")

        for container in containers:
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f"Resource Usage for Container: {container.name}", fontsize=16)

            # CPU plot
            ax_cpu = axes[0][0]
            ax_cpu.plot(
                container.time_history,
                container.cpu_usage_history,
                label="CPU Usage",
                marker="o",
                linestyle="-",
            )
            ax_cpu.axhline(
                container.cpu, color="red", linestyle="--", label=f"Max CPU ({container.cpu} core)"
            )
            ax_cpu.set_title("CPU Usage")
            ax_cpu.set_xlabel("Time [sec]")
            ax_cpu.set_ylabel("CPU [core]")
            ax_cpu.legend()

            # RAM plot
            ax_ram = axes[0][1]
            ax_ram.plot(
                container.time_history,
                container.ram_usage_history,
                label="RAM Usage",
                marker="o",
                linestyle="-",
            )
            ax_ram.axhline(
                container.ram, color="red", linestyle="--", label=f"Max RAM ({container.ram} MB)"
            )
            ax_ram.set_title("RAM Usage")
            ax_ram.set_xlabel("Time [sec]")
            ax_ram.set_ylabel("RAM [MB]")
            ax_ram.legend()

            # Disk plot
            ax_disk = axes[1][0]
            ax_disk.plot(
                container.time_history,
                container.disk_usage_history,
                label="Disk Usage",
                marker="o",
                linestyle="-",
            )
            ax_disk.axhline(
                container.disk, color="red", linestyle="--", label=f"Max Disk ({container.disk} MB)"
            )
            ax_disk.set_title("Disk Usage")
            ax_disk.set_xlabel("Time [sec]")
            ax_disk.set_ylabel("Disk [MB]")
            ax_disk.legend()

            # Bandwidth plot
            ax_bw = axes[1][1]
            ax_bw.plot(
                container.time_history,
                container.bw_usage_history,
                label="Bandwidth Usage",
                marker="o",
                linestyle="-",
            )
            ax_bw.axhline(
                container.bw,
                color="red",
                linestyle="--",
                label=f"Max Bandwidth ({container.bw} Mbps)",
            )
            ax_bw.set_title("Bandwidth Usage")
            ax_bw.set_xlabel("Time [sec]")
            ax_bw.set_ylabel("Bandwidth [Mbps]")
            ax_bw.legend()

            plt.tight_layout(rect=(0, 0.03, 1, 0.95))
            plt.show()

    @staticmethod
    def visualize_container_usage(container: "Container") -> None:
        """Visualizes CPU, RAM, Disk, and Bandwidth usage for a single container in 1x4 layout."""
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
            container.cpu, color="red", linestyle="--", label=f"Max CPU ({container.cpu} core)"
        )
        plt.xlabel("Time [sec]")
        plt.ylabel("CPU Usage [core]")
        plt.title(f"CPU Usage: {container.name}")
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
        plt.xlabel("Time [sec]")
        plt.ylabel("RAM Usage [MB]")
        plt.title(f"RAM Usage: {container.name}")
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
        plt.xlabel("Time [sec]")
        plt.ylabel("Disk Usage [MB]")
        plt.title(f"Disk Usage: {container.name}")
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
            container.bw, color="red", linestyle="--", label=f"Max Bandwidth ({container.bw} Mbps)"
        )
        plt.xlabel("Time [sec]")
        plt.ylabel("Bandwidth Usage [Mbps]")
        plt.title(f"Bandwidth Usage: {container.name}")
        plt.legend()

        plt.tight_layout()
        plt.show()

    @staticmethod
    def visualize_node_usage(node: "Node") -> None:
        """Visualizes CPU, RAM, Disk, and Bandwidth usage over time for a single Node."""
        plt.figure(figsize=(20, 5))

        plt.subplot(1, 4, 1)
        plt.plot(
            node.time_history,
            node.cpu_usage_history,
            label="CPU Usage [core]",
            marker="o",
            linestyle="-",
        )
        plt.plot(
            node.time_history,
            node.available_cpu_history,
            label=f"Available CPU (Max. {format(node.cpu, '.2f')} cores)",
            color="red",
            linestyle="-",
        )
        plt.xlabel("Time [sec]")
        plt.ylabel("CPU Usage [core]")
        plt.title(f"CPU Usage for Node: {node.name} [core]")
        plt.legend()

        plt.subplot(1, 4, 2)
        plt.plot(
            node.time_history,
            node.ram_usage_history,
            label="RAM Usage [core]",
            marker="o",
            linestyle="-",
        )
        plt.plot(
            node.time_history,
            node.available_ram_history,
            label=f"Available RAM (Max. {format(node.ram, '.2f')}) [MB]",
            color="red",
            linestyle="-",
        )
        plt.xlabel("Time [ssec]")
        plt.ylabel("RAM Usage (MB)")
        plt.title(f"RAM Usage for Node: {node.name} [MB]")
        plt.legend()

        plt.subplot(1, 4, 3)
        plt.plot(
            node.time_history,
            node.disk_usage_history,
            label="Disk Usage [MB]",
            marker="o",
            linestyle="-",
        )
        plt.plot(
            node.time_history,
            node.available_disk_history,
            label=f"Available Disk (Max. {format(node.disk, '.2f')}) [MB]",
            color="red",
            linestyle="-",
        )
        plt.xlabel("Time [sec]")
        plt.ylabel("Disk Usage (MB)")
        plt.title(f"Disk Usage for Node: {node.name} [MB]")
        plt.legend()

        plt.subplot(1, 4, 4)
        plt.plot(
            node.time_history,
            node.bw_usage_history,
            label="Bandwidth Usage [Mbps]",
            marker="o",
            linestyle="-",
        )
        plt.plot(
            node.time_history,
            node.available_bw_history,
            label=f"Available BW (Max. {format(node.bw, '.2f')}) [Mbps]",
            color="red",
            linestyle="-",
        )
        plt.xlabel("Time [sec]")
        plt.ylabel("Bandwidth Usage [Mbps]")
        plt.title(f"Bandwidth Usage for Node: {node.name} [Mbps]")
        plt.legend()

        plt.tight_layout()
        plt.show()

    @staticmethod
    def visualize_all_nodes_in_datacenter(datacenter: "DataCenter") -> None:
        """Visualizes CPU, RAM, Disk, and Bandwidth usage of all Nodes in a DataCenter,
        with units in labels."""
        nodes: list["Node"] = datacenter.nodes
        num_nodes: int = len(nodes)

        if num_nodes == 0:
            raise ValueError("No Nodes available to visualize.")

        for node in nodes:
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f"Resource Usage for Node: {node.name}", fontsize=16)

            # CPU plot
            ax_cpu = axes[0][0]
            ax_cpu.plot(
                node.time_history,
                node.cpu_usage_history,
                label="CPU Usage",
                marker="o",
                linestyle="-",
            )
            ax_cpu.axhline(
                node.cpu, color="red", linestyle="--", label=f"Max CPU ({node.cpu} core)"
            )
            ax_cpu.set_title("CPU Usage")
            ax_cpu.set_xlabel("Time [sec]")
            ax_cpu.set_ylabel("CPU [core]")
            ax_cpu.legend()

            # RAM plot
            ax_ram = axes[0][1]
            ax_ram.plot(
                node.time_history,
                node.ram_usage_history,
                label="RAM Usage",
                marker="o",
                linestyle="-",
            )
            ax_ram.axhline(node.ram, color="red", linestyle="--", label=f"Max RAM ({node.ram} MB)")
            ax_ram.set_title("RAM Usage")
            ax_ram.set_xlabel("Time [sec]")
            ax_ram.set_ylabel("RAM [MB]")
            ax_ram.legend()

            # Disk plot
            ax_disk = axes[1][0]
            ax_disk.plot(
                node.time_history,
                node.disk_usage_history,
                label="Disk Usage",
                marker="o",
                linestyle="-",
            )
            ax_disk.axhline(
                node.disk, color="red", linestyle="--", label=f"Max Disk ({node.disk} MB)"
            )
            ax_disk.set_title("Disk Usage")
            ax_disk.set_xlabel("Time [sec]")
            ax_disk.set_ylabel("Disk [MB]")
            ax_disk.legend()

            # Bandwidth plot
            ax_bw = axes[1][1]
            ax_bw.plot(
                node.time_history,
                node.bw_usage_history,
                label="Bandwidth Usage",
                marker="o",
                linestyle="-",
            )
            ax_bw.axhline(
                node.bw, color="red", linestyle="--", label=f"Max Bandwidth ({node.bw} Mbps)"
            )
            ax_bw.set_title("Bandwidth Usage")
            ax_bw.set_xlabel("Time [sec]")
            ax_bw.set_ylabel("Bandwidth [Mbps]")
            ax_bw.legend()

            plt.tight_layout(rect=(0, 0.03, 1, 0.95))
            plt.show()
