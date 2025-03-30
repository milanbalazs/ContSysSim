"""
This module initializes and starts a simulation based on a YAML configuration file.
It supports creating a dynamic simulation environment with Nodes, containers, workloads,
and an optional load balancer. The simulation runs based on the provided configuration
and outputs resource summaries and optional visualizations.

Classes:
    SimulationRunner: Main class responsible for setting up and running the simulation.

Usage:
    Run the script with the desired configuration file:
        python3 src/container_simulation/config_parser.py --config configs/example.yml

TODO: The First-Fit LoadBalancer with Reservation doesn't work as expected. It should be checked!
"""

import argparse
from typing import Optional, List
from logging import Logger

from container_simulation.datacenter import DataCenter
from container_simulation.node import Node
from container_simulation.container import Container
from container_simulation.workload_request import WorkloadRequest
from container_simulation.simulation import Simulation
from container_simulation.loadbalancer import FirstFitReservationContainerLoadBalancer
from container_simulation.utils import get_logger
from config_parser import SimulationConfig, parse_simulation_config

LOGGER: Logger = get_logger()


class SimulationRunner:
    """
    Handles setting up and running a container simulation based on a parsed configuration.

    Attributes:
        simulation (Simulation): The simulation environment.
        datacenter (Optional[DataCenter]): The data center managing all Nodes and containers.
        load_balancer (Optional[FirstFitReservationContainerLoadBalancer]):
            The load balancer, if enabled.
    """

    def __init__(self, config: SimulationConfig) -> None:
        """
        Initializes the simulation environment based on the parsed configuration.

        Args:
            config (SimulationConfig): Parsed simulation configuration.
        """
        self.config: SimulationConfig = config
        self.simulation: Simulation = Simulation()
        self.datacenter: Optional[DataCenter] = None
        self.load_balancer: Optional[FirstFitReservationContainerLoadBalancer] = None

    @staticmethod
    def _create_workload(workload_config) -> WorkloadRequest:
        """
        Creates a WorkloadRequest object from a workload configuration.

        Args:
            workload_config: Configuration object containing workload parameters.

        Returns:
            WorkloadRequest: An instance of WorkloadRequest initialized with the given parameters.
        """
        return WorkloadRequest(
            cpu=workload_config.cpu,
            ram=workload_config.ram,
            disk=workload_config.disk,
            bw=workload_config.bandwidth,
            delay=workload_config.delay,
            duration=workload_config.duration,
            cpu_saturation_percent=workload_config.cpu_saturation_percent,
            ram_saturation_percent=workload_config.ram_saturation_percent,
            disk_saturation_percent=workload_config.disk_saturation_percent,
            bw_saturation_percent=workload_config.bandwidth_saturation_percent,
            priority=workload_config.priority,
            workload_type=workload_config.type,
        )

    def _create_container(self, container_config) -> Container:
        """
        Creates a Container object from a container configuration.

        Args:
            container_config: Configuration object containing container parameters.

        Returns:
            Container: An instance of Container initialized with the given parameters.
        """
        workloads: List[WorkloadRequest] = [
            self._create_workload(w) for w in container_config.workloads
        ]
        container = Container(
            self.simulation.env,
            name=container_config.name,
            cpu=container_config.cpu,
            ram=container_config.ram,
            disk=container_config.disk,
            bw=container_config.bandwidth,
            start_up_delay=container_config.start_up_delay,
            cpu_saturation_percent=container_config.cpu_saturation_percent,
            ram_saturation_percent=container_config.ram_saturation_percent,
            disk_saturation_percent=container_config.disk_saturation_percent,
            bw_saturation_percent=container_config.bandwidth_saturation_percent,
        )
        for workload in workloads:
            LOGGER.debug(f"[{self.simulation.env.now}] Parsed Workload: {workload}")
            container.add_workload_request(workload)
        return container

    def _create_node(self, node_config) -> Node:
        """
        Creates a Node object from a Node configuration.

        Args:
            node_config: Configuration object containing Node parameters.

        Returns:
            Node: An instance of Node initialized with the given parameters.
        """
        containers: List[Container] = [self._create_container(c) for c in node_config.containers]
        node = Node(
            self.simulation.env,
            name=node_config.name,
            cpu=node_config.cpu,
            ram=node_config.ram,
            disk=node_config.disk,
            bw=node_config.bandwidth,
            start_up_delay=node_config.start_up_delay,
            cpu_saturation_percent=node_config.cpu_saturation_percent,
            ram_saturation_percent=node_config.ram_saturation_percent,
            disk_saturation_percent=node_config.disk_saturation_percent,
            bw_saturation_percent=node_config.bandwidth_saturation_percent,
            stop_lack_of_resource=node_config.stop_lack_of_resource,
        )
        node.containers = containers
        return node

    def setup_simulation(self) -> None:
        """
        Sets up the simulation environment based on the parsed configuration.

        This method initializes all Nodes, containers, and the optional load balancer.
        """
        LOGGER.info("Setting up the simulation environment...")
        LOGGER.debug(f"Nodes from config: {self.config.datacenter.nodes}")

        nodes: List[Node] = [
            self._create_node(node_config) for node_config in self.config.datacenter.nodes
        ]
        self.datacenter = DataCenter(self.config.datacenter.name, nodes=nodes)

        if self.config.load_balancer and self.config.load_balancer.enabled:
            LOGGER.debug(f"Initializing Load Balancer with: {self.config.load_balancer.workloads}")
            workloads: List[WorkloadRequest] = [
                self._create_workload(w) for w in self.config.load_balancer.workloads
            ]
            all_containers: List[Container] = [
                container for node in nodes for container in node.containers
            ]
            target_containers: List[Container] = [
                container
                for container in all_containers
                if container.name in self.config.load_balancer.target_containers
            ]
            self.load_balancer = FirstFitReservationContainerLoadBalancer(
                workload_reqs=workloads,
                containers=target_containers,
                use_reservations=self.config.load_balancer.reservation_enabled,
            )

    def run(self) -> None:
        """
        Runs the simulation and displays resource usage and visualization results.

        Raises:
            RuntimeError: If the simulation environment is not properly set up.
        """
        if not self.datacenter:
            raise RuntimeError(
                "Simulation environment is not set up. Call setup_simulation() first."
            )
        self.simulation.run(self.datacenter, simulation_time=self.config.duration)
        self.simulation.print_info()
        print("\nVisualization Results:")
        # self.datacenter.visualize_all_nodes()
        self.datacenter.nodes[0].visualize_all_containers()
        self.datacenter.nodes[1].visualize_all_containers()


def parse_cli_args() -> argparse.Namespace:
    """
    Parses CLI arguments to get the configuration file path.

    Returns:
        argparse.Namespace: Parsed CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Run a container simulation using a configuration file."
    )
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the YAML configuration file (e.g., configs/example.yml).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    # Parse CLI arguments
    args: argparse.Namespace = parse_cli_args()
    config_path: str = args.config

    # Parse the configuration file
    simulation_config: SimulationConfig = parse_simulation_config(config_path)

    # Initialize and run the simulation
    runner: SimulationRunner = SimulationRunner(simulation_config)
    runner.setup_simulation()
    runner.run()
