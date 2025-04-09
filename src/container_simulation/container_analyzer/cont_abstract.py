"""
Abstract Base Class for Container and Service Analyzers

This module provides an abstract base class (`ContainerAnalyzerAbstract`) for analyzing
Docker containers and Swarm services. It defines methods for retrieving container/service
statistics, disk usage, and entity listings.

Classes:
    - ContainerAnalyzerAbstract:
        Abstract class defining common methods for container/service analysis.

Methods:
    - get_container_or_service_ref(container_or_service_id, container_or_service_name) -> str:
      Determines the reference ID or name of a container/service.
    - get_stats(container_or_service_id, container_or_service_name) -> dict:
      Abstract method to retrieve container/service statistics.
    - get_disk_usage(container_or_service_id, container_or_service_name, swarm_mode) -> float:
      Retrieves the total disk usage of a container or Swarm service.
    - get_entity() -> list[docker.models.containers.Container | docker.models.services.Service]:
      Abstract method to list all available containers or services.

Usage Example:
    class MyContainerAnalyzer(ContainerAnalyzerAbstract):
        def get_stats(self, container_id, container_name):
            return self.docker_client.containers.get(container_id).stats(stream=False)

        def get_entity(self):
            return self.docker_client.containers.list(all=True)

    analyzer = MyContainerAnalyzer()
    stats = analyzer.get_stats(container_id="0800b9b5426c")
"""

from logging import Logger
from typing import Optional
from abc import ABC, abstractmethod

import docker

from container_simulation.utils import get_logger

LOGGER: Logger = get_logger()


class ContainerAnalyzerAbstract(ABC):
    """
    Abstract base class for analyzing Docker containers and Swarm services.

    This class provides an interface for retrieving container/service statistics,
    disk usage, and entity listings, which should be implemented by subclasses.

    Attributes:
        docker_client (docker.DockerClient):
            A Docker client instance for interacting with the Docker API.
    """

    def __init__(
        self,
        docker_client: Optional[docker.DockerClient] = None,
    ) -> None:
        """
        Initializes the abstract container analyzer.

        Args:
            docker_client (Optional[docker.DockerClient]): A Docker client instance.
                If not provided, a new instance is created from the environment.
        """
        self.docker_client: docker.client.DockerClient = docker_client or docker.from_env()

    def get_container_or_service_ref(
        self,
        container_or_service_id: Optional[str] = None,
        container_or_service_name: Optional[str] = None,
    ) -> docker.models.containers.Container | docker.models.services.Service:
        """
        Determines the reference identifier for a container or Swarm service.

        If both `container_or_service_id` and `container_or_service_name` are provided,
        `container_or_service_id` is prioritized.

        Args:
            container_or_service_id (Optional[str]): The unique ID of the container/service.
            container_or_service_name (Optional[str]): The name of the container/service.

        Returns:
            docker.models.containers.Container | docker.models.services.Service:
                The Container or Service object.

        Raises:
            AttributeError: If neither `container_or_service_id` nor
                `container_or_service_name` is provided.
        """
        if container_or_service_id and container_or_service_name:
            LOGGER.warning(
                "Both 'container_or_service_id' and 'container_or_service_name' are provided. "
                "'container_or_service_id' will be used!"
            )
            container_ref: str = container_or_service_id
        elif container_or_service_id:
            container_ref: str = container_or_service_id
        elif container_or_service_name:
            container_ref: str = container_or_service_name
        else:
            error_msg: str = (
                "The 'container_or_service_id' or 'container_or_service_name' must be provided!"
            )
            LOGGER.critical(error_msg)
            raise AttributeError(error_msg)

        try:
            return self.docker_client.containers.get(container_ref)
        except Exception:
            return self.docker_client.services.get(container_ref)

    @abstractmethod
    def get_stats(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> dict:
        """
        Abstract method to retrieve statistics of a Docker container or Swarm service.

        Args:
            id (Optional[str]): The unique ID of the container/service.
            name (Optional[str]): The name of the container/service.

        Returns:
            dict: A dictionary containing statistics (e.g., CPU, RAM, Disk, Network usage).
        """
        pass

    def get_disk_usage(
        self,
        container_or_service_id: Optional[str] = None,
        container_or_service_name: Optional[str] = None,
        swarm_mode: bool = False,
    ) -> float:
        """
        Retrieves the total disk usage of a Docker container or a Swarm service.

        If Swarm mode is enabled, it calculates the total disk usage for all tasks (replicas)
        of a given service.

        Args:
            container_or_service_id (Optional[str]): The unique ID of the container/service.
            container_or_service_name (Optional[str]): The name of the container/service.
            swarm_mode (bool, optional): Whether the target is a Swarm service (default: False).

        Returns:
            float: Total disk usage in MB. If the container/service is not found, returns 0.0.
        """
        disk_info: dict = self.docker_client.df()  # Get system-wide disk usage details

        if swarm_mode:
            # Get all tasks (containers) belonging to the service
            tasks: list = self.docker_client.api.tasks(
                filters={"service": container_or_service_name}
            )
            if not tasks:
                LOGGER.warning(f"No tasks found for service {container_or_service_name}")
                return 0.0

            total_disk_usage: float = 0.0
            for task in tasks:
                if "Status" in task and "ContainerStatus" in task["Status"]:
                    container_id: str = task["Status"]["ContainerStatus"].get("ContainerID")
                    if not container_id:
                        continue

                    # Find the corresponding container disk usage
                    for container in disk_info["Containers"]:
                        if container["Id"].startswith(container_id):
                            total_disk_usage += container["SizeRootFs"] / (
                                1024**2
                            )  # Convert bytes to MB

            return round(total_disk_usage, 2)

        else:
            # Normal mode: Get disk usage for a single container
            container_ref: docker.models.containers.Container | docker.models.services.Service = (
                self.get_container_or_service_ref(
                    container_or_service_id, container_or_service_name
                )
            )
            for container in disk_info["Containers"]:
                if container["Id"].startswith(container_ref.id) or any(
                    container_ref.name in name for name in container["Names"]
                ):
                    return round(container["SizeRootFs"] / (1024**2), 2)  # Convert bytes to MB

        return 0.0  # If container/service ID is not found

    @abstractmethod
    def get_entity(
        self,
    ) -> list[docker.models.containers.Container | docker.models.services.Service]:
        """
        Abstract method to list all available containers or services.

        Returns:
            list[docker.models.containers.Container | docker.models.services.Service]:
            A list of container or service entities.
        """
        pass

    @abstractmethod
    def get_name_or_id(
        self, entity_id: Optional[str] = None, entity_name: Optional[str] = None
    ) -> str:
        """
        Abstract method to provide the docker entity ID or name.
        If the ID is provided, then the Name will be returned.
        If the Name is provided, then the ID will be returned.
        None of the parameters or all of the parameters are set then Exception is raised.

        Returns:
            str: The ID or Name of the entity
        """
        pass
