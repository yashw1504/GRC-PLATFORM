from grc_scanner.config.settings import (
    Settings
)


class GCPAuth:

    @staticmethod
    def get_credentials():

        if not (
            Settings.GOOGLE_APPLICATION_CREDENTIALS
        ):

            return None

        return (
            Settings
            .GOOGLE_APPLICATION_CREDENTIALS
        )