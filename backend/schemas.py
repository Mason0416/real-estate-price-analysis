from pydantic import BaseModel, Field
from typing import Optional, Dict

class PropertyAnalysisRequest(BaseModel):
    address: str
    askingPrice: float
    area: float
    age: int
    buildingType: str
    floor: Optional[int] = None
    totalFloors: int
    parking: str
    layout: str
    rooms: int
    livingRooms: int
    bathrooms: int
    weights: Optional[Dict[str, float]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "address": "台北市大安區復興南路一段390號",
                "askingPrice": 1688,
                "area": 30,
                "age": 10,
                "buildingType": "電梯大樓",
                "totalFloors": 12,
                "parking": "yes",
                "layout": "2房1廳1衛",
                "rooms": 2,
                "livingRooms": 1,
                "bathrooms": 1,
                "weights": {
                    "price": 20,
                    "mrt": 20,
                    "hospital": 20,
                    "school": 20,
                    "park": 20
                }
            }
        }

class FacilityInfo(BaseModel):
    distance: float
    score: int

class SimilarCase(BaseModel):
    address: str
    price: float
    area: float
    unit_price: float
    age: int
    layout: str
    rooms: int
    living_rooms: int
    bathrooms: int
    distance: float
    similarity_score: float
    transaction_date: str

class AnalysisResult(BaseModel):
    asking_price: float
    reasonable_price_range: Dict[str, float]
    price_assessment: str
    weighted_score: int
    nearby_facilities: Dict[str, FacilityInfo]
    similar_cases: list[SimilarCase]
    recommendation: str
    area: float

