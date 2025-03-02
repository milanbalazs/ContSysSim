from logging import Logger
from typing import Optional
from abc import ABC, abstractmethod

import docker

from container_simulation.utils import get_logger

LOGGER: Logger = get_logger()


class ContainerAnalyzerAbstract(ABC):
    def __init__(
        self,
        container_id: Optional[str] = None,
        container_name: Optional[str] = None,
        docker_client: Optional[docker.DockerClient] = None,
    ) -> None:
        if container_id:
            self.container_ref: str = container_id
        elif container_name:
            self.container_ref: str = container_name
        elif container_id and container_name:
            LOGGER.warning(
                "The both of 'container_id', 'container_name' parameters are defined. "
                "'container_id' will be used!"
            )
            self.container_ref: str = container_id
        else:
            error_msg: str = "The 'container_id' or 'container_name' has to be defined!"
            LOGGER.critical(error_msg)
            raise AttributeError(error_msg)

        self.docker_client: docker.client.DockerClient = docker_client or docker.from_env()

    @abstractmethod
    def get_stats(self) -> dict:
        pass
