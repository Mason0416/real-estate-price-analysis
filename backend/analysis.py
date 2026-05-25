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
        'school': (300, 80),
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
) -> List[Dict]:
    db = SessionLocal()

    area_min, area_max = area * 0.8, area * 1.2
    age_min, age_max = max(0, age - 5), age + 5

    type_mapping = {
        "電梯大樓": "building",
        "公寓": "apartment",
        "透天": "house"
    }
    mapped_type = type_mapping.get(building_type, building_type)

    query = db.query(TransactionRecord).filter(
        TransactionRecord.building_type.in_([building_type, mapped_type]),
        TransactionRecord.area.between(area_min, area_max),
        TransactionRecord.age.between(age_min, age_max),
    )

    cases = query.all()
    db.close()

    if not cases:
        return []

    similar = []
    for case in cases[:10]:
        distance = ((case.latitude - lat) ** 2 + (case.longitude - lon) ** 2) ** 0.5
        similar.append({
            'address': case.address,
            'price': case.price,
            'area': case.area,
            'age': case.age,
            'unit_price': round(case.price / case.area, 2),
            'transaction_date': case.transaction_date,
            'distance_km': round(distance * 111, 2),
        })

    similar.sort(key=lambda x: x['distance_km'])
    return similar[:5]

def calculate_reasonable_price(similar_cases: List[Dict]) -> Tuple[float, Dict[str, float]]:
    if not similar_cases:
        return None, None

    unit_prices = [case['unit_price'] for case in similar_cases]
    median_price = statistics.median(unit_prices)

    return median_price, {
        'min': round(median_price * 0.95, 2),
        'max': round(median_price * 1.05, 2),
    }

def assess_price(asking_price: float, area: float, reasonable_range: Dict[str, float]) -> str:
    asking_unit_price = asking_price / area
    median_unit = (reasonable_range['min'] + reasonable_range['max']) / 2
    ratio = asking_unit_price / median_unit

    if ratio < 0.95:
        return '可考慮購買'
    elif ratio <= 1.05:
        return '合理'
    elif ratio <= 1.10:
        return '略高'
    elif ratio <= 1.20:
        return '建議議價'
    else:
        return '明顯偏高'

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
    asking_unit_price = asking_price / area
    median_unit = (reasonable_range['min'] + reasonable_range['max']) / 2

    diff_percent = ((asking_unit_price - median_unit) / median_unit) * 100

    if diff_percent <= -10:
        return 100
    elif diff_percent <= 0:
        return 80
    elif diff_percent <= 10:
        return 60
    elif diff_percent <= 20:
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
