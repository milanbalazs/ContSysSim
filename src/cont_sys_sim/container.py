"""Container Module.

This module defines the `Container` class, which represents a container running inside
a Node in a simulated Docker Swarm environment using SimPy.

Containers consume CPU, RAM, Disk, and Bandwidth resources while dynamically updating
their workload over time. They may also experience resource fluctuations due to
random fluctuation effects.

Classes:
    Container: Represents a container running in a Node with dynamic resource consumption.

Example:
    Creating a container and assigning a workload request:

    >>> from cont_sys_sim.container import Container
    >>> from cont_sys_sim.workload_request import WorkloadRequest
    >>> import simpy
    >>> env = simpy.Environment()
    >>> container = Container(env, "MyContainer", cpu=2, ram=1024, disk=2048, bw=100)
    >>> workload = WorkloadRequest(cpu=1.0, ram=512, disk=1024, bw=50, delay=2.0, duration=10.0,
    ...                           cpu_fluctuation_percent=5.0, ram_fluctuation_percent=3.0,
    ...                           disk_fluctuation_percent=2.0, bw_fluctuation_percent=4.0)
    >>> container.add_workload_request(workload)
    >>> env.run(until=15)

Attributes:
    _id (int): A class-level identifier counter for containers, ensuring unique IDs.
"""

import random
from logging import Logger
from typing import Optional

import simpy

from cont_sys_sim.computing_model import AbstractBaseModel
from cont_sys_sim.visualizations import Visualisations
from cont_sys_sim.workload_request import WorkloadRequest
from cont_sys_sim.utils import get_logger  # Import singleton logger


class Container(AbstractBaseModel):
    """Represents a container in a simulated environment.

    A container runs inside a Node and consumes CPU, RAM, Disk,
    and Bandwidth resources.
    It has a startup delay before becoming active and updates its workload dynamically.

    Attributes:
        env (simpy.Environment): The SimPy environment for event-driven execution.
        id (int): Unique identifier for the container instance.
        current_cpu_usage (float): The current CPU usage of the container.
        current_ram_usage (int): The current RAM usage of the container in MB.
        current_disk_usage (int): The current Disk usage of the container in MB.
        current_bw_usage (int): The current Network Bandwidth (Data Transfer)
                                usage of the container in Mbps.
        running (bool): Indicates whether the container is active.
        process (simpy.Process): The SimPy process that manages the container workload.
        cpu_usage_history (list[int]): Historical CPU usage data for visualization.
        ram_usage_history (list[int]): Historical RAM usage data for visualization.
        disk_usage_history (list[int]): Historical Disk usage data for visualization.
        bw_usage_history (list[int]): Historical Bandwidth usage data for visualization.
        time_history (list[int]): Timestamps for visualization.
        workload_requests (dict[int | float, list[WorkloadRequest]]): A dictionary
            mapping the simulation time to a list of workload requests.
        _logger (Optional[Logger]): Logger object.
    """

    _id: int = 0  # Class-level identifier counter for containers

    def __init__(
        self,
        env: simpy.Environment,
        name: str,
        cpu: float,
        ram: int,
        disk: int,
        bw: int,
        start_up_delay: float = 0.9,
        cpu_fluctuation_percent: float = 0.0,
        ram_fluctuation_percent: float = 0.0,
        disk_fluctuation_percent: float = 0.0,
        bw_fluctuation_percent: float = 0.0,
        logger: Optional[Logger] = None,
    ) -> None:
        """Initializes a Container instance."""
        super().__init__(
            name,
            cpu,
            ram,
            disk,
            bw,
            start_up_delay,
            cpu_fluctuation_percent,
            ram_fluctuation_percent,
            disk_fluctuation_percent,
            bw_fluctuation_percent,
        )
        self._logger = logger if logger else get_logger()  # Use shared logger
        self.env: simpy.Environment = env
        self.id: int = Container._id
        Container._id += 1
        self.current_cpu_usage: float = 0  # Start with zero CPU usage
        self.current_ram_usage: int = 0  # Start with zero RAM usage
        self.current_disk_usage: int = 0  # Start with zero Disk usage
        self.current_bw_usage: int = 0  # Start with zero Bandwidth usage
        self.running: bool = False  # Track container state
        self.process: simpy.Process = env.process(self.run())  # Start workload updates

        # Data storage for visualization
        self.cpu_usage_history: list[float] = []
        self.ram_usage_history: list[int] = []
        self.disk_usage_history: list[int] = []
        self.bw_usage_history: list[int] = []
        self.time_history: list[int] = []

        # Visualisations
        self.visualisations: Visualisations = Visualisations()

        # Workload
        self.workload_requests: dict[int | float, list[WorkloadRequest]] = {}

    def add_workload_request(self, workload_request: WorkloadRequest):
        """Adds a new workload request to the container.

        Args:
            workload_request (WorkloadRequest): The workload request to be added.
        """
        # Check if the workload is already assigned
        for workloads in self.workload_requests.values():
            if workload_request in workloads:
                self._logger.info(
                    f"[{self.env.now}] Workload '{workload_request.id}' "
                    f"({workload_request.workload_type}) "
                    f"is already assigned to {self.name} Container, skipping."
                )
                return  # Skip duplicate assignment

        self._logger.info(
            f"[{self.env.now}] Assign '{workload_request.id}' ({workload_request.workload_type}) "
            f"Workload to {self.name} Container"
        )
        if self.env.now in self.workload_requests:
            self.workload_requests[self.env.now].append(workload_request)
        else:
            self.workload_requests[self.env.now] = [workload_request]

    def start(self) -> simpy.events.Timeout:
        """Simulates the container startup process with a delay.

        The container remains inactive until the startup delay is completed.

        Yields:
            simpy.events.Timeout: A SimPy event representing the startup delay.
        """
        yield self.env.timeout(self.start_up_delay)  # Wait for start-up delay
        self.running = True
        self._logger.info(f"[{self.env.now}] Container '{self.name}' started.")

    def add_base_fluctuation(self) -> None:
        """Applies random fluctuation fluctuations based on base resource values.

        This method modifies the current resource usage by applying a random fluctuation
        based on a percentage of the base resource values. The fluctuation range is
        determined by the corresponding fluctuation percentage for each resource.

        The fluctuations are applied to:
            - CPU Usage (± `cpu_fluctuation_percent`% of `cpu`)
            - RAM Usage (± `ram_fluctuation_percent`% of `ram`)
            - Disk Usage (± `disk_fluctuation_percent`% of `disk`)
            - Bandwidth Usage (± `bw_fluctuation_percent`% of `bw`)
        """
        self.current_cpu_usage += random.uniform(
            -self.cpu * (self.cpu_fluctuation_percent / 100),
            self.cpu * (self.cpu_fluctuation_percent / 100),
        )
        self.current_ram_usage += random.randint(
            -int(self.ram * (self.ram_fluctuation_percent / 100)),
            int(self.ram * (self.ram_fluctuation_percent / 100)),
        )
        self.current_disk_usage += random.randint(
            -int(self.disk * (self.disk_fluctuation_percent / 100)),
            int(self.disk * (self.disk_fluctuation_percent / 100)),
        )
        self.current_bw_usage += random.randint(
            -int(self.bw * (self.bw_fluctuation_percent / 100)),
            int(self.bw * (self.bw_fluctuation_percent / 100)),
        )

    def prevent_resources(self) -> None:
        """Ensures resource values do not drop below zero.

        This method prevents resource usage values from becoming negative after
        applying fluctuation fluctuations or workload adjustments. It enforces
        a minimum limit of `0` for all resources.
        """
        self.current_cpu_usage = max(0.0, self.current_cpu_usage)
        self.current_ram_usage = max(0, self.current_ram_usage)
        self.current_disk_usage = max(0, self.current_disk_usage)
        self.current_bw_usage = max(0, self.current_bw_usage)

    def store_history(self) -> None:
        """Records current resource usage values for visualization.

        This method appends the current usage of CPU, RAM, Disk, and Bandwidth
        to their respective history lists. It also logs the current simulation
        time for time-series analysis.
        """
        self.cpu_usage_history.append(self.current_cpu_usage)
        self.ram_usage_history.append(self.current_ram_usage)
        self.disk_usage_history.append(self.current_disk_usage)
        self.bw_usage_history.append(self.current_bw_usage)
        self.time_history.append(self.env.now)

    def stop(self) -> None:
        """Gracefully stops the container and resets resource usage.

        This method stops the container, deactivates all workloads, and resets
        resource usage to ensure the container is in a clean state.
        """
        if not self.running:
            self._logger.warning(f"[{self.env.now}] Container '{self.name}' is already stopped.")
            return

        self.running = False
        self._logger.info(f"[{self.env.now}] Container '{self.name}' is stopping gracefully.")

        # Deactivate all active workloads
        for workloads in self.workload_requests.values():
            for workload in workloads:
                if workload.active:
                    self._logger.info(
                        f"[{self.env.now}] {workload.id} ({workload.workload_type}) is stopping."
                    )
                    self.current_cpu_usage -= workload.current_cpu_workload
                    self.current_ram_usage -= workload.current_ram_workload
                    self.current_disk_usage -= workload.current_disk_workload
                    self.current_bw_usage -= workload.current_bw_workload
                    workload.active = False

        # Reset resource usage
        self.current_cpu_usage = 0
        self.current_ram_usage = 0
        self.current_disk_usage = 0
        self.current_bw_usage = 0

        self._logger.info(f"[{self.env.now}] Container '{self.name}' stopped. Resources reset.")

    def run(self) -> simpy.events.Timeout:
        """SimPy process that updates workload every time unit.

        Simulates dynamic resource consumption by adjusting CPU and RAM usage based on
        active workloads.

        Yields:
            simpy.events.Timeout: A SimPy event representing the workload update interval.
        """
        while True:
            if not self.running:
                self._logger.info(f"[{self.env.now}] {self.name} Container is not running.")
                yield self.env.timeout(1)
            self._logger.debug(
                f"Time {self.env.now}: {self.name} Running: {self.running} - "
                f"CPU={self.current_cpu_usage}/{self.cpu}, "
                f"RAM={self.current_ram_usage}/{self.ram}, "
                f"Disk={self.current_disk_usage}/{self.disk}, "
                f"BW={self.current_bw_usage}/{self.bw}"
            )

            if self.running:
                old_cpu_usage: float = self.current_cpu_usage
                old_ram_usage: int = self.current_ram_usage
                old_disk_usage: int = self.current_disk_usage
                old_bw_usage: int = self.current_bw_usage

                # Iterate over a copy of workload_requests to safely modify the dictionary
                for receive_time, workload_requests in list(self.workload_requests.items()):
                    # Use a separate list to track completed workloads
                    completed_workloads = []

                    for workload_request in workload_requests:
                        start_time = receive_time + workload_request.delay
                        end_time = start_time + workload_request.duration

                        # Workload is active
                        if start_time <= self.env.now < end_time and not workload_request.active:
                            self.current_cpu_usage += workload_request.current_cpu_workload
                            self.current_ram_usage += workload_request.current_ram_workload
                            self.current_disk_usage += workload_request.current_disk_workload
                            self.current_bw_usage += workload_request.current_bw_workload
                            workload_request.active = True

                        # Workload should stop (duration has ended)
                        elif self.env.now >= end_time and workload_request.active:
                            self.current_cpu_usage -= workload_request.current_cpu_workload
                            self.current_ram_usage -= workload_request.current_ram_workload
                            self.current_disk_usage -= workload_request.current_disk_workload
                            self.current_bw_usage -= workload_request.current_bw_workload
                            workload_request.active = False
                            completed_workloads.append(workload_request)  # Mark for removal

                        # The workload is running, apply fluctuation (fluctuation)
                        else:
                            self.current_cpu_usage += workload_request.current_cpu_fluctuation
                            self.current_ram_usage += workload_request.current_ram_fluctuation
                            self.current_disk_usage += workload_request.current_disk_fluctuation
                            self.current_bw_usage += workload_request.current_bw_fluctuation

                    # Remove completed workloads from the list
                    for workload in completed_workloads:
                        workload_requests.remove(workload)

                    # If no workloads are left at this timestamp, delete the key from the dictionary
                    if not workload_requests:
                        del self.workload_requests[receive_time]

                self.add_base_fluctuation()
                self.prevent_resources()
                self.store_history()

                self._logger.info(
                    f"[{self.env.now}] Container '{self.name}' updated workload: "
                    f"CPU {format(old_cpu_usage, '.2f')}/{format(self.cpu, '.2f')} --> "
                    f"{format(self.current_cpu_usage, '.2f')}/{format(self.cpu, '.2f')}, "
                    f"RAM {old_ram_usage}/{self.ram} --> {self.current_ram_usage}/{self.ram}, "
                    f"Disk {old_disk_usage}/{self.disk} --> {self.current_disk_usage}/{self.disk}, "
                    f"Disk {old_bw_usage}/{self.bw} --> {self.current_bw_usage}/{self.bw}"
                )

            yield self.env.timeout(1)  # Update workload every time unit

    def visualize_usage(self) -> None:
        """Visualizes CPU and RAM usage over time using Matplotlib.

        This method uses the `Visualisations` class to plot historical usage
        statistics for analysis.
        """
        self.visualisations.visualize_container_usage(self)

    @property
    def available_bw(self) -> int:
        """
        Calculates available Network Bandwidth (Data Transfer) dynamically based on container usage.

        Returns:
            int: The amount of Network Bandwidth (Data Transfer) available in the Node.
        """

        return max(0, self.bw - self.current_bw_usage)

    @property
    def available_cpu(self) -> float:
        """Calculates available CPU dynamically based on container usage.

        Returns:
            float: The number of free CPU cores available in the Node.
        """

        return max(
            0.0,
            self.cpu - self.current_cpu_usage,
        )

    @property
    def available_ram(self) -> int:
        """Calculates available RAM dynamically based on container usage.

        Returns:
            int: The amount of free RAM available in the Node.
        """

        return max(0, self.ram - self.current_ram_usage)

    @property
    def available_disk(self) -> int:
        """Calculates available Disk dynamically based on container usage.

        Returns:
            int: The amount of free Disk available in the Node.
        """
        return max(0, self.disk - self.current_disk_usage)

    @property
    def logger(self) -> Logger:
        """Gets the logger of the container.

        Returns:
            str: The logger of the container.
        """
        return self._logger

    @logger.setter
    def logger(self, new_logger: Logger) -> None:
        """Sets a logger name for the container.

        Args:
            new_logger (str): The new logger to be assigned.
        """
        self._logger = new_logger
