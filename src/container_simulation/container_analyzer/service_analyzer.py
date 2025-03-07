"""
Service Analyzer for Docker Swarm Services

This module implements the `ServiceAnalyzer` class, which provides methods to
retrieve Swarm service statistics and list running services.

Classes:
    - ServiceAnalyzer: Retrieves resource statistics and service details.

Methods:
    - get_stats(service_id, service_name) -> dict:
      Retrieves real-time resource statistics (CPU, RAM, Disk...) for a given Swarm service.
    - get_entity() -> list[docker.models.services.Service]:
      Lists all available Docker Swarm services.

Usage Example:
    analyzer = ServiceAnalyzer()
    stats = analyzer.get_stats(service_id="0800b9b5426c")
    print(stats)
"""

from logging import Logger
from typing import Optional

import docker

from container_simulation.container_analyzer.cont_abstract import ContainerAnalyzerAbstract
from container_simulation.utils import get_logger

LOGGER: Logger = get_logger()


class ServiceAnalyzer(ContainerAnalyzerAbstract):
    """
    Concrete implementation of `ContainerAnalyzerAbstract` for analyzing Docker Swarm services.

    This class provides methods to retrieve real-time resource statistics of
    running Docker Swarm services and list all available services.

    Attributes:
        docker_client (docker.DockerClient): Docker client instance for API interactions.
    """

    def __init__(
        self,
        container_id: Optional[str] = None,
    ) -> None:
        """
        Initializes the `ServiceAnalyzer`.

        Args:
            container_id (Optional[str]):
                The ID of the container associated with the service (if any).
        """
        super().__init__(container_id)

    def get_stats(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> dict:
        """
        Retrieves real-time resource statistics for a specified Docker Swarm service.

        The statistics include CPU usage, RAM usage, disk I/O, and network I/O.

        Args:
            id (Optional[str]): The unique ID of the Swarm service.
            name (Optional[str]): The name of the Swarm service.

        Returns:
            dict: A dictionary containing service statistics, including:
                - CPU usage
                - RAM usage
                - Disk I/O
                - Network I/O
                - Process statistics

        Raises:
            docker.errors.NotFound: If the specified service is not found.
            docker.errors.APIError: If there is an error while fetching service stats.

        Example:
            >>> analyzer = ServiceAnalyzer()
            >>> stats = analyzer.get_stats(service_id="0800b9b5426c")
            >>> print(stats)
        """
        container_ref: docker.models.services.Service = self.get_container_or_service_ref(id, name)
        status: dict = container_ref.attrs
        return status

    def get_entity(self) -> list[docker.models.services.Service]:
        """
        Retrieves a list of all available Docker Swarm services.

        Returns:
            list[docker.models.services.Service]: A list of all Swarm services.

        Example:
            >>> analyzer = ServiceAnalyzer()
            >>> services = analyzer.get_entity()
            >>> for service in services:
            >>>     print(service.name)
        """
        return self.docker_client.services.list()


# JUST FOR TESTING
if __name__ == "__main__":
    sa = ServiceAnalyzer()
    print(sa.get_stats("0800b9b5426c"))
