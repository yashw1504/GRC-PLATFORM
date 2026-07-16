import json

from grc_scanner.database.models.asset import Asset


class AssetMapper:

    @staticmethod
    def map(asset, credential_id):

        return Asset(

            credential_id=credential_id,

            provider=asset["provider"],

            service=asset["service"],

            asset_id=asset["asset_id"],

            asset_name=asset["asset_name"],

            region=asset["region"],

            metadata=json.dumps(
                asset["metadata"],
                default=str
            )

        )