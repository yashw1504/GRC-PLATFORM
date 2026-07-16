import boto3


class S3Discovery:

    @staticmethod
    def discover(session):

        s3 = session.client("s3")

        response = s3.list_buckets()

        assets = []

        for bucket in response["Buckets"]:

            assets.append({

                "provider": "aws",

                "service": "S3",

                "asset_id": bucket["Name"],

                "asset_name": bucket["Name"],

                "region": "global",

                "metadata": bucket

            })

        return assets