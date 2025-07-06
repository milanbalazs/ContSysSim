"""Multi-Node Simulation Example.

This script simulates a Docker Swarm-like environment using SimPy. It manages a
DataCenter with multiple Virtual Machines (Nodes) and Containers, simulating
their startup and workload behavior over time.

The simulation consists of:
- **Manager Nodes**: Handle authentication, service management, and monitoring.
- **Database Nodes**: Store application data and caching services.

Each node has predefined resources and can host multiple containers.
"""

from cont_sys_sim.datacenter import DataCenter
from cont_sys_sim.node import Node
from cont_sys_sim.container import Container
from cont_sys_sim.workload_request import WorkloadRequest
from cont_sys_sim.utils import gb_to_mb
from cont_sys_sim.simulation import Simulation


class MultiNodeSimulation:
    """Represents a Docker Swarm-like simulation with multiple nodes.

    The simulation initializes a data center with manager and database Nodes,
    assigns common containers to them, and runs a time-based simulation.

    Attributes:
        simulation (Simulation): The main simulation manager.
        common_manager_containers (list[Container]): List of common manager containers.
        common_db_containers (list[Container]): List of common database containers.
        manager_nodes (list[Node]): List of manager Nodes.
        db_nodes (list[Node]): List of database Nodes.
        datacenter (DataCenter): The data center managing all Nodes.
    """

    def __init__(self) -> None:
        """Initializes the Multi-Node Simulation instance.

        The simulation consists of:
        - Manager Nodes: Running authentication, service management, and monitoring containers.
        - Database Nodes: Running database and caching containers.
        """

        # Create the simulation environment
        self.simulation = Simulation()

        # Create predefined containers and Nodes
        self.common_manager_containers: list[Container] = self.get_common_manager_containers()
        self.common_db_containers: list[Container] = self.get_common_db_containers()
        self.manager_nodes: list[Node] = self.get_manager_nodes()
        self.db_nodes: list[Node] = self.get_db_nodes()

        # Assign common containers to their respective Nodes
        for node in self.manager_nodes:
            node.containers = self.common_manager_containers
        for node in self.db_nodes:
            node.containers = self.common_db_containers

        # Combine all Nodes into a single DataCenter instance
        all_nodes: list[Node] = self.manager_nodes + self.db_nodes
        self.datacenter: DataCenter = DataCenter("MyDatacenter", nodes=all_nodes)

        # Assign a sample workload request to a container
        task1 = WorkloadRequest(
            cpu=1.0,
            ram=512,
            disk=gb_to_mb(0.5),
            bw=400,
            delay=3.0,
            duration=8.0,
            cpu_fluctuation_percent=10.0,
            ram_fluctuation_percent=15.5,
            disk_fluctuation_percent=1.5,
            bw_fluctuation_percent=5.5,
            priority=1,
            workload_type="User Request",
        )

        self.common_manager_containers[0].add_workload_request(task1)

        # Run the simulation
        self.simulation.run(datacenter=self.datacenter)

    def get_common_manager_containers(self) -> list[Container]:
        """Creates a predefined list of manager containers.

        The manager containers handle authentication, service management,
        and system monitoring.

        Returns:
            list[Container]: A list of predefined manager containers.
        """
        return [
            Container(
                self.simulation.env,
                "KeyCloak",  # Authentication and Identity Management
                2,
                gb_to_mb(1),
                gb_to_mb(1),
                1000,
                cpu_fluctuation_percent=2.5,
                ram_fluctuation_percent=3.2,
                disk_fluctuation_percent=1.0,
                bw_fluctuation_percent=2.5,
            ),
            Container(
                self.simulation.env, "ServiceManager", 2, gb_to_mb(2), gb_to_mb(2), 1000
            ),  # Microservice Coordination
            Container(
                self.simulation.env, "Grafana", 1, gb_to_mb(1), gb_to_mb(2), 1000
            ),  # Monitoring & Dashboards
        ]

    def get_common_db_containers(self) -> list[Container]:
        """Creates a predefined list of database containers.

        These containers store application data and handle caching.

        Returns:
            list[Container]: A list of predefined database containers.
        """
        return [
            Container(
                self.simulation.env, "MySQL", 2, gb_to_mb(4), gb_to_mb(3), 1000
            ),  # SQL Database
            Container(
                self.simulation.env, "Redis", 2, gb_to_mb(2), gb_to_mb(1), 1000
            ),  # In-Memory Cache
            Container(
                self.simulation.env, "MongoDB", 1, gb_to_mb(1), gb_to_mb(2), 1000
            ),  # NoSQL Database
        ]

    def get_manager_nodes(self) -> list[Node]:
        """Creates a predefined list of manager Nodes.

        The manager nodes are responsible for coordinating containers
        and handling various administrative tasks.

        Returns:
            list[Node]: A list of predefined manager Virtual Machines.
        """
        return [
            Node(
                self.simulation.env,
                "manager-1",
                8,
                gb_to_mb(16),
                gb_to_mb(20),
                10000,
                cpu_fluctuation_percent=3.0,
                ram_fluctuation_percent=8.5,
                disk_fluctuation_percent=1.0,
                bw_fluctuation_percent=15.2,
            ),
            Node(self.simulation.env, "manager-2", 8, gb_to_mb(16), gb_to_mb(20), 10000),
            Node(self.simulation.env, "manager-3", 8, gb_to_mb(16), gb_to_mb(20), 10000),
        ]

    def get_db_nodes(self) -> list[Node]:
        """Creates a predefined list of database Nodes.

        The database nodes are responsible for storing and retrieving data
        for the application.

        Returns:
            list[Node]: A list of predefined database Virtual Machines.
        """
        return [
            Node(self.simulation.env, "db-1", 16, gb_to_mb(16), gb_to_mb(200), 10000),
            Node(self.simulation.env, "db-2", 16, gb_to_mb(16), gb_to_mb(200), 10000),
            Node(self.simulation.env, "db-3", 16, gb_to_mb(16), gb_to_mb(200), 10000),
        ]


if __name__ == "__main__":
    # Initialize and run the multi-node simulation
    simulation = MultiNodeSimulation()

    # Print simulation summary
    simulation.simulation.print_info()

    # Visualize resource usage for the first Node and its first container
    # simulation.datacenter.nodes[0].containers[0].visualize_usage()

    # Uncomment these lines for additional visualization options:
    # simulation.datacenter.nodes[0].visualize_usage()
    # simulation.datacenter.nodes[0].visualize_all_containers()
    simulation.datacenter.visualize_all_nodes()

    """
    Alternative way to visualize all Nodes and containers:
    
    for node in simulation.datacenter.nodes:
        node.visualize_usage()
        for container in node.containers:
            container.visualize_usage()
    """
