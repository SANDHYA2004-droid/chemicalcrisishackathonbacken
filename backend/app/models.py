from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from .database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    incident_type = Column(String, nullable=False)

    location = Column(String, nullable=False)

    severity = Column(Integer, nullable=False)

    people_affected = Column(Integer, default=0)

    chemical = Column(String, nullable=True)

    fire = Column(Boolean, default=False)

    status = Column(String, default="active")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)

    resource_type = Column(String, nullable=False)

    name = Column(String, nullable=False)

    location = Column(String, nullable=False)

    available = Column(Boolean, default=True)

    status = Column(String, default="available")