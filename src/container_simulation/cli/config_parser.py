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
    cpu_saturation_percent: float
    ram_saturation_percent: float
    disk_saturation_percent: float
    bandwidth_saturation_percent: float
    priority: int
    type: str


@dataclass
class Container:
    """Represents a container within a VM."""

    name: str
    cpu: int
    ram: int
    disk: int
    bandwidth: int
    cpu_saturation_percent: float
    ram_saturation_percent: float
    disk_saturation_percent: float
    bandwidth_saturation_percent: float
    workloads: List[Workload] = field(default_factory=list)


@dataclass
class VM:
    """Represents a Virtual Machine (VM) in the data center."""

    name: str
    cpu: int
    ram: int
    disk: int
    bandwidth: int
    cpu_saturation_percent: float
    ram_saturation_percent: float
    disk_saturation_percent: float
    bandwidth_saturation_percent: float
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
    """Represents a data center with a list of VMs."""

    name: str
    vms: List[VM] = field(default_factory=list)


@dataclass
class SimulationConfig:
    """Root configuration for the simulation."""

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
    workloads = [parse_workload(w) for w in data.get("workloads", [])]
    return Container(
        name=data["name"],
        cpu=data["cpu"],
        ram=data["ram"],
        disk=data["disk"],
        bandwidth=data["bandwidth"],
        cpu_saturation_percent=data["cpu_saturation_percent"],
        ram_saturation_percent=data["ram_saturation_percent"],
        disk_saturation_percent=data["disk_saturation_percent"],
        bandwidth_saturation_percent=data["bandwidth_saturation_percent"],
        workloads=workloads,
    )


def parse_vm(data: dict) -> VM:
    """Parses a VM configuration from a dictionary.

    Args:
        data (dict): The dictionary containing VM details.

    Returns:
        VM: The parsed VM object.
    """
    containers = [parse_container(c) for c in data.get("containers", [])]
    return VM(
        name=data["name"],
        cpu=data["cpu"],
        ram=data["ram"],
        disk=data["disk"],
        bandwidth=data["bandwidth"],
        cpu_saturation_percent=data["cpu_saturation_percent"],
        ram_saturation_percent=data["ram_saturation_percent"],
        disk_saturation_percent=data["disk_saturation_percent"],
        bandwidth_saturation_percent=data["bandwidth_saturation_percent"],
        containers=containers,
    )


def parse_datacenter(data: dict) -> DataCenter:
    """Parses a data center configuration from a dictionary.

    Args:
        data (dict): The dictionary containing data center details.

    Returns:
        DataCenter: The parsed DataCenter object.
    """
    vms = [parse_vm(vm) for vm in data.get("vms", [])]
    return DataCenter(name=data["name"], vms=vms)


def parse_load_balancer(data: dict) -> LoadBalancer:
    """Parses a load balancer configuration from a dictionary.

    Args:
        data (dict): The dictionary containing load balancer details.

    Returns:
        LoadBalancer: The parsed LoadBalancer object.
    """
    workloads = [parse_workload(w) for w in data.get("workloads", [])]
    return LoadBalancer(
        enabled=data["enabled"],
        type=data["type"],
        reservation_enabled=data.get("reservation_enabled"),
        strategy_parameters=data.get("strategy_parameters"),
        workloads=workloads,
        target_containers=data.get("target_containers", []),  # Parse target containers
    )


def parse_simulation_config(config_path: str) -> SimulationConfig:
    """Parses the simulation configuration from a YAML file.

    Args:
        config_path (str): The path to the YAML configuration file.

    Returns:
        SimulationConfig: The parsed simulation configuration.
    """
    with open(config_path, "r") as file:
        config_data = yaml.safe_load(file)

    datacenter = parse_datacenter(config_data["datacenter"])
    load_balancer = None
    if "load_balancer" in config_data:
        load_balancer = parse_load_balancer(config_data["load_balancer"])

    return SimulationConfig(datacenter=datacenter, load_balancer=load_balancer)


if __name__ == "__main__":
    # Example usage
    config_file = "../../../configs/example.yml"  # Replace with your YAML file path
    simulation_config = parse_simulation_config(config_file)

    # Print parsed configuration for verification
    print(simulation_config)
