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
    def get_container_or_service_ref(
        container_or_service_id: Optional[str] = None,
        container_or_service_name: Optional[str] = None,
    ) -> str:
        if container_or_service_id and container_or_service_name:
            LOGGER.warning(
                "The both of 'container_or_service_id', 'container_or_service_name' parameters are defined. "
                "'container_or_service_id' will be used!"
            )
            container_ref: str = container_or_service_id
        elif container_or_service_id:
            container_ref: str = container_or_service_id
        elif container_or_service_name:
            container_ref: str = container_or_service_name
        else:
            error_msg: str = (
                "The 'container_or_service_id' or 'container_or_service_name' has to be defined!"
            )
            LOGGER.critical(error_msg)
            raise AttributeError(error_msg)

        return container_ref

    @abstractmethod
    def get_stats(
        self,
        container_or_service_id: Optional[str] = None,
        container_or_service_name: Optional[str] = None,
    ) -> dict:
        pass

    def get_disk_usage(
        self,
        container_or_service_id: Optional[str] = None,
        container_or_service_name: Optional[str] = None,
        swarm_mode: bool = False,
    ) -> float:
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
            container_ref: str = self.get_container_or_service_ref(
                container_or_service_id, container_or_service_name
            )
            for container in disk_info["Containers"]:
                if container["Id"].startswith(container_ref) or any(
                    container_ref in name for name in container["Names"]
                ):
                    return round(container["SizeRootFs"] / (1024**2), 2)  # Convert bytes to MB

        return 0.0  # If container/service ID is not found

    @abstractmethod
    def get_entity(
        self,
    ) -> list[docker.models.containers.Container | docker.models.services.Service]:
        pass
