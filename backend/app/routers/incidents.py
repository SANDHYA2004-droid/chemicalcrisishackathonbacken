from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Incident
from ..schemas import IncidentCreate, IncidentResponse


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.post("/", response_model=IncidentResponse)
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db)
):

    new_incident = Incident(
        incident_type=incident.incident_type,
        location=incident.location,
        severity=incident.severity,
        people_affected=incident.people_affected,
        chemical=incident.chemical,
        fire=incident.fire
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    return new_incident


@router.get("/")
def get_incidents(
    db: Session = Depends(get_db)
):

    return db.query(Incident).all()


@router.get("/{incident_id}")
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        Incident
    ).filter(
        Incident.id == incident_id
    ).first()