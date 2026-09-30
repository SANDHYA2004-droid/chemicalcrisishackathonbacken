from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Resource
from ..schemas import ResourceCreate


router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


@router.post("/")
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db)
):

    new_resource = Resource(
        resource_type=resource.resource_type,
        name=resource.name,
        location=resource.location,
        available=resource.available
    )

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return new_resource


@router.get("/")
def get_resources(
    db: Session = Depends(get_db)
):

    return db.query(Resource).all()