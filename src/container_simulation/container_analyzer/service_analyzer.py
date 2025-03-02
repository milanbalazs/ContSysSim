from logging import Logger
from typing import Optional

import docker

from container_simulation.container_analyzer.cont_abstract import ContainerAnalyzerAbstract
from container_simulation.utils import get_logger

LOGGER: Logger = get_logger()


class ServiceAnalyzer(ContainerAnalyzerAbstract):
    def __init__(
        self,
        container_id: Optional[str] = None,
        container_name: Optional[str] = None,
        docker_client: Optional[docker.DockerClient] = None,
    ) -> None:
        super().__init__(container_id, container_name, docker_client)

    def get_stats(self) -> dict:
        container_stat: docker.models.services.Service = self.docker_client.services.get(
            self.container_ref
        )
        status: dict = container_stat.attrs
        return status


# JUST FOR TESTING
if __name__ == "__main__":
    sa = ServiceAnalyzer("0800b9b5426c")
    print(sa.get_stats())
