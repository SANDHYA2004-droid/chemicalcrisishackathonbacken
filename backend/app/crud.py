from sqlalchemy.orm import Session

from . import models
from .schemas import IncidentCreate


def create_incident(
    db: Session,
    incident: IncidentCreate
):

    new_incident = models.Incident(
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


def get_incidents(db: Session):

    return db.query(
        models.Incident
    ).all()