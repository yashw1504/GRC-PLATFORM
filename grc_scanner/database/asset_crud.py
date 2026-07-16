from sqlalchemy.orm import Session

from grc_scanner.database.models.asset import Asset


class AssetCRUD:

    @staticmethod
    def save_assets(

        db,

        assets

    ):

        db.add_all(assets)

        db.commit()

        return assets

    @staticmethod
    def list_assets(db):

        return db.query(Asset).all()

    @staticmethod
    def delete_assets(

        db,

        credential_id

    ):

        db.query(Asset).filter(

            Asset.credential_id == credential_id

        ).delete()

        db.commit()