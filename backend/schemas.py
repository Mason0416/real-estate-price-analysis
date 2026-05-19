from pydantic import BaseModel, Field
from typing import Optional, Dict

class PropertyAnalysisRequest(BaseModel):
    address: str
    askingPrice: float
    area: float
    age: int
    buildingType: str
    floor: int
    totalFloors: int
    parking: str
    layout: Optional[str] = None
    weights: Optional[Dict[str, float]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "address": "台北市信義區光復路",
                "askingPrice": 1200,
                "area": 35,
                "age": 8,
                "buildingType": "building",
                "floor": 8,
                "totalFloors": 12,
                "parking": "yes",
                "layout": "3房2廳1衛",
                "weights": {
                    "price": 0.30,
                    "mrt": 0.20,
                    "hospital": 0.10,
                    "school": 0.15,
                    "park": 0.10,
                    "age": 0.10,
                    "area": 0.00,
                    "floor": 0.00,
                    "parking": 0.05
                }
            }
        }

class FacilityInfo(BaseModel):
    distance: float
    rating: str

class SimilarCase(BaseModel):
    address: str
    price: float
    area: float
    age: int
    unit_price: float
    transaction_date: str

class AnalysisResult(BaseModel):
    asking_price: float
    reasonable_price_range: Dict[str, float]
    price_assessment: str
    weighted_score: float
    nearby_facilities: Dict[str, FacilityInfo]
    similar_cases: list[SimilarCase]
    recommendation: str

