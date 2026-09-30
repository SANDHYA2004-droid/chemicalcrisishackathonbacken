from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Incident, Resource

router = APIRouter(
    prefix="/replan",
    tags=["Command & Replanning"]
)


@router.post("/{incident_id}")
def replan(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        return {"error": "Incident not found"}

    resources = db.query(Resource).filter(
        Resource.available == True
    ).all()

    return {
        "incident_id": incident.id,
        "status": "REPLANNING_REQUIRED",
        "reason": "Incident state changed",

        "incident": {
            "type": incident.incident_type,
            "location": incident.location,
            "severity": incident.severity
        },

        "available_resources": [
            {
                "id": r.id,
                "name": r.name,
                "type": r.resource_type,
                "location": r.location
            }
            for r in resources
        ],

        "human_approval_required": True
    }


@router.post("/simulate-change/{incident_id}")
def simulate_change(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        return {"error": "Incident not found"}

    # Hazmat Team becomes unavailable
    hazmat_team = db.query(Resource).filter(
        Resource.name == "Hazmat Team 1"
    ).first()

    if hazmat_team:
        hazmat_team.available = False
        hazmat_team.status = "unavailable"

    # New explosion at Factory B
    new_incident = Incident(
        incident_type="Explosion",
        location="Factory B",
        severity=9,
        people_affected=15,
        chemical=None,
        fire=True,
        status="active"
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    # Remaining resources
    resources = db.query(Resource).filter(
        Resource.available == True
    ).all()

    return {
        "status": "PLAN_REVISED",

        "trigger": {
            "new_incident": "Explosion",
            "location": "Factory B",
            "severity": 9
        },

        "resource_change": {
            "resource": "Hazmat Team 1",
            "previous_status": "available",
            "new_status": "unavailable"
        },

        "original_incident": {
            "id": incident.id,
            "type": incident.incident_type,
            "location": incident.location,
            "severity": incident.severity
        },

        "new_incident": {
            "id": new_incident.id,
            "type": new_incident.incident_type,
            "location": new_incident.location,
            "severity": new_incident.severity
        },

        "updated_available_resources": [
            {
                "id": r.id,
                "name": r.name,
                "type": r.resource_type,
                "location": r.location
            }
            for r in resources
        ],

        "updated_actions": [
            "Keep Fire Team 1 assigned to Factory A",
            "Deploy available Rescue Team toward Factory B",
            "Do not assign unavailable Hazmat Team 1",
            "Reassess evacuation zones",
            "Recalculate safe routes",
            "Reassess toxic exposure risk",
            "Check medical capacity",
            "Notify emergency control-room operator"
        ],

        "replanning_reason": [
            "New explosion detected",
            "Hazmat resource became unavailable",
            "Original response plan is no longer valid"
        ],

        "human_approval_required": True
    }