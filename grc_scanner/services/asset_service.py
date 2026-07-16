from grc_scanner.mappers.asset_mapper import AssetMapper

from grc_scanner.database.asset_crud import AssetCRUD

from grc_scanner.providers.aws.provider import AWSProvider


class AssetService:

    @staticmethod
    def discover(

        db,

        credential,

        credential_data

    ):

        provider = AWSProvider()

        assets = provider.discover(

            credential_data

        )

        mapped_assets = []

        for asset in assets:

            mapped_assets.append(

                AssetMapper.map(

                    asset,

                    credential.id

                )

            )

        AssetCRUD.delete_assets(

            db,

            credential.id

        )

        AssetCRUD.save_assets(

            db,

            mapped_assets

        )

        return mapped_assets