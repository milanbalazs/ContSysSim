"""DataCenter Module.

This module defines the DataCenter class, which represents a data center that
manages multiple Virtual Machines (VMs) in a simulated Docker Swarm environment.
"""

from container_simulation.vm import Vm
from typing import Optional, List
from container_simulation.visualizations import Visualisations


class DataCenter:
    """Represents a Data Center that manages Virtual Machines (VMs).

    The DataCenter class stores and manages a collection of VMs, allowing
    users to add new VMs dynamically and retrieve existing ones.

    Attributes:
        _id (int): Class-level counter to generate unique IDs for each DataCenter instance.
        _name (str): The name of the data center.
        _vms (Optional[List[Vm]]): A list of Virtual Machines (VMs) in the data center.
        id (int): The unique identifier for the data center instance.
    """

    _id: int = 0  # Class-level counter for unique DataCenter IDs

    def __init__(self, name: str = "", vms: Optional[List[Vm]] = None) -> None:
        """Initializes a DataCenter instance.

        Args:
            name (str, optional): The name of the data center. Defaults to an empty string.
            vms (Optional[List[Vm]], optional): A list of VMs to initialize the data center.
                                                Defaults to None.
        """
        self._name: str = name
        self._vms: Optional[List[Vm]] = vms if vms else []
        self.id: int = DataCenter._id
        DataCenter._id += 1

        # Visualisations
        self.visualisations: Visualisations = Visualisations()

    @property
    def name(self) -> str:
        """Gets the name of the data center.

        Returns:
            str: The name of the data center.
        """
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """Sets a new name for the data center.

        Args:
            new_name (str): The new name to be assigned.
        """
        self._name = new_name

    @property
    def vms(self) -> Optional[List[Vm]]:
        """Gets the list of VMs in the data center.

        Returns:
            Optional[List[Vm]]: A list of Virtual Machines (VMs) in the data center.
        """
        return self._vms

    @vms.setter
    def vms(self, new_vms: List[Vm]) -> None:
        """Sets a new list of VMs in the data center.

        Args:
            new_vms (List[Vm]): The new list of VMs to be assigned.
        """
        self._vms = new_vms

    def add_vms(self, new_vms: List[Vm]) -> None:
        """Adds new VMs to the data center.

        If the data center already has VMs, the new VMs will be added to the existing list.
        If there are no VMs yet, the provided list will be set as the new VMs.

        Args:
            new_vms (List[Vm]): The list of new VMs to add to the data center.
        """
        if self._vms is not None:
            self._vms.extend(new_vms)
        else:
            self._vms = new_vms

    def visualize_all_vms(self) -> None:
        """Visualizes the CPU and RAM usage of all VMs in a pop-up figure with scrolling support.

        This method generates a multi-subplot figure where:
            - Each row represents a VM.
            - The left column shows CPU usage over time.
            - The right column shows RAM usage over time.

        The visualization dynamically adjusts the window size based on the number of VMs
        while ensuring that the figure remains readable.
        Interactive mode (`plt.ion()`) is enabled to keep the figure
        responsive, and `plt.show(block=True)` ensures that it pops up as expected.

        Raises:
            ValueError: If no VMs are available to visualize.

        """
        self.visualisations.visualize_all_vms_in_datacenter(self)
