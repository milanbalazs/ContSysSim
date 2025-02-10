"""Single-Node Simulation Example.

This script demonstrates a simple Docker Swarm-like simulation using SimPy.

It creates:
- A **DataCenter** with a single Virtual Machine (VM).
- Multiple **Containers** running inside the VM.
- Multiple **Workload Requests** simulating resource-consuming tasks.
- A **Load Balancer** that assigns workloads to containers using
  the **First-Fit with Reservations Load Balancing strategy**.

The script then runs the simulation and prints the status of resources.

It also allows visualization of resource usage over time.
"""

# Import necessary modules
from container_simulation.datacenter import DataCenter
from container_simulation.vm import Vm
from container_simulation.container import Container
from container_simulation.workload_request import WorkloadRequest
from container_simulation.utils import gb_to_mb
from container_simulation.simulation import Simulation
from container_simulation.loadbalancer import FirstFitReservationContainerLoadBalancer


class LbSimulation:
    """Simulates a single-node environment with VMs and containers.

    This class initializes:
    - A **single VM** that acts as the manager node.
    - Multiple **containers** assigned to this VM.
    - Multiple **workload requests** to simulate resource consumption.
    - A **data center** managing the VM.

    The simulation runs for a specified duration and logs resource usage.

    Attributes:
        simulation (Simulation): The simulation environment.
        datacenter (DataCenter): The data center managing VMs and containers.
        nodes (list[Vm]): List of Virtual Machines in the data center.
        containers (list[Container]): List of containers assigned to the VMs.
    """

    def __init__(self, use_reservations: bool = True) -> None:
        """Initializes the simulation environment with VMs and containers.

        Args:
            use_reservations (bool, optional): If `True`, enables **First-Fit with Reservations**,
                which considers workload start time and duration for placement.
                If `False`, uses **Classic First-Fit**, where workloads are placed immediately
                based on available resources. Defaults to `True`.
        """

        # Create the simulation instance (event-driven environment)
        self.simulation = Simulation()

        # Define containers that will run workloads inside the VM
        self.containers = [
            Container(
                self.simulation.env,
                name="MyContainer-1",
                cpu=2,  # CPU core allocation
                ram=gb_to_mb(1),  # RAM in MB
                disk=gb_to_mb(1),  # Disk in MB
                bw=1000,  # Network Bandwidth in Mbps
                cpu_saturation_percent=2.5,  # CPU fluctuation range
                ram_saturation_percent=3.2,  # RAM fluctuation range
                disk_saturation_percent=1.0,  # Disk fluctuation range
                bw_saturation_percent=2.5,  # Bandwidth fluctuation range
            ),
            Container(
                self.simulation.env,
                name="MyContainer-2",
                cpu=4,  # CPU core allocation
                ram=gb_to_mb(3),  # RAM in MB
                disk=gb_to_mb(5),  # Disk in MB
                bw=3000,  # Network Bandwidth in Mbps
                cpu_saturation_percent=2.5,  # CPU fluctuation range
                ram_saturation_percent=3.2,  # RAM fluctuation range
                disk_saturation_percent=1.0,  # Disk fluctuation range
                bw_saturation_percent=2.5,  # Bandwidth fluctuation range
            ),
        ]

        # Define a single Virtual Machine (VM) that will host the containers
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

        # Define multiple workload requests simulating tasks
        workload_requests = [
            WorkloadRequest(
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
                workload_type="1. User Request",  # Type of workload
            ),
            WorkloadRequest(
                cpu=2.0,  # CPU required for this workload
                ram=512,  # RAM required in MB
                disk=gb_to_mb(1),  # Disk required in MB
                bw=400,  # Network bandwidth in Mbps
                delay=1.0,  # Delay before the workload starts
                duration=8.0,  # Duration the workload remains active
                cpu_saturation_percent=1.0,  # CPU fluctuation range
                ram_saturation_percent=8.5,  # RAM fluctuation range
                disk_saturation_percent=3.5,  # Disk fluctuation range
                bw_saturation_percent=4.5,  # Bandwidth fluctuation range
                priority=1,  # Priority level of workload
                workload_type="2. User Request",  # Type of workload
            ),
        ]

        # Assign containers to the VM
        self.nodes[0].containers = self.containers

        # Create a DataCenter with the defined VM
        self.datacenter: DataCenter = DataCenter("MyDatacenter", vms=self.nodes)

        # Assign workloads to containers using the Load Balancer
        FirstFitReservationContainerLoadBalancer(
            workload_reqs=workload_requests,
            containers=self.containers,
            use_reservations=use_reservations,  # Toggle between "real" First-Fit & Reservations
            # TODO: Solve that logger passing. It should be handled automatically.
            logger=self.simulation.logger,
        )

        # Run the simulation in the DataCenter for 15 time units
        self.simulation.run(self.datacenter, simulation_time=15)


if __name__ == "__main__":
    # Run the simulation instance with reservations enabled
    simulation = LbSimulation(use_reservations=True)

    # Print a summary of resources used
    simulation.simulation.print_info()

    # Uncomment to visualize the simulation results:

    # Visualize the resource usage of the first container
    # simulation.datacenter.vms[0].containers[0].visualize_usage()

    # Visualize the resource usage of the VM
    # simulation.datacenter.vms[0].visualize_usage()

    # Visualize all containers running on the VM
    simulation.datacenter.vms[0].visualize_all_containers()

    # Visualize all VMs in the data center
    # simulation.datacenter.visualize_all_vms()

    """
    # Loop through each VM and visualize its usage along with its containers.
    for vm in simulation.datacenter.vms:
        vm.visualize_usage()
        for container in vm.containers:
            container.visualize_usage()
    """
