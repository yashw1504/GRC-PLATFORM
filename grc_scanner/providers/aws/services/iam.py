class IAMDiscovery:

    @staticmethod
    def discover(session):

        iam = session.client("iam")

        response = iam.list_users()

        assets = []

        for user in response["Users"]:

            assets.append({

                "provider": "aws",

                "service": "IAM User",

                "asset_id": user["UserId"],

                "asset_name": user["UserName"],

                "region": "global",

                "metadata": user

            })

        return assets