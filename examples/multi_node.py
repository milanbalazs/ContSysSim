"""Multi-Node Simulation Example.

This script simulates a Docker Swarm-like environment using SimPy. It manages a
DataCenter with multiple Virtual Machines (VMs) and Containers, simulating
their startup and workload behavior over time.

The simulation consists of:
- **Manager Nodes**: Handle authentication, service management, and monitoring.
- **Database Nodes**: Store application data and caching services.

Each node has predefined resources and can host multiple containers.
"""

from container_simulation.datacenter import DataCenter
from container_simulation.vm import Vm
from container_simulation.container import Container
from container_simulation.workload_request import WorkloadRequest
from container_simulation.utils import gb_to_mb
from container_simulation.simulation import Simulation


class MultiNodeSimulation:
    """Represents a Docker Swarm-like simulation with multiple nodes.

    The simulation initializes a data center with manager and database VMs,
    assigns common containers to them, and runs a time-based simulation.

    Attributes:
        simulation (Simulation): The main simulation manager.
        common_manager_containers (list[Container]): List of common manager containers.
        common_db_containers (list[Container]): List of common database containers.
        manager_vms (list[Vm]): List of manager VMs.
        db_vms (list[Vm]): List of database VMs.
        datacenter (DataCenter): The data center managing all VMs.
    """

    def __init__(self) -> None:
        """Initializes the Multi-Node Simulation instance.

        The simulation consists of:
        - Manager Nodes: Running authentication, service management, and monitoring containers.
        - Database Nodes: Running database and caching containers.
        """

        # Create the simulation environment
        self.simulation = Simulation()

        # Create predefined containers and VMs
        self.common_manager_containers: list[Container] = self.get_common_manager_containers()
        self.common_db_containers: list[Container] = self.get_common_db_containers()
        self.manager_vms: list[Vm] = self.get_manager_nodes()
        self.db_vms: list[Vm] = self.get_db_nodes()

        # Assign a sample workload request to a container
        task1 = WorkloadRequest(
            cpu=1.0,
            ram=512,
            disk=gb_to_mb(0.5),
            bw=400,
            delay=3.0,
            duration=8.0,
            cpu_saturation_percent=10.0,
            ram_saturation_percent=15.5,
            disk_saturation_percent=1.5,
            bw_saturation_percent=5.5,
            priority=1,
            workload_type="User Request",
        )

        self.common_manager_containers[0].add_workload_request(task1)

        # Assign common containers to their respective VMs
        for vm in self.manager_vms:
            vm.containers = self.common_manager_containers
        for vm in self.db_vms:
            vm.containers = self.common_db_containers

        # Combine all VMs into a single DataCenter instance
        all_vms: list[Vm] = self.manager_vms + self.db_vms
        self.datacenter: DataCenter = DataCenter("MyDatacenter", vms=all_vms)

        # Run the simulation
        self.simulation.run(self.datacenter)

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
                cpu_saturation_percent=2.5,
                ram_saturation_percent=3.2,
                disk_saturation_percent=1.0,
                bw_saturation_percent=2.5,
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

    def get_manager_nodes(self) -> list[Vm]:
        """Creates a predefined list of manager VMs.

        The manager nodes are responsible for coordinating containers
        and handling various administrative tasks.

        Returns:
            list[Vm]: A list of predefined manager Virtual Machines.
        """
        return [
            Vm(
                self.simulation.env,
                "manager-1",
                8,
                gb_to_mb(16),
                gb_to_mb(20),
                10000,
                cpu_saturation_percent=3.0,
                ram_saturation_percent=8.5,
                disk_saturation_percent=1.0,
                bw_saturation_percent=15.2,
            ),
            Vm(self.simulation.env, "manager-2", 8, gb_to_mb(16), gb_to_mb(20), 10000),
            Vm(self.simulation.env, "manager-3", 8, gb_to_mb(16), gb_to_mb(20), 10000),
        ]

    def get_db_nodes(self) -> list[Vm]:
        """Creates a predefined list of database VMs.

        The database nodes are responsible for storing and retrieving data
        for the application.

        Returns:
            list[Vm]: A list of predefined database Virtual Machines.
        """
        return [
            Vm(self.simulation.env, "db-1", 16, gb_to_mb(16), gb_to_mb(200), 10000),
            Vm(self.simulation.env, "db-2", 16, gb_to_mb(16), gb_to_mb(200), 10000),
            Vm(self.simulation.env, "db-3", 16, gb_to_mb(16), gb_to_mb(200), 10000),
        ]


if __name__ == "__main__":
    # Initialize and run the multi-node simulation
    simulation = MultiNodeSimulation()

    # Print simulation summary
    simulation.simulation.print_info()

    # Visualize resource usage for the first VM and its first container
    simulation.datacenter.vms[0].containers[0].visualize_usage()

    # Uncomment these lines for additional visualization options:
    # simulation.datacenter.vms[0].visualize_usage()
    # simulation.datacenter.vms[0].visualize_all_containers()
    # simulation.datacenter.visualize_all_vms()

    """
    Alternative way to visualize all VMs and containers:
    
    for vm in simulation.datacenter.vms:
        vm.visualize_usage()
        for container in vm.containers:
            container.visualize_usage()
    """
