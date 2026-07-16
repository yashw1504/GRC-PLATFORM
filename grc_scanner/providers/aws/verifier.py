import boto3

from botocore.exceptions import ClientError

from botocore.exceptions import NoCredentialsError

from botocore.exceptions import EndpointConnectionError


class AWSVerifier:

    @staticmethod
    def verify(credentials):

        try:

            session = boto3.Session(

                aws_access_key_id=credentials["accessKey"],

                aws_secret_access_key=credentials["secretKey"],

                region_name=credentials.get(
                    "region",
                    "ap-south-1"
                )

            )

            sts = session.client("sts")

            identity = sts.get_caller_identity()

            return {

                "success": True,

                "account": identity["Account"],

                "arn": identity["Arn"],

                "user_id": identity["UserId"]

            }

        except NoCredentialsError:

            return {

                "success": False,

                "message": "Credentials not found"

            }

        except EndpointConnectionError:

            return {

                "success": False,

                "message": "Unable to connect to AWS"

            }

        except ClientError as e:

            return {

                "success": False,

                "message": str(e)

            }

        except Exception as e:

            return {

                "success": False,

                "message": str(e)

            }