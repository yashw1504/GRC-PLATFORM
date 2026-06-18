import boto3

from grc_scanner.config.settings import (
    Settings
)


class AWSAuth:

    @staticmethod
    def get_session():

        if not (
            Settings.AWS_ACCESS_KEY_ID
            and
            Settings.AWS_SECRET_ACCESS_KEY
        ):

            return None

        return boto3.Session(
            aws_access_key_id=
                Settings.AWS_ACCESS_KEY_ID,

            aws_secret_access_key=
                Settings.AWS_SECRET_ACCESS_KEY,

            region_name=
                Settings.AWS_DEFAULT_REGION
        )