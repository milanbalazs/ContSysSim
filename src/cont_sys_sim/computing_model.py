"""Abstract Base Model Module.

This module defines the AbstractBaseModel class, which serves as a base
for both Nodes and Containers. It provides attributes
for name, CPU, RAM, and startup delay, along with property methods for
accessing and modifying these attributes.
"""

from abc import ABC


class AbstractBaseModel(ABC):
    """An abstract base model for Nodes and Containers.

    This class provides a foundational structure for managing computing
    resources such as CPU, RAM, and startup delay.

    Attributes:
        _name (str): The name of the instance (Node or Container).
        _cpu (float): The CPU capacity allocated to the instance.
        _ram (int): The RAM capacity allocated to the instance in MB.
        _disk (int): The RAM capacity allocated to the instance in MB.
        _bw(int): The Network Bandwidth capacity allocated to the instance in Mbps.
        _cpu_fluctuation_percent (float): Variability in CPU usage (+/- percentage).
        _ram_fluctuation_percent (float): Variability in RAM usage (+/- percentage).
        _disk_fluctuation_percent (float): Variability in Disk usage (+/- percentage).
        _bw_fluctuation_percent (float): Variability in Network Bandwidth (Data Transfer)
                                        usage (+/- percentage).
        _start_up_delay (float): The startup delay in seconds.
    """

    def __init__(
        self,
        name: str,
        cpu: float,
        ram: int,
        disk: int,
        bw: int,
        start_up_delay: float = 0.5,
        cpu_fluctuation_percent: float = 0.0,
        ram_fluctuation_percent: float = 0.0,
        disk_fluctuation_percent: float = 0.0,
        bw_fluctuation_percent: float = 0.0,
    ) -> None:
        """Initializes an AbstractBaseModel instance.

        Args:
            name (str): The name of the instance.
            cpu (float): The CPU capacity allocated to the instance.
            ram (int): The RAM capacity allocated to the instance in MB.
            disk (int): The Disk capacity allocated to the instance in MB.
            bw (int): The Network Bandwidth (Data Transfer) capacity allocated to the instance in
                        Megabits per second (Mbps)
            cpu_fluctuation_percent (float): Variability in CPU usage (+/- percentage).
            ram_fluctuation_percent (float): Variability in RAM usage (+/- percentage).
            disk_fluctuation_percent (float): Variability in Disk usage (+/- percentage).
            bw_fluctuation_percent (float): Variability in Network Bandwidth (Data Transfer)
                                           usage (+/- percentage).
            start_up_delay (float, optional): The startup delay in seconds. Defaults to 0.5.
        """
        self._name: str = name
        self._cpu: float = cpu
        self._ram: int = ram
        self._disk: int = disk
        self._bw: int = bw
        self._start_up_delay: float = start_up_delay
        self._cpu_fluctuation_percent: float = cpu_fluctuation_percent
        self._ram_fluctuation_percent: float = ram_fluctuation_percent
        self._disk_fluctuation_percent: float = disk_fluctuation_percent
        self._bw_fluctuation_percent: float = bw_fluctuation_percent

    @property
    def name(self) -> str:
        """Gets the name of the instance.

        Returns:
            str: The name of the instance.
        """
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """Sets a new name for the instance.

        Args:
            new_name (str): The new name to be assigned.
        """
        self._name = new_name

    @property
    def cpu(self) -> float:
        """Gets the CPU capacity of the instance.

        Returns:
            int: The CPU capacity.
        """
        return self._cpu

    @cpu.setter
    def cpu(self, new_cpu: int) -> None:
        """Sets a new CPU capacity for the instance.

        Args:
            new_cpu (int): The new CPU capacity to be assigned.
        """
        self._cpu = new_cpu

    @property
    def ram(self) -> int:
        """Gets the RAM capacity of the instance.

        Returns:
            int: The RAM capacity in MB.
        """
        return self._ram

    @ram.setter
    def ram(self, new_ram: int) -> None:
        """Sets a new RAM capacity for the instance.

        Args:
            new_ram (int): The new RAM capacity to be assigned.
        """
        self._ram = new_ram

    @property
    def start_up_delay(self) -> float:
        """Gets the startup delay of the instance.

        Returns:
            float: The startup delay in seconds.
        """
        return self._start_up_delay

    @start_up_delay.setter
    def start_up_delay(self, new_start_up_delay: float) -> None:
        """Sets a new startup delay for the instance.

        Args:
            new_start_up_delay (float): The new startup delay to be assigned.
        """
        self._start_up_delay = new_start_up_delay

    @property
    def disk(self) -> int:
        """Gets the Disk capacity of the instance.

        Returns:
            int: The Disk capacity in MB.
        """
        return self._disk

    @disk.setter
    def disk(self, new_disk: int) -> None:
        """Sets a new Disk capacity for the instance.

        Args:
            new_disk (int): The new Disk capacity to be assigned.
        """
        self._disk = new_disk

    @property
    def bw(self) -> int:
        """Gets the Network Bandwidth (Data Transfer) capacity of the instance.

        Returns:
            int: The Network Bandwidth (Data Transfer) capacity in MB.
        """
        return self._bw

    @bw.setter
    def bw(self, new_bw: int) -> None:
        """Sets a new Network Bandwidth (Data Transfer) for the instance.

        Args:
            new_bw (int): The new Network Bandwidth (Data Transfer) capacity to be assigned.
        """
        self._bw = new_bw

    @property
    def cpu_fluctuation_percent(self) -> float:
        """Gets the CPU fluctuation of the instance in percent.

        Returns:
            float: The CPU fluctuation in percent.
        """
        return self._cpu_fluctuation_percent

    @cpu_fluctuation_percent.setter
    def cpu_fluctuation_percent(self, new_fluctuation_percent: float) -> None:
        """Sets new CPU fluctuation for the instance.

        Args:
            new_fluctuation_percent (float): The new CPU fluctuation to be assigned.
        """
        self._cpu_fluctuation_percent = new_fluctuation_percent

    @property
    def ram_fluctuation_percent(self) -> float:
        """Gets the RAM fluctuation of the instance in percent.

        Returns:
            float: The RAM fluctuation in percent.
        """
        return self._ram_fluctuation_percent

    @ram_fluctuation_percent.setter
    def ram_fluctuation_percent(self, new_fluctuation_percent: float) -> None:
        """Sets new RAM fluctuation for the instance.

        Args:
            new_fluctuation_percent (float): The new RAM fluctuation to be assigned.
        """
        self._ram_fluctuation_percent = new_fluctuation_percent

    @property
    def disk_fluctuation_percent(self) -> float:
        """Gets the Disk fluctuation of the instance in percent.

        Returns:
            float: The Disk fluctuation in percent.
        """
        return self._disk_fluctuation_percent

    @disk_fluctuation_percent.setter
    def disk_fluctuation_percent(self, new_fluctuation_percent: float) -> None:
        """Sets new Disk fluctuation for the instance.

        Args:
            new_fluctuation_percent (float): The new Disk fluctuation to be assigned.
        """
        self._disk_fluctuation_percent = new_fluctuation_percent

    @property
    def bw_fluctuation_percent(self) -> float:
        """Gets the BW fluctuation of the instance in percent.

        Returns:
            float: The BW fluctuation in percent.
        """
        return self._bw_fluctuation_percent

    @bw_fluctuation_percent.setter
    def bw_fluctuation_percent(self, new_fluctuation_percent: float) -> None:
        """Sets new BW fluctuation for the instance.

        Args:
            new_fluctuation_percent (float): The new BW fluctuation to be assigned.
        """
        self._bw_fluctuation_percent = new_fluctuation_percent
