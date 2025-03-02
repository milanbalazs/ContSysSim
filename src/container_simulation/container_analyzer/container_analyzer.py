from logging import Logger
from typing import Optional

import docker

from container_simulation.container_analyzer.cont_abstract import ContainerAnalyzerAbstract
from container_simulation.utils import get_logger

LOGGER: Logger = get_logger()


class ContainerAnalyzer(ContainerAnalyzerAbstract):
    def __init__(
        self,
        container_id: Optional[str] = None,
    ) -> None:
        super().__init__(container_id)

    def get_stats(
        self,
        container_id: Optional[str] = None,
        container_name: Optional[str] = None,
    ) -> dict:
        container_ref: str = self.get_container_ref(container_id, container_name)
        container_stat: docker.models.containers.Container = self.docker_client.containers.get(
            container_ref
        )
        status: dict = container_stat.stats(decode=None, stream=False)
        return status


# JUST FOR TESTING
if __name__ == "__main__":
    ca = ContainerAnalyzer()
    print(ca.get_stats("0800b9b5426c"))
