"""Single-Node Simulation Example.

This script demonstrates a simple Docker Swarm-like simulation using SimPy.

It creates:
- A **DataCenter** with a single Virtual Machine (Node).
- A **Container** running inside the Node.
- A **Workload Request** simulating a resource-consuming task.

The script then runs the simulation and prints the status of resources.
"""

# Import necessary modules
from cont_sys_sim.datacenter import DataCenter
from cont_sys_sim.node import Node
from cont_sys_sim.container import Container
from cont_sys_sim.workload_request import WorkloadRequest
from cont_sys_sim.utils import gb_to_mb
from cont_sys_sim.simulation import Simulation


class SingleNodeSimulation:
    """Simulates a single-node environment with Nodes and containers.

    This class initializes:
    - A **single manager node (Node)**.
    - A **container** assigned to this node.
    - A **workload request** to simulate resource consumption.
    - A **data center** managing the Node.

    The simulation runs for a specified duration and logs resource usage.

    Attributes:
        simulation (Simulation): The simulation environment.
        datacenter (DataCenter): The data center managing Nodes and containers.
        nodes (list[Node]): List of Virtual Machines in the data center.
        containers (list[Container]): List of containers assigned to the Nodes.
    """

    def __init__(self) -> None:
        """Initializes the simulation environment with Nodes and containers."""

        # Create the simulation instance (event-driven environment)
        self.simulation = Simulation()

        # Create a single Virtual Machine (Node)
        self.nodes = [
            Node(
                self.simulation.env,
                name="single-manager-node",
                cpu=8,  # Total CPU cores
                ram=gb_to_mb(16),  # Total RAM in MB
                disk=gb_to_mb(20),  # Total Disk in MB
                bw=10000,  # Network Bandwidth in Mbps
                cpu_fluctuation_percent=3.0,  # CPU fluctuation range
                ram_fluctuation_percent=8.5,  # RAM fluctuation range
                disk_fluctuation_percent=1.0,  # Disk fluctuation range
                bw_fluctuation_percent=15.2,  # Bandwidth fluctuation range
            )
        ]

        # Create a single container instance
        self.containers = [
            Container(
                self.simulation.env,
                name="MyContainer",
                cpu=2,  # CPU core allocation
                ram=gb_to_mb(1),  # RAM in MB
                disk=gb_to_mb(1),  # Disk in MB
                bw=1000,  # Network Bandwidth in Mbps
                cpu_fluctuation_percent=2.5,  # CPU fluctuation range
                ram_fluctuation_percent=3.2,  # RAM fluctuation range
                disk_fluctuation_percent=1.0,  # Disk fluctuation range
                bw_fluctuation_percent=2.5,  # Bandwidth fluctuation range
            )
        ]

        # Assign the container to the Node
        self.nodes[0].containers = self.containers

        # Create a DataCenter with the defined Node
        self.datacenter: DataCenter = DataCenter("MyDatacenter", nodes=self.nodes)

        # Define a workload request (simulating a task running inside the container)
        task1 = WorkloadRequest(
            cpu=1.0,  # CPU required for this workload
            ram=512,  # RAM required in MB
            disk=gb_to_mb(0.5),  # Disk required in MB
            bw=400,  # Network bandwidth in Mbps
            delay=3.0,  # Delay before the workload starts
            duration=8.0,  # Duration the workload remains active
            cpu_fluctuation_percent=10.0,  # CPU fluctuation range
            ram_fluctuation_percent=15.5,  # RAM fluctuation range
            disk_fluctuation_percent=1.5,  # Disk fluctuation range
            bw_fluctuation_percent=5.5,  # Bandwidth fluctuation range
            priority=1,  # Priority level of workload
            workload_type="User Request",  # Type of workload
        )

        # Assign the workload to the container
        self.containers[0].add_workload_request(task1)

        # Run the simulation in the DataCenter for 15 time units
        self.simulation.run(datacenter=self.datacenter, simulation_time=15)


if __name__ == "__main__":
    # Run the simulation instance
    single_node_simulation = SingleNodeSimulation()

    # Print a summary of resources
    single_node_simulation.simulation.print_info()

    # Uncomment the following lines to visualize the simulation results:

    # Visualize the resource usage of the first container
    single_node_simulation.datacenter.nodes[0].containers[0].visualize_usage()

    # Visualize the resource usage of the Node
    # single_node_simulation.datacenter.nodes[0].visualize_usage()

    # Visualize all containers running on the Node
    # single_node_simulation.datacenter.nodes[0].visualize_all_containers()

    # Visualize all Nodes in the data center
    # single_node_simulation.datacenter.visualize_all_nodes()

    """
    # Loop through each Node and visualize its usage along with its containers.
    for node in single_node_simulation.datacenter.nodes:
        node.visualize_usage()
        for container in node.containers:
            container.visualize_usage()
    """
