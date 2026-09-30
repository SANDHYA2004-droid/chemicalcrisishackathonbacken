from fastapi import APIRouter

from ..data_loader import (
    incidents,
    resources,
    roads_with_status,
    hospitals,
    shelters,
    chemicals,
)


router = APIRouter(
    prefix="/data",
    tags=["Dataset"]
)


@router.get("/incidents")
def get_dataset_incidents():
    df = incidents()

    return {
        "count": len(df),
        "data": df.to_dict(orient="records")
    }


@router.get("/resources")
def get_dataset_resources():
    df = resources()

    return {
        "count": len(df),
        "data": df.to_dict(orient="records")
    }


@router.get("/roads")
def get_dataset_roads():
    df = roads_with_status()

    return {
        "count": len(df),
        "data": df.to_dict(orient="records")
    }


@router.get("/hospitals")
def get_dataset_hospitals():
    df = hospitals()

    return {
        "count": len(df),
        "data": df.to_dict(orient="records")
    }


@router.get("/shelters")
def get_dataset_shelters():
    df = shelters()

    return {
        "count": len(df),
        "data": df.to_dict(orient="records")
    }


@router.get("/chemicals")
def get_dataset_chemicals():
    df = chemicals()

    return {
        "count": len(df),
        "data": df.to_dict(orient="records")
    }