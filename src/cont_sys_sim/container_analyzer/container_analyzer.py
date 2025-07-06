"""
Container Analyzer for Docker Containers

This module implements the `ContainerAnalyzer` class, which provides methods to
retrieve container statistics and list running containers.

Classes:
    - ContainerAnalyzer: Retrieves resource statistics and container details.

Methods:
    - get_stats(container_id, container_name) -> dict:
      Retrieves real-time resource statistics (CPU, RAM, Disk, Network usage) for a given container.
    - get_entity() -> list[docker.models.containers.Container]:
      Lists all available Docker containers.

Usage Example:
    analyzer = ContainerAnalyzer()
    stats = analyzer.get_stats(container_id="0800b9b5426c")
    print(stats)
"""

from logging import Logger
from typing import Optional

import docker

from cont_sys_sim.container_analyzer.cont_abstract import ContainerAnalyzerAbstract
from cont_sys_sim.utils import get_logger

LOGGER: Logger = get_logger()


class ContainerAnalyzer(ContainerAnalyzerAbstract):
    """
    Concrete implementation of `ContainerAnalyzerAbstract` for analyzing Docker containers.

    This class provides methods to retrieve real-time resource statistics of
    running Docker containers and list all available containers.

    Attributes:
        docker_client (docker.DockerClient): Docker client instance for API interactions.
    """

    def __init__(
        self,
        container_id: Optional[str] = None,
    ) -> None:
        """
        Initializes the `ContainerAnalyzer`.

        Args:
            container_id (Optional[str]): The ID of the container to analyze (if any).
        """
        super().__init__(container_id)

    def get_stats(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> dict:
        """
        Retrieves real-time resource statistics for a specified Docker container.

        The statistics include CPU usage, RAM usage, disk I/O, and network I/O.

        Args:
            id (Optional[str]): The unique ID of the container.
            name (Optional[str]): The name of the container.

        Returns:
            dict: A dictionary containing container statistics, including:
                - CPU usage
                - RAM usage
                - Disk I/O
                - Network I/O
                - Process statistics

        Raises:
            docker.errors.NotFound: If the specified container is not found.
            docker.errors.APIError: If there is an error while fetching container stats.

        Example:
            >>> analyzer = ContainerAnalyzer()
            >>> stats = analyzer.get_stats(container_id="0800b9b5426c")
            >>> print(stats)
        """
        container_ref: docker.models.containers.Container = self.get_container_or_service_ref(
            id, name
        )
        status: dict = container_ref.stats(decode=None, stream=False)
        return status

    def get_entity(self) -> list[docker.models.containers.Container]:
        """
        Retrieves a list of all available Docker containers.

        Returns:
            list[docker.models.containers.Container]: A list of all containers.

        Example:
            >>> analyzer = ContainerAnalyzer()
            >>> containers = analyzer.get_entity()
            >>> for container in containers:
            >>>     print(container.name)
        """
        return self.docker_client.containers.list()

    def get_name_or_id(
        self, entity_id: Optional[str] = None, entity_name: Optional[str] = None
    ) -> str:
        """
        If the Container ID is provided, then the Container Name will be returned.
        If the Container Name is provided, then the Container ID will be returned.
        If none or both parameters are set, an exception is raised.

        Args:
            entity_id (Optional[str]): The Docker container ID.
            entity_name (Optional[str]): The Docker container name.

        Returns:
            str: The ID if name was given, or the name if ID was given.

        Raises:
            ValueError: If both or neither parameter are provided.
            docker.errors.NotFound: If no container matches the given ID or name.
        """

        if entity_name and entity_id:
            raise ValueError(
                f"Both 'entity_id' ({entity_id}) and 'entity_name' ({entity_name}) are provided. "
                "Provide only one."
            )

        if entity_name:
            container = self.docker_client.containers.get(entity_name)
            return container.id

        elif entity_id:
            container = self.docker_client.containers.get(entity_id)
            return container.name

        else:
            raise ValueError("One of 'entity_id' or 'entity_name' must be provided.")


# JUST FOR TESTING
if __name__ == "__main__":
    ca = ContainerAnalyzer()
    print(ca.get_stats("0800b9b5426c"))
