from .base_provider import BaseProvider


class AzureProvider(BaseProvider):

    def verify_credentials(self, credential_data):

        return {

            "success": True

        }

    def discover_assets(self, credential_data):

        return []

    def get_regions(self, credential_data):

        return []

    def run_scan(self, credential_data, asset):

        return []