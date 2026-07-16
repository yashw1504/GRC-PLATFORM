class SecurityGroupDiscovery:

    @staticmethod
    def discover(session):

        ec2 = session.client("ec2")

        response = ec2.describe_security_groups()

        assets = []

        for sg in response["SecurityGroups"]:

            assets.append({

                "provider": "aws",

                "service": "Security Group",

                "asset_id": sg["GroupId"],

                "asset_name": sg["GroupName"],

                "region": ec2.meta.region_name,

                "metadata": sg

            })

        return assets