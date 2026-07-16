from abc import ABC
from abc import abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def verify_credentials(self, credential_data):

        pass

    @abstractmethod
    def discover_assets(self, credential_data):

        pass

    @abstractmethod
    def get_regions(self, credential_data):

        pass

    @abstractmethod
    def run_scan(self, credential_data, asset):

        pass