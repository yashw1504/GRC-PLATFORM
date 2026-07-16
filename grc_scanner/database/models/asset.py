from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime

from grc_scanner.database.database import Base


class Asset(Base):

    __tablename__ = "assets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    credential_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    provider = Column(
        String(50),
        nullable=False
    )

    service = Column(
        String(100),
        nullable=False
    )

    asset_id = Column(
        String(255),
        nullable=False
    )

    asset_name = Column(
        String(255)
    )

    region = Column(
        String(100)
    )

    status = Column(
        String(50),
        default="Active"
    )

    metadata = Column(
        Text
    )

    discovered_at = Column(
        DateTime,
        default=datetime.utcnow
    )