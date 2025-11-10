from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from services.jwt_service import get_company_from_token
from database import get_database
from models.station_model import Station

router = APIRouter(prefix="/stations", tags=["stations"])

@router.get("/", response_model=list[Station])
def get_stations(company_id: str = Depends(get_company_from_token)):
    """Return all stations belonging to the authenticated company."""
    db = get_database()
    stations = list(db.stations.find({"company_id": company_id}))
    return stations

@router.put("/", response_model=Station, status_code=status.HTTP_201_CREATED)
def add_station(station: Station, company_id: str = Depends(get_company_from_token)):
    """Add a new station for the authenticated company."""
    db = get_database()

    # Override any provided company_id
    data = station.dict(exclude_unset=True, by_alias=True)
    data["company_id"] = company_id
    data.pop("_id", None)

    result = db.stations.insert_one(data)
    new_station = db.stations.find_one({"_id": result.inserted_id})
    return new_station

@router.patch("/{station_id}", response_model=Station)
def edit_station(station_id: str, station: Station, company_id: str = Depends(get_company_from_token)):
    """Edit an existing station (full update)."""
    db = get_database()
    obj_id = ObjectId(station_id)

    existing = db.stations.find_one({"_id": obj_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Station not found")
    if existing["company_id"] != company_id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this station")

    update_data = station.dict(exclude_unset=True, by_alias=True)
    update_data.pop("_id", None)
    update_data["company_id"] = company_id  # always enforce from JWT

    db.stations.update_one({"_id": obj_id}, {"$set": update_data})
    updated = db.stations.find_one({"_id": obj_id})
    return updated

@router.delete("/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_station(station_id: str, company_id: str = Depends(get_company_from_token)):
    """Delete a station belonging to the authenticated company."""
    db = get_database()
    obj_id = ObjectId(station_id)

    existing = db.stations.find_one({"_id": obj_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Station not found")
    if existing["company_id"] != company_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this station")

    db.stations.delete_one({"_id": obj_id})
    return None