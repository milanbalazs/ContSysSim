"""VM Module.

This module defines the Vm class, which represents a Virtual Machine (VM) in a simulated
Docker Swarm environment using SimPy. VMs host containers and manage resource allocations.
"""

import random
from typing import Optional

import simpy

from container_simulation.computing_model import AbstractBaseModel
from container_simulation.container import Container
from container_simulation.visualizations import Visualisations


class InsufficientResourcesError(Exception):
    """Exception raised when a VM does not have enough resources to run its containers."""

    def __init__(self, message: str) -> None:
        """Initializes the exception with a given message.

        Args:
            message (str): The error message describing the resource issue.
        """
        super().__init__(message)


class Vm(AbstractBaseModel):
    """Represents a Virtual Machine (VM) in a simulated environment.

    A VM is responsible for managing containers, tracking CPU, RAM, Disk, and Bandwidth usage,
    and simulating startup, monitoring, and workload updates. Additionally, it applies random
    saturation fluctuations based on base resource values.

    Attributes:
        env (simpy.Environment): The SimPy environment for event-driven execution.
        id (int): Unique identifier for the VM instance.
        _containers (Optional[list[Container]]): List of containers assigned to this VM.
        running (bool): Indicates whether the VM is running.
        process (simpy.Process): The SimPy process that manages the VM.
        cpu_usage_history (list[float]): Historical CPU usage data for visualization.
        ram_usage_history (list[int]): Historical RAM usage data for visualization.
        disk_usage_history (list[int]): Historical Disk usage data for visualization.
        bw_usage_history (list[int]): Historical Network Bandwidth usage data for visualization.
        available_cpu_history (list[float]): Historical available CPU data for visualization.
        available_ram_history (list[int]): Historical available RAM data for visualization.
        available_disk_history (list[int]): Historical available Disk data for visualization.
        available_bw_history (list[int]): Historical available Network Bandwidth data
                                          for visualization.
        time_history (list[int]): Timestamps for visualization.
    """

    _id: int = 0

    def __init__(
        self,
        env: simpy.Environment,
        name: str,
        cpu: float,
        ram: int,
        disk: int,
        bw: int,
        start_up_delay: float = 0.5,
        containers: Optional[list[Container]] = None,
        cpu_saturation_percent: float = 0.0,
        ram_saturation_percent: float = 0.0,
        disk_saturation_percent: float = 0.0,
        bw_saturation_percent: float = 0.0,
    ) -> None:
        """Initializes a Virtual Machine (VM) with resource limits and optional saturation handling.

        Args:
            env (simpy.Environment): The SimPy environment for event scheduling.
            name (str): The name of the VM.
            cpu (float): The total CPU capacity of the VM.
            ram (int): The total RAM capacity of the VM in MB.
            disk (int): The total Disk capacity of the VM in MB.
            bw (int): The total Network Bandwidth (Data Transfer) capacity of the VM in Mbps.
            start_up_delay (float, optional): The time required for the VM to start.
                                              Default to 0.5.
            containers (Optional[list[Container]], optional): List of containers assigned to the VM.
                                                              Default to None.
            cpu_saturation_percent (float, optional): CPU saturation percentage.
                                                      Default to 0.0.
            ram_saturation_percent (float, optional): RAM saturation percentage.
                                                      Default to 0.0.
            disk_saturation_percent (float, optional): Disk saturation percentage.
                                                       Default to 0.0.
            bw_saturation_percent (float, optional): Bandwidth saturation percentage.
                                                     Default to 0.0.
        """
        super().__init__(
            name,
            cpu,
            ram,
            disk,
            bw,
            start_up_delay,
            cpu_saturation_percent,
            ram_saturation_percent,
            disk_saturation_percent,
            bw_saturation_percent,
        )
        self.env: simpy.Environment = env
        self.id: int = Vm._id
        Vm._id += 1
        self._containers: list[Container] = containers if containers else []
        self.running: bool = False
        self.process: simpy.Process = env.process(self.run())

        # Data storage for visualization
        self.cpu_usage_history: list[float] = []
        self.ram_usage_history: list[int] = []
        self.disk_usage_history: list[int] = []
        self.bw_usage_history: list[int] = []
        self.available_cpu_history: list[float] = []
        self.available_ram_history: list[int] = []
        self.available_disk_history: list[int] = []
        self.available_bw_history: list[int] = []
        self.time_history: list[int] = []

        # Visualisations
        self.visualisations: Visualisations = Visualisations()

    def add_base_saturation(self) -> None:
        """Applies random saturation fluctuations to the VM's available resources.

        Unlike containers, a VM has a fixed total resource allocation. This method ensures
        that fluctuations only affect the available (unused) portion of each resource while
        maintaining the VM's total capacity.

        The fluctuations are applied to:
            - Available CPU Usage (± `cpu_saturation_percent`% of available CPU)
            - Available RAM Usage (± `ram_saturation_percent`% of available RAM)
            - Available Disk Usage (± `disk_saturation_percent`% of available Disk)
            - Available Bandwidth Usage (± `bw_saturation_percent`% of available Bandwidth)

        This ensures that saturation does not increase the total VM resources beyond
        their defined limits.
        """

        cpu_saturation = random.uniform(
            -self.cpu * (self.cpu_saturation_percent / 100),
            self.cpu * (self.cpu_saturation_percent / 100),
        )

        ram_saturation = random.randint(
            -int(self.ram * (self.ram_saturation_percent / 100)),
            int(self.ram * (self.ram_saturation_percent / 100)),
        )

        disk_saturation = random.randint(
            -int(self.disk * (self.disk_saturation_percent / 100)),
            int(self.disk * (self.disk_saturation_percent / 100)),
        )

        bw_saturation = random.randint(
            -int(self.bw * (self.bw_saturation_percent / 100)),
            int(self.bw * (self.bw_saturation_percent / 100)),
        )

        # Apply saturation while ensuring values remain within bounds
        available_cpu = max(0.0, min(self.cpu, self.cpu + cpu_saturation))
        available_ram = max(0, min(self.ram, self.ram + ram_saturation))
        available_disk = max(0, min(self.disk, self.disk + disk_saturation))
        available_bw = max(0, min(self.bw, self.bw + bw_saturation))

        # Store the fluctuated available resources in history
        self.available_cpu_history.append(available_cpu)
        self.available_ram_history.append(available_ram)
        self.available_disk_history.append(available_disk)
        self.available_bw_history.append(available_bw)

    def prevent_resources(self) -> None:
        """Ensures resource values do not drop below zero."""
        self.cpu = max(0.0, self.cpu)
        self.ram = max(0, self.ram)
        self.disk = max(0, self.disk)
        self.bw = max(0, self.bw)

    def store_history(self) -> None:
        """Records current resource usage values for visualization."""
        total_cpu_usage: float = sum(c.current_cpu_usage for c in self._containers)
        total_ram_usage: int = sum(c.current_ram_usage for c in self._containers)
        total_disk_usage: int = sum(c.current_disk_usage for c in self._containers)
        total_bw_usage: int = sum(c.current_bw_usage for c in self._containers)

        self.cpu_usage_history.append(total_cpu_usage)
        self.ram_usage_history.append(total_ram_usage)
        self.disk_usage_history.append(total_disk_usage)
        self.bw_usage_history.append(total_bw_usage)
        self.time_history.append(self.env.now)

        print(
            f"[{self.env.now}] VM '{self.name}' Status - "
            f"Containers: {len(self.containers)}, "
            f"CPU: {format(total_cpu_usage, '.2f')}/{self.available_cpu} "
            f"RAM: {total_ram_usage}/{self.available_ram} "
            f"Disk: {total_disk_usage}/{self.available_disk} "
            f"BW: {total_bw_usage}/{self.available_bw}"
        )

    def check_resources(self) -> None:
        """Checks if the VM has enough CPU and RAM for its running containers.

        Raises:
            InsufficientResourcesError: If the VM runs out of CPU or RAM.
        """
        total_cpu_usage: float = sum(container.current_cpu_usage for container in self._containers)
        total_ram_usage: int = sum(container.current_ram_usage for container in self._containers)
        total_disk_usage: int = sum(container.current_disk_usage for container in self._containers)
        total_bw_usage: int = sum(container.current_bw_usage for container in self._containers)

        if total_cpu_usage > self.available_cpu:
            raise InsufficientResourcesError(
                f"[{self.env.now}] VM '{self.name}' OUT OF CPU: "
                f"Required {total_cpu_usage}, Available {self.available_cpu}"
            )

        if total_ram_usage > self.available_ram:
            raise InsufficientResourcesError(
                f"[{self.env.now}] VM '{self.name}' OUT OF RAM: "
                f"Required {total_ram_usage}, Available {self.available_ram}"
            )

        if total_disk_usage > self.available_disk:
            raise InsufficientResourcesError(
                f"[{self.env.now}] VM '{self.name}' OUT OF Disk: "
                f"Required {total_disk_usage}, Available {self.available_disk}"
            )

        if total_bw_usage > self.available_bw:
            raise InsufficientResourcesError(
                f"[{self.env.now}] VM '{self.name}' OUT OF Network Bandwidth (Data Transfer): "
                f"Required {total_bw_usage}, Available {self.available_bw}"
            )

    def stop(self) -> None:
        """Stops the VM and shuts down all running containers."""
        self.running = False
        print(f"[{self.env.now}] VM '{self.name}' SHUTTING DOWN due to insufficient resources.")
        for container in self._containers:
            container.running = False  # Stop all containers
            print(f"[{self.env.now}] Container '{container.name}' stopped.")

    def start(self) -> simpy.events.Timeout:
        """Simulates VM startup process with a delay and ensures enough resources are available.

        Yields:
            simpy.events.Timeout: A SimPy event representing the startup delay.
        """
        try:
            self.check_resources()
        except InsufficientResourcesError as e:
            print(f"[{self.env.now}] ERROR: {e}")
            return  # Stop VM startup if resources are insufficient

        yield self.env.timeout(self.start_up_delay)  # Simulate startup delay
        self.running = True
        print(f"[{self.env.now}] VM '{self.name}' started.")

        # Start all containers inside this VM
        for container in self._containers:
            self.env.process(container.start())

    def monitor(self) -> simpy.events.Timeout:
        """Continuously monitors the VM's resource usage and logs it for visualization.

        Yields:
            simpy.events.Timeout: A SimPy event representing the monitoring interval.
        """
        while True:
            try:
                self.add_base_saturation()
                self.prevent_resources()
                self.store_history()
                self.check_resources()
            except InsufficientResourcesError as e:
                print(f"[{self.env.now}] ERROR: {e}")
                self.stop()
                return  # Stop monitoring process

            yield self.env.timeout(2)  # Check every 2 time units

    def visualize_usage(self) -> None:
        """Visualizes CPU and RAM usage over time using Matplotlib for a single VM."""
        self.visualisations.visualize_vm_usage(self)

    def run(self) -> simpy.events.Timeout:
        """Runs the VM process and ensures continuous monitoring.

        This method acts as the main event loop for the VM, ensuring that monitoring continues
        while the VM is running.

        Yields:
            simpy.events.Timeout: A SimPy event representing the loop interval.
        """
        while True:
            if self.running:
                self.env.process(self.monitor())  # Ensure monitoring continues
            yield self.env.timeout(1)  # Avoid blocking the event loop

    def visualize_all_containers(self) -> None:
        """Visualizes the CPU and RAM usage of all containers running on this VM.

        This method generates a figure where:
            - Each row represents a container.
            - The left column shows CPU usage over time.
            - The right column shows RAM usage over time.

        The visualization dynamically adjusts the window size based on the number of containers
        while ensuring that the figure remains readable.

        Raises:
            ValueError: If no containers are available to visualize.
        """
        self.visualisations.visualize_all_containers_on_vm(self)

    @property
    def available_ram(self) -> int:
        """Calculates available RAM dynamically based on container usage.

        Returns:
            int: The amount of free RAM available in the VM.
        """
        used_ram: int = sum(c.current_ram_usage for c in self._containers)
        return max(
            0,
            (self.available_ram_history[-1] if self.available_ram_history else self.ram) - used_ram,
        )

    @property
    def available_disk(self) -> int:
        """Calculates available Disk dynamically based on container usage.

        Returns:
            int: The amount of free Disk available in the VM.
        """
        used_disk: int = sum(c.current_disk_usage for c in self._containers)
        return max(
            0,
            (self.available_disk_history[-1] if self.available_disk_history else self.disk)
            - used_disk,
        )

    @property
    def available_bw(self) -> int:
        """
        Calculates available Network Bandwidth (Data Transfer) dynamically based on container usage.

        Returns:
            int: The amount of Network Bandwidth (Data Transfer) available in the VM.
        """
        used_bw: int = sum(c.current_bw_usage for c in self._containers)
        return max(
            0, (self.available_bw_history[-1] if self.available_bw_history else self.bw) - used_bw
        )

    @property
    def available_cpu(self) -> float:
        """Calculates available CPU dynamically based on container usage.

        Returns:
            float: The number of free CPU cores available in the VM.
        """
        used_cpu: float = sum(c.current_cpu_usage for c in self._containers)
        return max(
            0.0,
            (self.available_cpu_history[-1] if self.available_cpu_history else self.cpu) - used_cpu,
        )

    @property
    def containers(self) -> list[Container]:
        """Gets the list of containers assigned to this VM.

        Returns:
            list[Container]: The list of containers running on this VM.
        """
        return self._containers

    @containers.setter
    def containers(self, new_containers: list[Container]) -> None:
        """Assigns a new list of containers to the VM.

        Args:
            new_containers (list[Container]): The new list of containers.
        """
        self._containers = new_containers
