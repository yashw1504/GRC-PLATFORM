"""Base class for all scanners"""
from abc import ABC, abstractmethod

class BaseScanner(ABC):
    name: str = "BaseScanner"

    @abstractmethod
    def scan(self, target, **kwargs):
        pass