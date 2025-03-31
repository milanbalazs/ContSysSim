import yaml
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Workload:
    """Represents a workload request for a container."""

    cpu: float
    ram: int
    disk: int
    bandwidth: int
    delay: float
    duration: float
    cpu_fluctuation_percent: float
    ram_fluctuation_percent: float
    disk_fluctuation_percent: float
    bandwidth_fluctuation_percent: float
    priority: int
    type: str


@dataclass
class Container:
    """Represents a container within a Node."""

    name: str
    cpu: int
    ram: int
    disk: int
    bandwidth: int
    start_up_delay: float
    cpu_fluctuation_percent: float
    ram_fluctuation_percent: float
    disk_fluctuation_percent: float
    bandwidth_fluctuation_percent: float
    workloads: List[Workload] = field(default_factory=list)


@dataclass
class Node:
    """Represents a Node in the data center."""

    name: str
    cpu: int
    ram: int
    disk: int
    bandwidth: int
    start_up_delay: float
    cpu_fluctuation_percent: float
    ram_fluctuation_percent: float
    disk_fluctuation_percent: float
    bandwidth_fluctuation_percent: float
    stop_lack_of_resource: bool
    containers: List[Container] = field(default_factory=list)


@dataclass
class LoadBalancer:
    """Represents the load balancer configuration."""

    enabled: bool
    type: str
    reservation_enabled: Optional[bool] = None
    strategy_parameters: Optional[dict] = None
    target_containers: List[str] = field(default_factory=list)
    workloads: List[Workload] = field(default_factory=list)


@dataclass
class DataCenter:
    """Represents a data center with a list of Nodes."""

    name: str
    nodes: List[Node] = field(default_factory=list)


@dataclass
class SimulationConfig:
    """Root configuration for the simulation."""

    duration: int
    datacenter: DataCenter
    load_balancer: Optional[LoadBalancer] = None


def parse_workload(data: dict) -> Workload:
    """Parses a workload configuration from a dictionary.

    Args:
        data (dict): The dictionary containing workload details.

    Returns:
        Workload: The parsed Workload object.
    """
    return Workload(**data)


def parse_container(data: dict) -> Container:
    """Parses a container configuration from a dictionary.

    Args:
        data (dict): The dictionary containing container details.

    Returns:
        Container: The parsed Container object.
    """
    workloads: list[Workload] = [parse_workload(w) for w in data.get("workloads", [])]
    return Container(
        name=data["name"],
        cpu=data["cpu"],
        ram=data["ram"],
        disk=data["disk"],
        bandwidth=data["bandwidth"],
        start_up_delay=data["start_up_delay"],
        cpu_fluctuation_percent=data["cpu_fluctuation_percent"],
        ram_fluctuation_percent=data["ram_fluctuation_percent"],
        disk_fluctuation_percent=data["disk_fluctuation_percent"],
        bandwidth_fluctuation_percent=data["bandwidth_fluctuation_percent"],
        workloads=workloads,
    )


def parse_node(data: dict) -> Node:
    """Parses a Node configuration from a dictionary.

    Args:
        data (dict): The dictionary containing Node details.

    Returns:
        Node: The parsed Node object.
    """
    containers: list[Container] = [parse_container(c) for c in data.get("containers", [])]
    return Node(
        name=data["name"],
        cpu=data["cpu"],
        ram=data["ram"],
        disk=data["disk"],
        bandwidth=data["bandwidth"],
        start_up_delay=data["start_up_delay"],
        cpu_fluctuation_percent=data["cpu_fluctuation_percent"],
        ram_fluctuation_percent=data["ram_fluctuation_percent"],
        disk_fluctuation_percent=data["disk_fluctuation_percent"],
        bandwidth_fluctuation_percent=data["bandwidth_fluctuation_percent"],
        stop_lack_of_resource=data["stop_lack_of_resource"],
        containers=containers,
    )


def parse_datacenter(data: dict) -> DataCenter:
    """Parses a data center configuration from a dictionary.

    Args:
        data (dict): The dictionary containing data center details.

    Returns:
        DataCenter: The parsed DataCenter object.
    """
    nodes: list[Node] = [parse_node(node) for node in data.get("nodes", [])]
    return DataCenter(name=data["name"], nodes=nodes)


def parse_load_balancer(data: dict) -> LoadBalancer:
    """Parses a load balancer configuration from a dictionary.

    Args:
        data (dict): The dictionary containing load balancer details.

    Returns:
        LoadBalancer: The parsed LoadBalancer object.
    """
    workloads: list[Workload] = [parse_workload(w) for w in data.get("workloads", [])]
    return LoadBalancer(
        enabled=data["enabled"],
        type=data["type"],
        reservation_enabled=data.get("reservation_enabled"),
        strategy_parameters=data.get("strategy_parameters"),
        workloads=workloads,
        target_containers=data.get("target_containers", []),  # Parse target containers
    )


def parse_simulation_fields(data: dict) -> dict:
    """Parses a simulation related configuration from a dictionary.

    Args:
        data (dict): The dictionary containing simulation details.

    Returns:
        LoadBalancer: The parsed simulation related configs in dict.
    """

    return data["simulation"]


def parse_simulation_config(config_path: str) -> SimulationConfig:
    """Parses the simulation configuration from a YAML file.

    Args:
        config_path (str): The path to the YAML configuration file.

    Returns:
        SimulationConfig: The parsed simulation configuration.
    """
    with open(config_path, "r") as file:
        config_data = yaml.safe_load(file)

    datacenter: DataCenter = parse_datacenter(config_data["datacenter"])
    load_balancer: Optional[LoadBalancer] = None
    if "load_balancer" in config_data:
        load_balancer = parse_load_balancer(config_data["load_balancer"])
    simulations_fields: dict = parse_simulation_fields(config_data)

    return SimulationConfig(
        datacenter=datacenter, load_balancer=load_balancer, duration=simulations_fields["duration"]
    )


# That part is used only for debugging.
if __name__ == "__main__":
    # Example usage
    config_file = "../../../configs/example.yml"  # Replace with your YAML file path
    simulation_config = parse_simulation_config(config_file)

    # Print parsed configuration for verification
    print(simulation_config)
