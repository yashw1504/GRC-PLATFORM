from azure.identity import (
    ClientSecretCredential
)

from grc_scanner.config.settings import (
    Settings
)


class AzureAuth:

    @staticmethod
    def get_credential():

        if not (
            Settings.AZURE_CLIENT_ID
            and
            Settings.AZURE_CLIENT_SECRET
            and
            Settings.AZURE_TENANT_ID
        ):

            return None

        return ClientSecretCredential(
            tenant_id=Settings.AZURE_TENANT_ID,
            client_id=Settings.AZURE_CLIENT_ID,
            client_secret=Settings.AZURE_CLIENT_SECRET
        )