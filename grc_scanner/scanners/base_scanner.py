"""Base class for all scanners"""
from abc import ABC, abstractmethod
from typing import List
from grc_scanner.engine.finding import Finding

class BaseScanner(ABC):
    name: str = "BaseScanner"

    @abstractmethod
    def scan(self, target, **kwargs) -> List[Finding]:
        pass