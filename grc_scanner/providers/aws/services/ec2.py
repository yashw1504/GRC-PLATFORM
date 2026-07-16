import boto3


class EC2Discovery:

    @staticmethod
    def discover(session):

        ec2 = session.client("ec2")

        response = ec2.describe_instances()

        assets = []

        for reservation in response["Reservations"]:

            for instance in reservation["Instances"]:

                assets.append({

                    "provider": "aws",

                    "service": "EC2",

                    "asset_id": instance["InstanceId"],

                    "asset_name": instance.get("PrivateDnsName", ""),

                    "region": ec2.meta.region_name,

                    "metadata": instance

                })

        return assets