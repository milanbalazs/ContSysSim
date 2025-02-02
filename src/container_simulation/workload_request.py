from typing import Optional
import random


class WorkloadRequest:
    """Represents a task (workload) that consumes CPU and RAM within a container.

    Attributes:
        id (str): Unique identifier for the workload request.
        cpu (float): Base CPU requirement for the workload.
        ram (int): Base RAM requirement in MB.
        disk (int): Base Disk requirement in MB.
        bw (int): Base Network Bandwidth (Data Transfer) requirement in Mbps.
        delay (float): Time before the workload starts execution.
        duration (float): Time for which the workload remains active.
        cpu_saturation_percent (float): Variability in CPU usage (+/- percentage).
        ram_saturation_percent (float): Variability in RAM usage (+/- percentage).
        disk_saturation_percent (float): Variability in Disk usage (+/- percentage).
        bw_saturation_percent (float): Variability in Network Bandwidth (Data Transfer) usage (+/- percentage).
        priority (int, optional): Priority level of the workload (higher = more important).
        workload_type (str, optional): Type of workload (e.g., "User Request", "Background Task").
    """

    _id = 0

    def __init__(
        self,
        cpu: float,
        ram: int,
        disk: int,
        bw: int,
        delay: float,
        duration: float,
        cpu_saturation_percent: float,
        ram_saturation_percent: float,
        disk_saturation_percent: float,
        bw_saturation_percent: float,
        priority: Optional[int] = None,
        workload_type: Optional[str] = None,
    ) -> None:
        """Initializes a WorkloadRequest.

        Args:
            cpu (float): Base CPU requirement for the workload.
            ram (int): Base RAM requirement in MB.
            disk (int): Base Disk requirement in MB.
            disk (int): Base Network Bandwidth (Data Transfer) requirement in Mbps.
            delay (float): Time before the workload starts execution.
            duration (float): Time for which the workload remains active.
            cpu_saturation_percent (float): Variability in CPU usage (+/- percentage).
            ram_saturation_percent (float): Variability in RAM usage (+/- percentage).
            disk_saturation_percent (float): Variability in Disk usage (+/- percentage).
            bw_saturation_percent (float): Variability in Network Bandwidth (Data Transfer) usage (+/- percentage).
            priority (Optional[int], optional): Priority level of the workload. Defaults to None.
            workload_type (Optional[str], optional): Type of workload. Defaults to None.
        """
        self.cpu: float = cpu
        self.ram: int = ram
        self.disk: int = disk
        self.bw: int = bw
        self.delay: float = delay
        self.duration: float = duration
        self.cpu_saturation_percent: float = cpu_saturation_percent
        self.ram_saturation_percent: float = ram_saturation_percent
        self.disk_saturation_percent: float = disk_saturation_percent
        self.bw_saturation_percent: float = bw_saturation_percent
        self.priority: Optional[int] = priority
        self.workload_type: Optional[str] = workload_type

        # Set ID of Workload instance
        self.id = WorkloadRequest._id
        WorkloadRequest._id += 1

        # Mark if request is active
        self.active = False

    def __repr__(self) -> str:
        """Returns a string representation of the workload."""
        return (
            f"WorkloadRequest(id={self.id}, type={self.workload_type}, "
            f"CPU={self.cpu}, RAM={self.ram}, DISK={self.disk}, BW={self.bw} "
            f"CPU saturation={self.cpu_saturation_percent}, "
            f"RAM saturation: {self.ram_saturation_percent}, "
            f"DISK saturation: {self.disk_saturation_percent}, "
            f"BW saturation: {self.bw_saturation_percent}, "
            f"Priority={self.priority}, Delay={self.delay}, Duration={self.duration})"
        )

    @staticmethod
    def current_unit_workload(unit_value: int | float, saturation: float) -> int | float:
        """Calculates the dynamically saturated unit workload.

        This method determines the current unit workload by applying a saturation
        percentage, allowing the workload to fluctuate within a range.

        Returns:
            int: A randomly selected unit workload within the allowed range.
        """

        saturation_value: float = unit_value * (saturation / 100)

        # Define the fluctuation range
        if isinstance(unit_value, int):
            lower_bound: int = max(0, int(unit_value - saturation_value))
            upper_bound: int = int(unit_value + saturation_value)
            # Generate a random unit usage within this range
            saturated_unit: int = random.randint(lower_bound, upper_bound)
        else:
            # Define the fluctuation range
            lower_bound: float = max(0.0, unit_value - saturation_value)
            upper_bound: float = unit_value + saturation_value
            # Generate a random unit usage within this range
            saturated_unit: float = random.uniform(lower_bound, upper_bound)
            # Formatting the value
            saturated_unit: float = float(format(saturated_unit, ".2f"))

        return saturated_unit

    @staticmethod
    def current_unit_saturation(unit_value: int | float, saturation: float) -> int | float:
        saturation_value: float = unit_value * (saturation / 100)

        if isinstance(unit_value, int):
            # Generate a random Unit usage within this range
            saturation_of_unit: int = random.randint(
                int(0 - saturation_value), int(saturation_value)
            )
        else:
            # Generate a random Unit usage within this range
            saturation_of_unit: float = random.uniform(
                float(0.0 - saturation_value), float(saturation_value)
            )

        return saturation_of_unit

    @property
    def current_ram_workload(self) -> int:
        """Calculates the dynamically saturated RAM workload.

        This method determines the current RAM workload by applying a saturation
        percentage, allowing the workload to fluctuate within a range.

        Returns:
            int: A randomly selected RAM workload within the allowed range.
        """
        return self.current_unit_workload(self.ram, self.ram_saturation_percent)

    @property
    def current_ram_saturation(self) -> int:
        return self.current_unit_saturation(self.ram, self.ram_saturation_percent)

    @property
    def current_disk_workload(self) -> int:
        """Calculates the dynamically saturated Disk workload.

        This method determines the current Disk workload by applying a saturation
        percentage, allowing the workload to fluctuate within a range.

        Returns:
            int: A randomly selected Disk workload within the allowed range.
        """

        return self.current_unit_workload(self.disk, self.disk_saturation_percent)

    @property
    def current_disk_saturation(self) -> int:
        return self.current_unit_saturation(self.disk, self.disk_saturation_percent)

    @property
    def current_bw_workload(self) -> int:
        """Calculates the dynamically saturated Network Bandwidth (Data Transfer) workload.

        This method determines the current Network Bandwidth (Data Transfer) workload by applying a saturation
        percentage, allowing the workload to fluctuate within a range.

        Returns:
            int: A randomly selected Network Bandwidth (Data Transfer) workload within the allowed range.
        """

        return self.current_unit_workload(self.bw, self.bw_saturation_percent)

    @property
    def current_bw_saturation(self) -> int:
        return self.current_unit_saturation(self.bw, self.bw_saturation_percent)

    @property
    def current_cpu_workload(self) -> float:
        """Calculates the dynamically saturated CPU workload.

        This method determines the current CPU workload by applying a saturation
        percentage, allowing the workload to fluctuate within a range.

        Returns:
            float: A randomly selected CPU workload within the allowed range, rounded to 2 decimal places.
        """

        return self.current_unit_workload(self.cpu, self.cpu_saturation_percent)

    @property
    def current_cpu_saturation(self) -> float:
        return self.current_unit_saturation(self.cpu, self.cpu_saturation_percent)


if __name__ == "__main__":
    task1 = WorkloadRequest(
        cpu=2.5,
        ram=1024,
        disk=20480,
        bw=1,
        delay=1.0,
        duration=5.0,
        cpu_saturation_percent=10.0,
        ram_saturation_percent=5.0,
        disk_saturation_percent=1.5,
        bw_saturation_percent=0.5,
        priority=1,
        workload_type="User Request",
    )

    print(task1)
