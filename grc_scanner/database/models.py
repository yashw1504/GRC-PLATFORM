from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Boolean

from .database import Base


class Credential(Base):

    __tablename__ = "credentials"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    provider = Column(
        String(100),
        nullable=False
    )

    credential_type = Column(
        String(100),
        nullable=False
    )

    encrypted_data = Column(
        Text,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(50),
        default="Pending"
    )

    verified = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    last_verified = Column(
        DateTime,
        nullable=True
    )