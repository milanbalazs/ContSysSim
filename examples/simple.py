"""Single-Node Simulation Example.

This script demonstrates a simple Docker Swarm-like simulation using SimPy.

It creates:
- A **DataCenter** with a single Virtual Machine (VM).
- A **Container** running inside the VM.
- A **Workload Request** simulating a resource-consuming task.

The script then runs the simulation and prints the status of resources.
"""

# Import necessary modules
from container_simulation.datacenter import DataCenter
from container_simulation.vm import Vm
from container_simulation.container import Container
from container_simulation.workload_request import WorkloadRequest
from container_simulation.utils import gb_to_mb
from container_simulation.simulation import Simulation


class MultiNodeSimulation:
    """Simulates a multi-node environment with VMs and containers.

    This class initializes:
    - A **single manager node (VM)**.
    - A **container** assigned to this node.
    - A **workload request** to simulate resource consumption.
    - A **data center** managing the VM.

    The simulation runs for a specified duration and logs resource usage.

    Attributes:
        simulation (Simulation): The simulation environment.
        datacenter (DataCenter): The data center managing VMs and containers.
        nodes (list[Vm]): List of Virtual Machines in the data center.
        containers (list[Container]): List of containers assigned to the VMs.
    """

    def __init__(self) -> None:
        """Initializes the simulation environment with VMs and containers."""

        # Create the simulation instance (event-driven environment)
        self.simulation = Simulation()

        # Create a single container instance
        self.containers = [
            Container(
                self.simulation.env,
                name="MyContainer",
                cpu=2,  # CPU core allocation
                ram=gb_to_mb(1),  # RAM in MB
                disk=gb_to_mb(1),  # Disk in MB
                bw=1000,  # Network Bandwidth in Mbps
                cpu_saturation_percent=2.5,  # CPU fluctuation range
                ram_saturation_percent=3.2,  # RAM fluctuation range
                disk_saturation_percent=1.0,  # Disk fluctuation range
                bw_saturation_percent=2.5,  # Bandwidth fluctuation range
            )
        ]

        # Create a single Virtual Machine (VM)
        self.nodes = [
            Vm(
                self.simulation.env,
                name="single-manager-node",
                cpu=8,  # Total CPU cores
                ram=gb_to_mb(16),  # Total RAM in MB
                disk=gb_to_mb(20),  # Total Disk in MB
                bw=10000,  # Network Bandwidth in Mbps
                cpu_saturation_percent=3.0,  # CPU fluctuation range
                ram_saturation_percent=8.5,  # RAM fluctuation range
                disk_saturation_percent=1.0,  # Disk fluctuation range
                bw_saturation_percent=15.2,  # Bandwidth fluctuation range
            )
        ]

        # Define a workload request (simulating a task running inside the container)
        task1 = WorkloadRequest(
            cpu=1.0,  # CPU required for this workload
            ram=512,  # RAM required in MB
            disk=gb_to_mb(0.5),  # Disk required in MB
            bw=400,  # Network bandwidth in Mbps
            delay=3.0,  # Delay before the workload starts
            duration=8.0,  # Duration the workload remains active
            cpu_saturation_percent=10.0,  # CPU fluctuation range
            ram_saturation_percent=15.5,  # RAM fluctuation range
            disk_saturation_percent=1.5,  # Disk fluctuation range
            bw_saturation_percent=5.5,  # Bandwidth fluctuation range
            priority=1,  # Priority level of workload
            workload_type="User Request",  # Type of workload
        )

        # Assign the workload to the container
        self.containers[0].add_workload_request(task1)

        # Assign the container to the VM
        self.nodes[0].containers = self.containers

        # Create a DataCenter with the defined VM
        self.datacenter: DataCenter = DataCenter("MyDatacenter", vms=self.nodes)

        # Run the simulation in the DataCenter for 15 time units
        self.simulation.run(self.datacenter, simulation_time=15)


if __name__ == "__main__":
    # Run the simulation instance
    simulation = MultiNodeSimulation()

    # Print a summary of resources
    simulation.simulation.print_info()

    # Uncomment the following lines to visualize the simulation results:

    # Visualize the resource usage of the first container
    simulation.datacenter.vms[0].containers[0].visualize_usage()

    # Visualize the resource usage of the VM
    # simulation.datacenter.vms[0].visualize_usage()

    # Visualize all containers running on the VM
    # simulation.datacenter.vms[0].visualize_all_containers()

    # Visualize all VMs in the data center
    # simulation.datacenter.visualize_all_vms()

    """
    # Loop through each VM and visualize its usage along with its containers.
    for vm in simulation.datacenter.vms:
        vm.visualize_usage()
        for container in vm.containers:
            container.visualize_usage()
    """
