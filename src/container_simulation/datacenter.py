"""DataCenter Module.

This module defines the DataCenter class, which represents a data center that
manages multiple Virtual Machines (Nodes) in a simulated Docker Swarm environment.
"""

from logging import Logger
from typing import Optional, List

from container_simulation.node import Node
from container_simulation.visualizations import Visualisations
from container_simulation.utils import get_logger  # Import singleton logger


class DataCenter:
    """Represents a Data Center that manages Virtual Machines (Nodes).

    The DataCenter class stores and manages a collection of Nodes, allowing
    users to add new Nodes dynamically and retrieve existing ones.

    Attributes:
        _id (int): Class-level counter to generate unique IDs for each DataCenter instance.
        _name (str): The name of the data center.
        _nodes (Optional[List[Node]]): A list of Virtual Machines (Nodes) in the data center.
        id (int): The unique identifier for the data center instance.
        _logger (Optional[Logger]): Logger object.
    """

    _id: int = 0  # Class-level counter for unique DataCenter IDs

    def __init__(
        self, name: str = "", nodes: Optional[List[Node]] = None, logger: Optional[Logger] = None
    ) -> None:
        """Initializes a DataCenter instance.

        Args:
            name (str, optional): The name of the data center. Defaults to an empty string.
            nodes (Optional[List[Node]], optional): A list of Nodes to initialize the data center.
                                                Defaults to None.
            logger (Optional[Logger]): Logger object.
        """
        self._name: str = name
        self._nodes: Optional[List[Node]] = nodes if nodes else []
        self.id: int = DataCenter._id
        DataCenter._id += 1

        # Visualisations
        self.visualisations: Visualisations = Visualisations()

        self._logger = logger if logger else get_logger()

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
    def logger(self) -> Logger:
        """Gets the logger of the data center.

        Returns:
            str: The logger of the data center.
        """
        return self._logger

    @logger.setter
    def logger(self, new_logger: Logger) -> None:
        """Sets a logger name for the data center.

        Args:
            new_logger (str): The new logger to be assigned.
        """
        self._logger = new_logger

    @property
    def nodes(self) -> Optional[List[Node]]:
        """Gets the list of Nodes in the data center.

        Returns:
            Optional[List[Node]]: A list of Virtual Machines (Nodes) in the data center.
        """
        return self._nodes

    @nodes.setter
    def nodes(self, new_nodes: List[Node]) -> None:
        """Sets a new list of Nodes in the data center.

        Args:
            new_nodes (List[Node]): The new list of Nodes to be assigned.
        """
        self._nodes = new_nodes

    def add_nodes(self, new_nodes: List[Node]) -> None:
        """Adds new Nodes to the data center.

        If the data center already has Nodes, the new Nodes will be added to the existing list.
        If there are no Nodes yet, the provided list will be set as the new Nodes.

        Args:
            new_nodes (List[Node]): The list of new Nodes to add to the data center.
        """
        if self._nodes is not None:
            self._nodes.extend(new_nodes)
        else:
            self._nodes = new_nodes

    def visualize_all_nodes(self) -> None:
        """Visualizes the CPU and RAM usage of all Nodes in a pop-up figure with scrolling support.

        This method generates a multi-subplot figure where:
            - Each row represents a Node.
            - The left column shows CPU usage over time.
            - The right column shows RAM usage over time.

        The visualization dynamically adjusts the window size based on the number of Nodes
        while ensuring that the figure remains readable.
        Interactive mode (`plt.ion()`) is enabled to keep the figure
        responsive, and `plt.show(block=True)` ensures that it pops up as expected.

        Raises:
            ValueError: If no Nodes are available to visualize.

        """
        self.visualisations.visualize_all_nodes_in_datacenter(self)
