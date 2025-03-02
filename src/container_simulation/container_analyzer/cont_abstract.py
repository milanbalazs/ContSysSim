from logging import Logger
from typing import Optional
from abc import ABC, abstractmethod

import docker

from container_simulation.utils import get_logger

LOGGER: Logger = get_logger()


class ContainerAnalyzerAbstract(ABC):
    def __init__(
        self,
        docker_client: Optional[docker.DockerClient] = None,
    ) -> None:
        self.docker_client: docker.client.DockerClient = docker_client or docker.from_env()

    @staticmethod
    def get_container_ref(
        container_id: Optional[str] = None,
        container_name: Optional[str] = None,
    ):
        if container_id and container_name:
            LOGGER.warning(
                "The both of 'container_id', 'container_name' parameters are defined. "
                "'container_id' will be used!"
            )
            container_ref: str = container_id
        elif container_id:
            container_ref: str = container_id
        elif container_name:
            container_ref: str = container_name
        else:
            error_msg: str = "The 'container_id' or 'container_name' has to be defined!"
            LOGGER.critical(error_msg)
            raise AttributeError(error_msg)

        return container_ref

    @abstractmethod
    def get_stats(
        self,
        container_id: Optional[str] = None,
        container_name: Optional[str] = None,
    ) -> dict:
        pass

    def get_disk_usage(
        self,
        container_id: Optional[str] = None,
        container_name: Optional[str] = None,
    ) -> float:
        container_ref: str = self.get_container_ref(container_id, container_name)
        disk_info = self.docker_client.df()  # Get system-wide disk usage details

        # Find container disk usage
        for container in disk_info["Containers"]:
            if container["Id"].startswith(container_ref) or any(
                container_ref in name for name in container["Names"]
            ):
                return round(container["SizeRootFs"] / (1024**2), 2)  # Convert bytes to MB

        return 0.0  # If container ID is not found
