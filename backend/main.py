from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from schemas import PropertyAnalysisRequest, AnalysisResult, FacilityInfo, SimilarCase
from analysis import (
    get_geocode_mock,
    find_similar_cases,
    calculate_reasonable_price,
    assess_price,
    calculate_facility_scores,
    calculate_property_scores,
    calculate_price_score,
    calculate_weighted_score,
    generate_recommendation,
    calculate_facility_distance_mock,
)
from database import SessionLocal, TransactionRecord


app = FastAPI(title="Property Price Analysis API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DEFAULT_WEIGHTS = {
    "price": 0.30,
    "mrt": 0.20,
    "hospital": 0.10,
    "school": 0.15,
    "park": 0.10,
    "age": 0.10,
    "area": 0.00,
    "floor": 0.00,
    "parking": 0.05,
}


def validate_and_normalize_weights(weights: Dict[str, float] | None) -> Dict[str, float]:
    if not weights:
        return DEFAULT_WEIGHTS

    valid_keys = set(DEFAULT_WEIGHTS.keys())

    filtered_weights = {}
    for key, value in weights.items():
        if key in valid_keys:
            try:
                filtered_weights[key] = float(value)
            except (TypeError, ValueError):
                filtered_weights[key] = 0.0

    if not filtered_weights:
        return DEFAULT_WEIGHTS

    total = sum(filtered_weights.values())

    if total <= 0:
        return DEFAULT_WEIGHTS

    normalized = {}
    for key in valid_keys:
        normalized[key] = round(filtered_weights.get(key, 0.0) / total, 4)

    return normalized


def seed_transaction_data():
    db = SessionLocal()

    try:
        count = db.query(TransactionRecord).count()

        if count == 0:
            sample_data = [
                {
                    "address": "台北市信義區光復路",
                    "latitude": 25.033,
                    "longitude": 121.567,
                    "price": 1200,
                    "area": 35,
                    "age": 8,
                    "building_type": "building",
                    "floor": 8,
                    "transaction_date": "2024-01",
                    "district": "信義",
                },
                {
                    "address": "台北市信義區松山路",
                    "latitude": 25.034,
                    "longitude": 121.568,
                    "price": 1150,
                    "area": 32,
                    "age": 10,
                    "building_type": "building",
                    "floor": 5,
                    "transaction_date": "2024-02",
                    "district": "信義",
                },
                {
                    "address": "台北市信義區仁愛路",
                    "latitude": 25.032,
                    "longitude": 121.566,
                    "price": 1300,
                    "area": 40,
                    "age": 5,
                    "building_type": "building",
                    "floor": 12,
                    "transaction_date": "2024-03",
                    "district": "信義",
                },
                {
                    "address": "台北市大安區大安路",
                    "latitude": 25.033,
                    "longitude": 121.530,
                    "price": 950,
                    "area": 30,
                    "age": 12,
                    "building_type": "apartment",
                    "floor": 3,
                    "transaction_date": "2024-01",
                    "district": "大安",
                },
                {
                    "address": "台北市大安區信義路",
                    "latitude": 25.032,
                    "longitude": 121.531,
                    "price": 1000,
                    "area": 32,
                    "age": 9,
                    "building_type": "apartment",
                    "floor": 4,
                    "transaction_date": "2024-02",
                    "district": "大安",
                },
            ]

            for data in sample_data:
                db.add(TransactionRecord(**data))

            db.commit()

    finally:
        db.close()


seed_transaction_data()


@app.get("/")
async def root():
    return {"message": "房屋價格合理性分析 API"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_property(request: PropertyAnalysisRequest):
    print("[DEBUG] Request:", request.model_dump())

    lat, lon = get_geocode_mock(request.address)

    nearby_facilities = {
        "mrt": calculate_facility_distance_mock(lat, lon, "mrt"),
        "hospital": calculate_facility_distance_mock(lat, lon, "hospital"),
        "school": calculate_facility_distance_mock(lat, lon, "school"),
        "park": calculate_facility_distance_mock(lat, lon, "park"),
    }

    similar_cases = find_similar_cases(
        request.address,
        request.area,
        request.age,
        request.buildingType,
        lat,
        lon,
    )

    print("[DEBUG] Similar cases found:", len(similar_cases))

    if not similar_cases:
        print("[WARNING] No similar cases found, using fallback mock cases")

        similar_cases = [
            {
                "address": "台北市信義區模擬案例",
                "price": 1200,
                "area": request.area,
                "age": request.age,
                "unit_price": 40,
                "transaction_date": "2024-01",
            },
            {
                "address": "台北市大安區模擬案例",
                "price": 1150,
                "area": request.area,
                "age": request.age,
                "unit_price": 38,
                "transaction_date": "2024-02",
            },
            {
                "address": "台北市松山區模擬案例",
                "price": 1250,
                "area": request.area,
                "age": request.age,
                "unit_price": 42,
                "transaction_date": "2024-03",
            },
        ]

    median_unit_price, reasonable_range = calculate_reasonable_price(similar_cases)

    reasonable_price_min = reasonable_range["min"] * request.area
    reasonable_price_max = reasonable_range["max"] * request.area

    price_assessment = assess_price(
        request.askingPrice,
        request.area,
        reasonable_range,
    )

    facility_scores = calculate_facility_scores(nearby_facilities)

    property_scores = calculate_property_scores(
        request.age,
        request.floor,
        request.totalFloors,
        request.parking,
    )

    price_score = calculate_price_score(
        request.askingPrice,
        request.area,
        reasonable_range,
    )

    weights = validate_and_normalize_weights(request.weights)

    print("[DEBUG] Normalized weights:", weights)
    print("[DEBUG] Weight sum:", sum(weights.values()))

    weighted_score = calculate_weighted_score(
        price_score,
        facility_scores,
        property_scores,
        weights,
    )

    recommendation = generate_recommendation(
        price_assessment,
        weighted_score,
        similar_cases,
    )

    return AnalysisResult(
        asking_price=request.askingPrice,
        reasonable_price_range={
            "min": round(reasonable_price_min, 0),
            "max": round(reasonable_price_max, 0),
        },
        price_assessment=price_assessment,
        weighted_score=weighted_score,
        nearby_facilities={
            "mrt": FacilityInfo(
                distance=nearby_facilities["mrt"][0],
                rating=nearby_facilities["mrt"][1],
            ),
            "hospital": FacilityInfo(
                distance=nearby_facilities["hospital"][0],
                rating=nearby_facilities["hospital"][1],
            ),
            "school": FacilityInfo(
                distance=nearby_facilities["school"][0],
                rating=nearby_facilities["school"][1],
            ),
            "park": FacilityInfo(
                distance=nearby_facilities["park"][0],
                rating=nearby_facilities["park"][1],
            ),
        },
        similar_cases=[
            SimilarCase(
                address=case["address"],
                price=case["price"],
                area=case["area"],
                age=case["age"],
                unit_price=case["unit_price"],
                transaction_date=case["transaction_date"],
            )
            for case in similar_cases[:3]
        ],
        recommendation=recommendation,
    )