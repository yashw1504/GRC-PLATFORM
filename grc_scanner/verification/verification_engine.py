from grc_scanner.providers.provider_factory import ProviderFactory


class VerificationEngine:

    @staticmethod
    def verify(

        provider_name,

        credential_data

    ):

        provider = ProviderFactory.get_provider(

            provider_name

        )

        return provider.verify_credentials(

            credential_data

        )