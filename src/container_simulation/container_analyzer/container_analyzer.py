from logging import Logger
from typing import Optional

import docker

from container_simulation.utils import get_logger

LOGGER: Logger = get_logger()


class ContainerAnalyzer:
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

    def get_container_stats(self) -> dict:
        container_stat: docker.models.containers.Container = self.docker_client.containers.get(
            self.container_ref
        )
        status: dict = container_stat.stats(decode=None, stream=False)
        return status


if __name__ == "__main__":
    ca = ContainerAnalyzer("0800b9b5426c")
    print(ca.get_container_stats())
