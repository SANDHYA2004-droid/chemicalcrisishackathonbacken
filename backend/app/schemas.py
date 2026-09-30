from pydantic import BaseModel
from typing import Optional


class IncidentCreate(BaseModel):
    incident_type: str
    location: str
    severity: int
    people_affected: int = 0
    chemical: Optional[str] = None
    fire: bool = False


class IncidentResponse(BaseModel):
    id: int
    incident_type: str
    location: str
    severity: int
    people_affected: int
    chemical: Optional[str] = None
    fire: bool
    status: str

    class Config:
        from_attributes = True


class ResourceCreate(BaseModel):
    resource_type: str
    name: str
    location: str
    available: bool = True