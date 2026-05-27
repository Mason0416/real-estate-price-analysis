from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import statistics
from database import SessionLocal, TransactionRecord

def get_geocode_mock(address: str) -> Tuple[float, float]:
    district_coords = {
        '信義': (25.033, 121.567),
        '大安': (25.033, 121.530),
        '中山': (25.051, 121.530),
        '松山': (25.051, 121.567),
        '文山': (25.000, 121.530),
        '南港': (25.051, 121.610),
        '北投': (25.120, 121.510),
        '士林': (25.095, 121.510),
        '內湖': (25.070, 121.590),
        '中正': (25.015, 121.512),
    }

    for district, coords in district_coords.items():
        if district in address:
            return coords
    return (25.033, 121.567)

def calculate_facility_distance_mock(lat: float, lon: float, facility_type: str) -> Tuple[float, int]:
    distances = {
        'mrt': (450, 80),
        'hospital': (650, 60),
        'school': (200, 100),
        'park': (500, 80),
    }
    return distances.get(facility_type, (1000, 60))

def find_similar_cases(
    address: str,
    area: float,
    age: int,
    building_type: str,
    lat: float,
    lon: float,
    floor: Optional[int],
    total_floors: int,
    rooms: int,
    living_rooms: int,
    bathrooms: int,
) -> List[Dict]:
    db = SessionLocal()
    cases = db.query(TransactionRecord).all()
    db.close()

    if not cases:
        return []

    target_district = ""
    for d in ["大安", "信義", "中山", "松山", "文山", "南港", "北投", "士林", "內湖", "中正"]:
        if d in address:
            target_district = d
            break

    type_mapping = {
        "電梯大樓": "building",
        "公寓": "apartment",
        "透天": "house"
    }
    target_mapped_type = type_mapping.get(building_type, building_type)

    similar = []
    for case in cases:
        # Distance calculation
        dist_deg = ((case.latitude - lat) ** 2 + (case.longitude - lon) ** 2) ** 0.5
        distance_in_meters = dist_deg * 111000
        distance_score = distance_in_meters / 100

        # Area score
        area_score = abs(case.area - area) * 2

        # Age score
        age_score = abs(case.age - age) * 1.5

        # Building type score
        case_mapped_type = type_mapping.get(case.building_type, case.building_type)
        building_type_score = 0 if case_mapped_type == target_mapped_type else 50

        # Floor score
        if floor is None or case.floor is None:
            floor_score = 0
        else:
            floor_score = abs(case.floor - floor) * 2

        # Total floors score
        case_total_floors = case.total_floors if case.total_floors is not None else 1
        total_floors_score = abs(case_total_floors - total_floors) * 1

        # Rooms score
        case_rooms = case.rooms if case.rooms is not None else 0
        rooms_score = abs(case_rooms - rooms) * 10

        # Living rooms score
        case_living_rooms = case.living_rooms if case.living_rooms is not None else 0
        living_rooms_score = abs(case_living_rooms - living_rooms) * 8

        # Bathrooms score
        case_bathrooms = case.bathrooms if case.bathrooms is not None else 0
        bathrooms_score = abs(case_bathrooms - bathrooms) * 8

        # District score
        case_district = case.district if case.district else ""
        district_score = 0 if case_district == target_district else 30

        # Total similarity score
        score = (
            distance_score +
            area_score +
            age_score +
            building_type_score +
            floor_score +
            total_floors_score +
            rooms_score +
            living_rooms_score +
            bathrooms_score +
            district_score
        )

        similar.append({
            'address': case.address,
            'price': case.price,
            'area': case.area,
            'unit_price': round(case.price / case.area, 1),
            'age': case.age,
            'layout': case.layout if case.layout else f"{case_rooms}房{case_living_rooms}廳{case_bathrooms}衛",
            'rooms': case_rooms,
            'living_rooms': case_living_rooms,
            'bathrooms': case_bathrooms,
            'distance': round(distance_in_meters, 1),
            'similarity_score': round(score, 2),
            'transaction_date': case.transaction_date,
        })

    # Sort by similarity score ascending
    similar.sort(key=lambda x: x['similarity_score'])
    return similar[:5]

def calculate_reasonable_price(similar_cases: List[Dict]) -> Tuple[float, Dict[str, float]]:
    if not similar_cases:
        return None, None

    unit_prices = [case['unit_price'] for case in similar_cases]
    median_unit_price = statistics.median(unit_prices)

    return median_unit_price, {
        'min': round(median_unit_price * 0.9, 2),
        'max': round(median_unit_price * 1.1, 2),
    }

def assess_price(asking_price: float, area: float, reasonable_range: Dict[str, float]) -> str:
    seller_unit_price = asking_price / area
    min_price = reasonable_range['min']
    max_price = reasonable_range['max']

    if min_price <= seller_unit_price <= max_price:
        return '價格合理'

    if seller_unit_price < min_price:
        under_ratio = (min_price - seller_unit_price) / min_price
        if under_ratio <= 0.05:
            return '略低於市場合理價格'
        elif under_ratio <= 0.15:
            return '明顯低於市場合理價格，請確認是否有特殊條件'
        else:
            return '異常低價，請謹慎確認房屋狀況與產權'

    # seller_unit_price > max_price
    over_ratio = (seller_unit_price - max_price) / max_price
    if over_ratio <= 0.05:
        return '略高，建議議價'
    elif over_ratio <= 0.15:
        return '偏高，建議議價'
    elif over_ratio <= 0.30:
        return '明顯偏高'
    else:
        return '嚴重偏高，不建議直接購買'

def calculate_facility_scores(nearby_facilities: Dict[str, Tuple[float, int]]) -> Dict[str, int]:
    scores = {}

    for facility, (distance, base_score) in nearby_facilities.items():
        if distance <= 250:
            scores[facility] = 100
        elif distance <= 500:
            scores[facility] = 80
        elif distance <= 1000:
            scores[facility] = 60
        elif distance <= 1500:
            scores[facility] = 40
        else:
            scores[facility] = 20

    return scores

def calculate_property_scores(
    age: int,
    floor: Optional[int] = None,
    total_floors: Optional[int] = None,
    parking: str = "yes"
) -> Dict[str, int]:
    if age < 5:
        age_score = 100
    elif age < 10:
        age_score = 80
    elif age < 20:
        age_score = 60
    elif age < 30:
        age_score = 40
    else:
        age_score = 20

    floor_score = 60
    if floor is not None and total_floors is not None:
        if floor == 1:
            floor_score = 80
        elif floor == total_floors:
            floor_score = 60
        elif floor >= 4 and total_floors <= 5:
            floor_score = 40
        else:
            floor_score = 100
    else:
        floor_score = 100

    parking_score = 100 if parking in ["yes", "有", "y"] else 40

    return {
        'age': age_score,
        'floor': floor_score,
        'parking': parking_score,
    }

def calculate_price_score(asking_price: float, area: float, reasonable_range: Dict[str, float]) -> int:
    seller_unit_price = asking_price / area
    min_price = reasonable_range['min']
    max_price = reasonable_range['max']

    if min_price <= seller_unit_price <= max_price:
        return 100

    if seller_unit_price < min_price:
        under_ratio = (min_price - seller_unit_price) / min_price
        if under_ratio <= 0.05:
            return 80
        elif under_ratio <= 0.15:
            return 60
        else:
            return 40

    # seller_unit_price > max_price
    over_ratio = (seller_unit_price - max_price) / max_price
    if over_ratio <= 0.05:
        return 80
    elif over_ratio <= 0.15:
        return 60
    elif over_ratio <= 0.30:
        return 40
    else:
        return 20

def calculate_weighted_score(
    price_score: int,
    facility_scores: Dict[str, int],
    property_scores: Dict[str, int],
    weights: Dict[str, float],
) -> int:
    total_weight = sum(weights.values())

    if total_weight == 0:
        total_weight = 1

    normalized_weights = {k: v / total_weight for k, v in weights.items()}

    total_score = (
        price_score * normalized_weights.get('price', 0) +
        facility_scores.get('mrt', 60) * normalized_weights.get('mrt', 0) +
        facility_scores.get('hospital', 60) * normalized_weights.get('hospital', 0) +
        facility_scores.get('school', 60) * normalized_weights.get('school', 0) +
        facility_scores.get('park', 60) * normalized_weights.get('park', 0)
    )

    divided = total_score / 20
    rounded_multiplier = int(divided + 0.5)
    final_score = max(20, min(100, rounded_multiplier * 20))

    return final_score

def generate_recommendation(
    price_assessment: str,
    weighted_score: float,
    similar_cases: List[Dict],
) -> str:
    if weighted_score >= 80:
        base = "這間房子各項條件都不錯，"
    elif weighted_score >= 60:
        base = "這間房子條件還不錯，"
    elif weighted_score >= 40:
        base = "這間房子有一些需要注意的地方，"
    else:
        base = "這間房子條件較一般，"

    if '合理' in price_assessment:
        return base + "價格也在合理範圍內，可以考慮看房。"
    elif '可考慮購買' in price_assessment:
        return base + "價格合理偏低，非常推薦購買。"
    elif '建議議價' in price_assessment or '略高' in price_assessment:
        return base + "建議與賣家商議價格後再決定。"
    else:
        return base + "建議尋找其他選項或進一步議價。"
