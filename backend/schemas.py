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
    weights: Optional[Dict[str, float]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "address": "台北市信義區光復路",
                "askingPrice": 1200,
                "area": 35,
                "age": 8,
                "buildingType": "電梯大樓",
                "totalFloors": 12,
                "parking": "yes",
                "layout": "3房2廳1衛",
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
    age: int
    transaction_date: str

class AnalysisResult(BaseModel):
    asking_price: float
    reasonable_price_range: Dict[str, float]
    price_assessment: str
    weighted_score: int
    nearby_facilities: Dict[str, FacilityInfo]
    similar_cases: list[SimilarCase]
    recommendation: str

