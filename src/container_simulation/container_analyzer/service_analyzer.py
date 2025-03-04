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
    ) -> None:
        super().__init__(container_id)

    def get_stats(
        self,
        service_id: Optional[str] = None,
        service_name: Optional[str] = None,
    ) -> dict:
        container_ref: str = self.get_container_or_service_ref(service_id, service_name)
        container_stat: docker.models.services.Service = self.docker_client.services.get(
            container_ref
        )
        status: dict = container_stat.attrs
        return status

    def get_entity(self) -> list[docker.models.services.Service]:
        return self.docker_client.services.list(all=True)


# JUST FOR TESTING
if __name__ == "__main__":
    sa = ServiceAnalyzer()
    print(sa.get_stats("0800b9b5426c"))
