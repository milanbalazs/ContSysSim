"""Simulation Module.

This module defines the Simulation class, which simulates a Docker Swarm-like
environment using SimPy. It manages a DataCenter with Virtual Machines (VMs)
and Containers, simulating their startup and workload behavior over time.
"""

from typing import Optional
from logging import Logger

import simpy

from container_simulation.datacenter import DataCenter
from container_simulation.utils import get_logger


class Simulation:
    """Represents a Docker Swarm simulation using SimPy.

    The Simulation class initializes a data center with manager and database VMs,
    assigns common containers to them, and runs a time-based simulation.

    Attributes:
        _env (simpy.Environment): The SimPy environment managing event-driven execution.
        _datacenter (Optional[DataCenter]): The data center managing all VMs.
    """

    def __init__(self) -> None:
        """Initializes the Simulation instance.

        Creates a SimPy environment for event-driven execution. The data center
        is initially set to `None` and must be assigned before running the simulation.
        """
        self._env: simpy.Environment = simpy.Environment()  # Create a SimPy environment
        self._datacenter: Optional[DataCenter] = None
        self._logger: Logger = get_logger()

    def run(self, datacenter: Optional[DataCenter] = None, simulation_time: int = 20) -> None:
        """Starts the simulation by running VMs and monitoring their status.

        The simulation runs for a specified time, during which VMs and containers
        undergo startup delays and dynamic workload updates.

        Args:
            datacenter (Optional[DataCenter]): The data center containing VMs and containers.
                If not provided, the existing `_datacenter` attribute is used.
            simulation_time (int, optional): The total time to run the simulation.
                Defaults to `20` time units.

        Raises:
            RuntimeError: If no data center is assigned to the simulation.
        """

        if not datacenter and not self._datacenter:
            raise RuntimeError("Datacenter is not defined!")

        self._datacenter = datacenter or self._datacenter

        for vm in self._datacenter.vms:
            self._env.process(vm.start())  # Start VM processes
            self._env.process(vm.monitor())  # Start monitoring

        self._env.run(until=simulation_time)  # Run simulation for X time units

    def print_info(self) -> None:
        """Prints a summary of the simulated data center's resources.

        This method provides an overview of the data center, including:
        - The total number of Virtual Machines (VMs).
        - The CPU, RAM, and Disk capacity of each VM.
        - The available (free) CPU, RAM, and Disk for each VM.
        - A list of assigned Containers and their resource allocations.

        Example Output:
            ==========================================
             Datacenter: CLOUD_ENVIRONMENT
            ==========================================
            Total VMs: 3

            --------------------------------------------------
             VM: manager-1
            --------------------------------------------------
             CPU: 8.0 Cores | Available CPU: 2.5
             RAM: 16384 MB  | Available RAM: 8192
             DISK: 20480 MB | Available Disk: 10240
            --------------------------------------------------
               Containers:
               ----------------------------------------
               • nginx-container   | CPU: 2  | RAM: 512 MB | Disk: 2048
               • db-container      | CPU: 4  | RAM: 1024 MB | Disk: 4096
               ----------------------------------------

        This function prints the output directly to the console.
        """

        summary: list[str] = [
            "\n",
            "=" * 50,
            f" Datacenter: {self._datacenter.name.upper()} ".center(50, "="),
            "=" * 50,
            f"Total VMs: {len(self._datacenter.vms)}\n",
        ]

        for vm in self._datacenter.vms:
            summary.append("-" * 50)
            summary.append(f" VM: {vm.name} ".center(50, "-"))
            summary.append(f" CPU: {vm.cpu} Cores | Available CPU: {vm.available_cpu:.2f}")
            summary.append(f" RAM: {vm.ram} MB | Available RAM: {vm.available_ram} MB")
            summary.append(f" DISK: {vm.disk} MB | Available Disk: {vm.available_disk} MB")
            summary.append("-" * 50)

            if vm.containers:
                summary.append("   Containers:")
                summary.append("   " + "-" * 40)
                for container in vm.containers:
                    summary.append(
                        f"   • {container.name:<15} | "
                        f"CPU: {container.cpu:<2} | "
                        f"RAM: {container.ram} MB | "
                        f"Disk: {container.disk} MB"
                    )
                summary.append("   " + "-" * 40)
            else:
                summary.append("   No Containers Assigned.")

        summary.append("=" * 50)
        summary.append(" Simulation Summary Complete ")
        summary.append("=" * 50)

        # Join all the strings and log the full summary
        self._logger.info("\n".join(summary))

    @property
    def env(self) -> simpy.Environment:
        """Gets the SimPy environment.

        Returns:
            simpy.Environment: The current simulation environment.
        """
        return self._env

    @env.setter
    def env(self, new_env: simpy.Environment) -> None:
        """Sets a new SimPy environment.

        Args:
            new_env (simpy.Environment): The new SimPy environment instance.
        """
        self._env = new_env

    @property
    def datacenter(self) -> DataCenter:
        """Gets the assigned data center.

        Returns:
            DataCenter: The current data center instance managing VMs and containers.
        """
        return self._datacenter

    @datacenter.setter
    def datacenter(self, new_datacenter: DataCenter) -> None:
        """Sets a new data center.

        Args:
            new_datacenter (DataCenter): The new data center instance.
        """
        self._datacenter = new_datacenter

    @property
    def logger(self) -> Logger:
        """Gets the logger of the Simulation.

        Returns:
            str: The logger of the Simulation.
        """
        return self._logger

    @logger.setter
    def logger(self, new_logger: Logger) -> None:
        """Sets a logger name for the Simulation.

        Args:
            new_logger (str): The new logger to be assigned.
        """
        self._logger = new_logger
