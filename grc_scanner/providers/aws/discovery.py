import boto3

from .services.ec2 import EC2Discovery
from .services.s3 import S3Discovery
from .services.iam import IAMDiscovery
from .services.security_groups import SecurityGroupDiscovery


class AWSDiscovery:

    @staticmethod
    def discover(credentials):

        session = boto3.Session(

            aws_access_key_id=credentials["accessKey"],

            aws_secret_access_key=credentials["secretKey"],

            region_name=credentials.get(
                "region",
                "ap-south-1"
            )

        )

        assets = []

        assets.extend(

            EC2Discovery.discover(session)

        )

        assets.extend(

            S3Discovery.discover(session)

        )

        assets.extend(

            IAMDiscovery.discover(session)

        )

        assets.extend(

            SecurityGroupDiscovery.discover(session)

        )

        return assets