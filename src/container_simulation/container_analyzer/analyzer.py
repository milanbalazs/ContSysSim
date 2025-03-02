from typing import Optional

from container_simulation.container_analyzer.container_analyzer import ContainerAnalyzer
from container_simulation.container_analyzer.service_analyzer import ServiceAnalyzer


class ContainerizedSystemAnalyzer:
    def __init__(self, swarm_mode: bool = False, entries: Optional[list[str]] = None):
        self.entries = entries or ["cpu", "ram", "bw"]
        if swarm_mode:
            analyzer: ServiceAnalyzer = ServiceAnalyzer()
        else:
            analyzer: ContainerAnalyzer = ContainerAnalyzer()
