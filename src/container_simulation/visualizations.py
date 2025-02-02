from typing import TYPE_CHECKING

import matplotlib.pyplot as plt

# Avoid circular import issue
if TYPE_CHECKING:  # Only imported for type hints
    from container_simulation.container import Container
    from container_simulation.vm import Vm
    from container_simulation.datacenter import DataCenter


class Visualisations:
    """Handles visualization of CPU, RAM, and Disk usage for containers and VMs."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def visualize_all_containers_on_vm(vm: "Vm") -> None:
        """Visualizes CPU, RAM, and Disk usage of all containers running on a VM."""
        containers = vm.containers
        num_containers = len(containers)

        if num_containers == 0:
            raise ValueError(f"VM '{vm.name}' has no running containers to visualize.")

        fig, axes = plt.subplots(nrows=num_containers, ncols=4, figsize=(18, 5 * num_containers))

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
    def visualize_vm_usage(vm: "Vm") -> None:
        """Visualizes CPU, RAM, Disk, and Bandwidth usage over time for a single VM."""
        plt.figure(figsize=(20, 5))

        plt.subplot(1, 4, 1)
        plt.plot(
            vm.time_history, vm.cpu_usage_history, label="CPU Usage", marker="o", linestyle="-"
        )
        plt.plot(
            vm.time_history,
            vm.available_cpu_history,
            label=f"Available CPU (Max. {format(vm.cpu, '.2f')})",
            color="red",
            linestyle="-",
        )
        plt.xlabel("Time")
        plt.ylabel("CPU Usage")
        plt.title(f"CPU Usage for VM: {vm.name}")
        plt.legend()

        plt.subplot(1, 4, 2)
        plt.plot(
            vm.time_history, vm.ram_usage_history, label="RAM Usage", marker="o", linestyle="-"
        )
        plt.plot(
            vm.time_history,
            vm.available_ram_history,
            label=f"Available RAM (Max. {format(vm.cpu, '.2f')})",
            color="red",
            linestyle="-",
        )
        plt.xlabel("Time")
        plt.ylabel("RAM Usage (MB)")
        plt.title(f"RAM Usage for VM: {vm.name}")
        plt.legend()

        plt.subplot(1, 4, 3)
        plt.plot(
            vm.time_history, vm.disk_usage_history, label="Disk Usage", marker="o", linestyle="-"
        )
        plt.plot(
            vm.time_history,
            vm.available_disk_history,
            label=f"Available Disk (Max. {format(vm.cpu, '.2f')})",
            color="red",
            linestyle="-",
        )
        plt.xlabel("Time")
        plt.ylabel("Disk Usage (MB)")
        plt.title(f"Disk Usage for VM: {vm.name}")
        plt.legend()

        plt.subplot(1, 4, 4)
        plt.plot(
            vm.time_history, vm.bw_usage_history, label="Bandwidth Usage", marker="o", linestyle="-"
        )
        plt.plot(
            vm.time_history,
            vm.available_bw_history,
            label=f"Available BW (Max. {format(vm.cpu, '.2f')})",
            color="red",
            linestyle="-",
        )
        plt.xlabel("Time")
        plt.ylabel("Bandwidth Usage (Mbps)")
        plt.title(f"Bandwidth Usage for VM: {vm.name}")
        plt.legend()

        plt.tight_layout()
        plt.show()

    @staticmethod
    def visualize_all_vms_in_datacenter(datacenter: "DataCenter") -> None:
        """Visualizes CPU, RAM, and Disk usage of all VMs in a DataCenter."""
        vms: list["Vm"] = datacenter.vms
        num_vms: int = len(vms)

        if num_vms == 0:
            raise ValueError("No VMs available to visualize.")

        plt.figure(figsize=(15, 5 * num_vms))

        for i, vm in enumerate(vms):
            plt.subplot(num_vms, 4, i * 4 + 1)
            plt.plot(
                vm.time_history, vm.cpu_usage_history, label="CPU Usage", marker="o", linestyle="-"
            )
            plt.axhline(
                float(vm.cpu),
                color="red",
                linestyle="--",
                label=f"Max CPU ({format(vm.cpu, '.2f')})",
            )
            plt.xlabel("Time")
            plt.ylabel("CPU Usage")
            plt.title(f"CPU Usage for VM: {vm.name}")
            plt.legend()

            plt.subplot(num_vms, 4, i * 4 + 2)
            plt.plot(
                vm.time_history, vm.ram_usage_history, label="RAM Usage", marker="o", linestyle="-"
            )
            plt.axhline(vm.ram, color="red", linestyle="--", label=f"Max RAM ({vm.ram} MB)")
            plt.xlabel("Time")
            plt.ylabel("RAM Usage (MB)")
            plt.title(f"RAM Usage for VM: {vm.name}")
            plt.legend()

            plt.subplot(num_vms, 4, i * 4 + 3)
            plt.plot(
                vm.time_history,
                vm.disk_usage_history,
                label="Disk Usage",
                marker="o",
                linestyle="-",
            )
            plt.axhline(vm.disk, color="red", linestyle="--", label=f"Max Disk ({vm.disk} MB)")
            plt.xlabel("Time")
            plt.ylabel("Disk Usage (MB)")
            plt.title(f"Disk Usage for VM: {vm.name}")
            plt.legend()

            plt.subplot(num_vms, 4, i * 4 + 4)
            plt.plot(
                vm.time_history,
                vm.bw_usage_history,
                label="Bandwidth Usage",
                marker="o",
                linestyle="-",
            )
            plt.axhline(vm.bw, color="red", linestyle="--", label=f"Max Bandwidth ({vm.bw} Mbps)")
            plt.xlabel("Time")
            plt.ylabel("Bandwidth Usage (Mbps)")
            plt.title(f"Bandwidth Usage for VM: {vm.bw}")
            plt.legend()

        plt.tight_layout()
        plt.show()
