from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    # Azure

    AZURE_CLIENT_ID = os.getenv(
        "AZURE_CLIENT_ID"
    )

    AZURE_CLIENT_SECRET = os.getenv(
        "AZURE_CLIENT_SECRET"
    )

    AZURE_TENANT_ID = os.getenv(
        "AZURE_TENANT_ID"
    )

    AZURE_SUBSCRIPTION_ID = os.getenv(
        "AZURE_SUBSCRIPTION_ID"
    )

    # AWS

    AWS_ACCESS_KEY_ID = os.getenv(
        "AWS_ACCESS_KEY_ID"
    )

    AWS_SECRET_ACCESS_KEY = os.getenv(
        "AWS_SECRET_ACCESS_KEY"
    )

    AWS_DEFAULT_REGION = os.getenv(
        "AWS_DEFAULT_REGION"
    )

    # GCP

    GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS"
    )