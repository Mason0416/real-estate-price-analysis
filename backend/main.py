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
    "price": 0.20,
    "mrt": 0.20,
    "hospital": 0.20,
    "school": 0.20,
    "park": 0.20,
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
                # 台北市大安區復興南路一段
                {
                    "address": "台北市大安區復興南路一段100號",
                    "latitude": 25.0331,
                    "longitude": 121.5432,
                    "price": 1650,
                    "area": 30.0,
                    "age": 10,
                    "building_type": "building",
                    "floor": 5,
                    "total_floors": 12,
                    "layout": "2房1廳1衛",
                    "rooms": 2,
                    "living_rooms": 1,
                    "bathrooms": 1,
                    "transaction_date": "2024-01",
                    "district": "大安"
                },
                {
                    "address": "台北市大安區復興南路一段200號",
                    "latitude": 25.0334,
                    "longitude": 121.5435,
                    "price": 1800,
                    "area": 32.0,
                    "age": 8,
                    "building_type": "building",
                    "floor": 8,
                    "total_floors": 14,
                    "layout": "3房2廳2衛",
                    "rooms": 3,
                    "living_rooms": 2,
                    "bathrooms": 2,
                    "transaction_date": "2024-02",
                    "district": "大安"
                },
                {
                    "address": "台北市大安區復興南路一段300號",
                    "latitude": 25.0328,
                    "longitude": 121.5431,
                    "price": 1400,
                    "area": 28.0,
                    "age": 25,
                    "building_type": "apartment",
                    "floor": 3,
                    "total_floors": 5,
                    "layout": "2房1廳1衛",
                    "rooms": 2,
                    "living_rooms": 1,
                    "bathrooms": 1,
                    "transaction_date": "2024-03",
                    "district": "大安"
                },
                {
                    "address": "台北市大安區復興南路一段390號",
                    "latitude": 25.0322,
                    "longitude": 121.5430,
                    "price": 1700,
                    "area": 30.0,
                    "age": 10,
                    "building_type": "building",
                    "floor": 6,
                    "total_floors": 12,
                    "layout": "2房1廳1衛",
                    "rooms": 2,
                    "living_rooms": 1,
                    "bathrooms": 1,
                    "transaction_date": "2024-01",
                    "district": "大安"
                },
                {
                    "address": "台北市大安區復興南路一段85號",
                    "latitude": 25.0340,
                    "longitude": 121.5438,
                    "price": 3500,
                    "area": 55.0,
                    "age": 35,
                    "building_type": "house",
                    "floor": 1,
                    "total_floors": 3,
                    "layout": "4房2廳3衛",
                    "rooms": 4,
                    "living_rooms": 2,
                    "bathrooms": 3,
                    "transaction_date": "2024-02",
                    "district": "大安"
                },
                # 台北市大安區信義路
                {
                    "address": "台北市大安區信義路三段",
                    "latitude": 25.0325,
                    "longitude": 121.5305,
                    "price": 2100,
                    "area": 35.0,
                    "age": 5,
                    "building_type": "building",
                    "floor": 10,
                    "total_floors": 15,
                    "layout": "3房2廳2衛",
                    "rooms": 3,
                    "living_rooms": 2,
                    "bathrooms": 2,
                    "transaction_date": "2024-03",
                    "district": "大安"
                },
                {
                    "address": "台北市大安區信義路四段",
                    "latitude": 25.0322,
                    "longitude": 121.5312,
                    "price": 1950,
                    "area": 33.0,
                    "age": 7,
                    "building_type": "building",
                    "floor": 4,
                    "total_floors": 14,
                    "layout": "2房2廳1衛",
                    "rooms": 2,
                    "living_rooms": 2,
                    "bathrooms": 1,
                    "transaction_date": "2024-01",
                    "district": "大安"
                },
                {
                    "address": "台北市大安區信義路二段",
                    "latitude": 25.0329,
                    "longitude": 121.5298,
                    "price": 1550,
                    "area": 29.0,
                    "age": 28,
                    "building_type": "apartment",
                    "floor": 2,
                    "total_floors": 4,
                    "layout": "3房1廳2衛",
                    "rooms": 3,
                    "living_rooms": 1,
                    "bathrooms": 2,
                    "transaction_date": "2024-02",
                    "district": "大安"
                },
                {
                    "address": "台北市大安區信義路三段50號",
                    "latitude": 25.0326,
                    "longitude": 121.5301,
                    "price": 1780,
                    "area": 30.0,
                    "age": 12,
                    "building_type": "building",
                    "floor": 6,
                    "total_floors": 12,
                    "layout": "2房1廳1衛",
                    "rooms": 2,
                    "living_rooms": 1,
                    "bathrooms": 1,
                    "transaction_date": "2024-03",
                    "district": "大安"
                },
                {
                    "address": "台北市大安區信義路四段120號",
                    "latitude": 25.0321,
                    "longitude": 121.5315,
                    "price": 3200,
                    "area": 50.0,
                    "age": 30,
                    "building_type": "house",
                    "floor": 1,
                    "total_floors": 3,
                    "layout": "4房2廳3衛",
                    "rooms": 4,
                    "living_rooms": 2,
                    "bathrooms": 3,
                    "transaction_date": "2024-01",
                    "district": "大安"
                },
                # 台北市大安區大安路
                {
                    "address": "台北市大安區大安路一段",
                    "latitude": 25.0332,
                    "longitude": 121.5402,
                    "price": 1750,
                    "area": 31.0,
                    "age": 11,
                    "building_type": "building",
                    "floor": 7,
                    "total_floors": 12,
                    "layout": "2房1廳1衛",
                    "rooms": 2,
                    "living_rooms": 1,
                    "bathrooms": 1,
                    "transaction_date": "2024-02",
                    "district": "大安"
                },
                {
                    "address": "台北市大安區大安路二段",
                    "latitude": 25.0326,
                    "longitude": 121.5408,
                    "price": 1850,
                    "area": 32.0,
                    "age": 9,
                    "building_type": "building",
                    "floor": 9,
                    "total_floors": 14,
                    "layout": "3房2廳2衛",
                    "rooms": 3,
                    "living_rooms": 2,
                    "bathrooms": 2,
                    "transaction_date": "2024-03",
                    "district": "大安"
                },
                {
                    "address": "台北市大安區大安路一段50號",
                    "latitude": 25.0335,
                    "longitude": 121.5405,
                    "price": 1280,
                    "area": 27.0,
                    "age": 26,
                    "building_type": "apartment",
                    "floor": 4,
                    "total_floors": 5,
                    "layout": "2房1廳1衛",
                    "rooms": 2,
                    "living_rooms": 1,
                    "bathrooms": 1,
                    "transaction_date": "2024-01",
                    "district": "大安"
                },
                {
                    "address": "台北市大安區大安路二段80號",
                    "latitude": 25.0324,
                    "longitude": 121.5401,
                    "price": 1680,
                    "area": 30.0,
                    "age": 13,
                    "building_type": "building",
                    "floor": 3,
                    "total_floors": 12,
                    "layout": "2房1廳1衛",
                    "rooms": 2,
                    "living_rooms": 1,
                    "bathrooms": 1,
                    "transaction_date": "2024-02",
                    "district": "大安"
                },
                {
                    "address": "台北市大安區大安路一段150號",
                    "latitude": 25.0338,
                    "longitude": 121.5409,
                    "price": 3800,
                    "area": 60.0,
                    "age": 28,
                    "building_type": "house",
                    "floor": 1,
                    "total_floors": 3,
                    "layout": "5房2廳4衛",
                    "rooms": 5,
                    "living_rooms": 2,
                    "bathrooms": 4,
                    "transaction_date": "2024-03",
                    "district": "大安"
                },
                # 台北市信義區松山路
                {
                    "address": "台北市信義區松山路100號",
                    "latitude": 25.0342,
                    "longitude": 121.5782,
                    "price": 1200,
                    "area": 32.0,
                    "age": 10,
                    "building_type": "building",
                    "floor": 5,
                    "total_floors": 12,
                    "layout": "3房2廳2衛",
                    "rooms": 3,
                    "living_rooms": 2,
                    "bathrooms": 2,
                    "transaction_date": "2024-01",
                    "district": "信義"
                },
                {
                    "address": "台北市信義區松山路200號",
                    "latitude": 25.0345,
                    "longitude": 121.5785,
                    "price": 1150,
                    "area": 31.0,
                    "age": 12,
                    "building_type": "building",
                    "floor": 4,
                    "total_floors": 12,
                    "layout": "2房1廳1衛",
                    "rooms": 2,
                    "living_rooms": 1,
                    "bathrooms": 1,
                    "transaction_date": "2024-02",
                    "district": "信義"
                },
                {
                    "address": "台北市信義區松山路300號",
                    "latitude": 25.0338,
                    "longitude": 121.5779,
                    "price": 900,
                    "area": 28.0,
                    "age": 30,
                    "building_type": "apartment",
                    "floor": 3,
                    "total_floors": 5,
                    "layout": "2房1廳1衛",
                    "rooms": 2,
                    "living_rooms": 1,
                    "bathrooms": 1,
                    "transaction_date": "2024-03",
                    "district": "信義"
                },
                {
                    "address": "台北市信義區松山路50號",
                    "latitude": 25.0348,
                    "longitude": 121.5788,
                    "price": 1350,
                    "area": 34.0,
                    "age": 7,
                    "building_type": "building",
                    "floor": 9,
                    "total_floors": 14,
                    "layout": "3房2廳2衛",
                    "rooms": 3,
                    "living_rooms": 2,
                    "bathrooms": 2,
                    "transaction_date": "2024-01",
                    "district": "信義"
                },
                {
                    "address": "台北市信義區松山路150號",
                    "latitude": 25.0340,
                    "longitude": 121.5780,
                    "price": 2600,
                    "area": 48.0,
                    "age": 32,
                    "building_type": "house",
                    "floor": 1,
                    "total_floors": 2,
                    "layout": "4房2廳3衛",
                    "rooms": 4,
                    "living_rooms": 2,
                    "bathrooms": 3,
                    "transaction_date": "2024-02",
                    "district": "信義"
                },
                # 台北市信義區光復路
                {
                    "address": "台北市信義區光復路100號",
                    "latitude": 25.0332,
                    "longitude": 121.5582,
                    "price": 1450,
                    "area": 31.0,
                    "age": 9,
                    "building_type": "building",
                    "floor": 6,
                    "total_floors": 12,
                    "layout": "2房1廳1衛",
                    "rooms": 2,
                    "living_rooms": 1,
                    "bathrooms": 1,
                    "transaction_date": "2024-03",
                    "district": "信義"
                },
                {
                    "address": "台北市信義區光復路200號",
                    "latitude": 25.0335,
                    "longitude": 121.5585,
                    "price": 1580,
                    "area": 33.0,
                    "age": 6,
                    "building_type": "building",
                    "floor": 8,
                    "total_floors": 14,
                    "layout": "3房2廳2衛",
                    "rooms": 3,
                    "living_rooms": 2,
                    "bathrooms": 2,
                    "transaction_date": "2024-01",
                    "district": "信義"
                },
                {
                    "address": "台北市信義區光復路300號",
                    "latitude": 25.0328,
                    "longitude": 121.5579,
                    "price": 1100,
                    "area": 29.0,
                    "age": 28,
                    "building_type": "apartment",
                    "floor": 2,
                    "total_floors": 5,
                    "layout": "2房1廳1衛",
                    "rooms": 2,
                    "living_rooms": 1,
                    "bathrooms": 1,
                    "transaction_date": "2024-02",
                    "district": "信義"
                },
                {
                    "address": "台北市信義區光復路50號",
                    "latitude": 25.0339,
                    "longitude": 121.5589,
                    "price": 1520,
                    "area": 32.0,
                    "age": 8,
                    "building_type": "building",
                    "floor": 10,
                    "total_floors": 12,
                    "layout": "2房2廳1衛",
                    "rooms": 2,
                    "living_rooms": 2,
                    "bathrooms": 1,
                    "transaction_date": "2024-03",
                    "district": "信義"
                },
                {
                    "address": "台北市信義區光復路150號",
                    "latitude": 25.0330,
                    "longitude": 121.5580,
                    "price": 2900,
                    "area": 52.0,
                    "age": 29,
                    "building_type": "house",
                    "floor": 1,
                    "total_floors": 3,
                    "layout": "4房2廳3衛",
                    "rooms": 4,
                    "living_rooms": 2,
                    "bathrooms": 3,
                    "transaction_date": "2024-01",
                    "district": "信義"
                }
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
        address=request.address,
        area=request.area,
        age=request.age,
        building_type=request.buildingType,
        lat=lat,
        lon=lon,
        floor=request.floor,
        total_floors=request.totalFloors,
        rooms=request.rooms,
        living_rooms=request.livingRooms,
        bathrooms=request.bathrooms,
    )

    print("[DEBUG] Similar cases found:", len(similar_cases))

    if not similar_cases:
        print("[WARNING] No similar cases found, using fallback mock cases")

        asking_val = request.askingPrice if request.askingPrice > 0 else 1000.0
        area_val = request.area if request.area > 0 else 30.0
        similar_cases = [
            {
                "address": f"{request.address or '台北市大安區'}模擬案例一",
                "price": round(asking_val * 0.9, 0),
                "area": area_val,
                "unit_price": round((asking_val * 0.9) / area_val, 1),
                "age": max(1, request.age),
                "building_type": request.buildingType,
                "floor": request.floor,
                "total_floors": request.totalFloors,
                "layout": request.layout,
                "rooms": request.rooms,
                "living_rooms": request.livingRooms,
                "bathrooms": request.bathrooms,
                "distance": 150.0,
                "similarity_score": 10.0,
                "transaction_date": "2024-01",
            },
            {
                "address": f"{request.address or '台北市大安區'}模擬案例二",
                "price": round(asking_val * 0.95, 0),
                "area": area_val,
                "unit_price": round((asking_val * 0.95) / area_val, 1),
                "age": max(1, request.age + 2),
                "building_type": request.buildingType,
                "floor": request.floor,
                "total_floors": request.totalFloors,
                "layout": request.layout,
                "rooms": request.rooms,
                "living_rooms": request.livingRooms,
                "bathrooms": request.bathrooms,
                "distance": 250.0,
                "similarity_score": 15.0,
                "transaction_date": "2024-02",
            },
            {
                "address": f"{request.address or '台北市大安區'}模擬案例三",
                "price": round(asking_val * 1.05, 0),
                "area": area_val,
                "unit_price": round((asking_val * 1.05) / area_val, 1),
                "age": max(1, request.age - 1),
                "building_type": request.buildingType,
                "floor": request.floor,
                "total_floors": request.totalFloors,
                "layout": request.layout,
                "rooms": request.rooms,
                "living_rooms": request.livingRooms,
                "bathrooms": request.bathrooms,
                "distance": 350.0,
                "similarity_score": 18.0,
                "transaction_date": "2024-03",
            },
            {
                "address": f"{request.address or '台北市大安區'}模擬案例四",
                "price": round(asking_val * 0.88, 0),
                "area": area_val,
                "unit_price": round((asking_val * 0.88) / area_val, 1),
                "age": max(1, request.age + 5),
                "building_type": request.buildingType,
                "floor": request.floor,
                "total_floors": request.totalFloors,
                "layout": request.layout,
                "rooms": request.rooms,
                "living_rooms": request.livingRooms,
                "bathrooms": request.bathrooms,
                "distance": 450.0,
                "similarity_score": 25.0,
                "transaction_date": "2024-01",
            },
            {
                "address": f"{request.address or '台北市大安區'}模擬案例五",
                "price": round(asking_val * 1.12, 0),
                "area": area_val,
                "unit_price": round((asking_val * 1.12) / area_val, 1),
                "age": max(1, request.age - 3),
                "building_type": request.buildingType,
                "floor": request.floor,
                "total_floors": request.totalFloors,
                "layout": request.layout,
                "rooms": request.rooms,
                "living_rooms": request.livingRooms,
                "bathrooms": request.bathrooms,
                "distance": 500.0,
                "similarity_score": 28.0,
                "transaction_date": "2024-02",
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
        age=request.age,
        floor=request.floor,
        total_floors=request.totalFloors,
        parking=request.parking,
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
                score=facility_scores["mrt"],
            ),
            "hospital": FacilityInfo(
                distance=nearby_facilities["hospital"][0],
                score=facility_scores["hospital"],
            ),
            "school": FacilityInfo(
                distance=nearby_facilities["school"][0],
                score=facility_scores["school"],
            ),
            "park": FacilityInfo(
                distance=nearby_facilities["park"][0],
                score=facility_scores["park"],
            ),
        },
        similar_cases=[
            SimilarCase(
                address=case["address"],
                price=case["price"],
                area=case["area"],
                unit_price=case["unit_price"],
                age=case["age"],
                layout=case["layout"],
                rooms=case["rooms"],
                living_rooms=case["living_rooms"],
                bathrooms=case["bathrooms"],
                distance=case["distance"],
                similarity_score=case["similarity_score"],
                transaction_date=case["transaction_date"],
            )
            for case in similar_cases[:5]
        ],
        recommendation=recommendation,
        area=request.area,
    )