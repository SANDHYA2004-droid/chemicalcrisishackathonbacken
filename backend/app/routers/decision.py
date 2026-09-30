from fastapi import APIRouter, HTTPException

from ..data_loader import incidents
from ..services.resource_service import find_available_resources
from ..services.hazard_service import find_chemical_scenarios
from ..services.medical_service import find_hospitals
from ..services.route_service import get_safe_roads
from ..services.evacuation_service import find_shelters


router = APIRouter(
    prefix="/decision",
    tags=["Crisis Decision"]
)


@router.get("/{incident_id}")
def generate_decision(incident_id: str):

    df = incidents()

    incident = df[
        df["incident_id"].astype(str) == str(incident_id)
    ]

    if incident.empty:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    row = incident.iloc[0]

    severity = int(row["severity"])
    people = int(row["people_affected"])
    chemical = str(row["chemical"])

    # Basic incident risk classification
    if severity >= 8:
        risk_level = "CRITICAL"
    elif severity >= 5:
        risk_level = "HIGH"
    elif severity >= 3:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    resources = find_available_resources()

    hospitals = find_hospitals(
        people_affected=people
    )

    shelters = find_shelters(
        people_affected=people
    )

    roads = get_safe_roads()

    hazard = None

    if chemical and chemical.lower() != "nan":
        hazard = find_chemical_scenarios(
            chemical
        )

    return {
        "incident": {
            "id": row["incident_id"],
            "plant": row["plant"],
            "type": row["type"],
            "severity": severity,
            "people_affected": people,
            "chemical": chemical,
            "fire": bool(row["fire"]),
            "explosion": bool(row["explosion"]),
            "location": {
                "x": row["x"],
                "y": row["y"]
            }
        },

        "risk": {
            "level": risk_level,
            "impact_score": row["incident_impact_score"]
        },

        "hazard": hazard,

        "resources": resources,

        "medical": {
            "affected_people": people,
            "hospitals": hospitals
        },

        "evacuation": shelters,

        "safe_roads": roads,

        "human_approval_required": True
    }