from .verifier import AWSVerifier

from .discovery import AWSDiscovery


class AWSProvider:

    def verify(

        self,

        credential_data

    ):

        return AWSVerifier.verify(

            credential_data

        )

    def discover(

        self,

        credential_data

    ):

        return AWSDiscovery.discover(

            credential_data

        )