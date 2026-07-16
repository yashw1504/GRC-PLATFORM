import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    APP_NAME = os.getenv(
        "APP_NAME",
        "GRC Platform"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./grc_platform.db"
    )

    ENCRYPTION_KEY = os.getenv(
        "ENCRYPTION_KEY"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "True"
    ) == "True"


settings = Settings()