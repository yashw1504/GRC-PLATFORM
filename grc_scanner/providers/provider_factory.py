from .aws_provider import AWSProvider
from .azure_provider import AzureProvider
from .gcp_provider import GCPProvider
from .docker_provider import DockerProvider
from .github_provider import GithubProvider
from .gitlab_provider import GitlabProvider
from .database_provider import DatabaseProvider
from .kubernetes_provider import KubernetesProvider
from .ssh_provider import SSHProvider
from .api_provider import APIProvider


class ProviderFactory:

    PROVIDERS = {

        "aws": AWSProvider,

        "azure": AzureProvider,

        "gcp": GCPProvider,

        "docker": DockerProvider,

        "github": GithubProvider,

        "gitlab": GitlabProvider,

        "database": DatabaseProvider,

        "kubernetes": KubernetesProvider,

        "ssh": SSHProvider,

        "api": APIProvider

    }

    @classmethod
    def get_provider(
        cls,
        provider
    ):

        provider_class = cls.PROVIDERS.get(provider)

        if provider_class is None:

            raise Exception(

                f"Unsupported provider {provider}"

            )

        return provider_class()