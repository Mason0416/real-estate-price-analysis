from typing import List, Dict, Tuple
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

def calculate_facility_distance_mock(lat: float, lon: float, facility_type: str) -> Tuple[float, str]:
    distances = {
        'mrt': (450, '便利'),
        'hospital': (650, '便利'),
        'school': (300, '非常便利'),
        'park': (500, '便利'),
    }
    return distances.get(facility_type, (1000, '普通'))

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

    query = db.query(TransactionRecord).filter(
        TransactionRecord.building_type == building_type,
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

    if asking_unit_price < reasonable_range['min']:
        return '價格偏低，可考慮購買'
    elif asking_unit_price <= reasonable_range['max']:
        return '價格合理'
    elif asking_unit_price <= reasonable_range['max'] * 1.1:
        return '略高，建議議價'
    else:
        return '明顯偏高，不建議直接購買'

def calculate_facility_scores(nearby_facilities: Dict[str, Tuple[float, str]]) -> Dict[str, float]:
    scores = {}

    for facility, (distance, rating) in nearby_facilities.items():
        if distance < 300:
            scores[facility] = 100
        elif distance < 800:
            scores[facility] = 85
        elif distance < 1500:
            scores[facility] = 70
        else:
            scores[facility] = 50

    return scores

def calculate_property_scores(age: int, floor: int, total_floors: int, parking: str) -> Dict[str, float]:
    age_score = max(50, 100 - (age / 50) * 100)
    floor_score = 100 if 3 <= floor <= total_floors - 2 else 75
    parking_score = 100 if parking == 'yes' else 60

    return {
        'age': age_score,
        'floor': floor_score,
        'parking': parking_score,
    }

def calculate_price_score(asking_price: float, area: float, reasonable_range: Dict[str, float]) -> float:
    asking_unit_price = asking_price / area
    median_unit = (reasonable_range['min'] + reasonable_range['max']) / 2

    if asking_unit_price <= median_unit:
        return 100
    else:
        diff_percent = ((asking_unit_price - median_unit) / median_unit) * 100
        return max(0, 100 - diff_percent)

def calculate_weighted_score(
    price_score: float,
    facility_scores: Dict[str, float],
    property_scores: Dict[str, float],
    weights: Dict[str, float],
) -> float:
    total_weight = sum(weights.values())

    if total_weight == 0:
        total_weight = 1

    normalized_weights = {k: v / total_weight for k, v in weights.items()}

    total_score = (
        price_score * normalized_weights.get('price', 1/9) +
        facility_scores.get('mrt', 75) * normalized_weights.get('mrt', 1/9) +
        facility_scores.get('hospital', 75) * normalized_weights.get('hospital', 1/9) +
        facility_scores.get('school', 75) * normalized_weights.get('school', 1/9) +
        facility_scores.get('park', 75) * normalized_weights.get('park', 1/9) +
        property_scores.get('age', 75) * normalized_weights.get('age', 1/9) +
        property_scores.get('floor', 75) * normalized_weights.get('floor', 1/9) +
        property_scores.get('parking', 75) * normalized_weights.get('parking', 1/9)
    )

    return round(total_score, 1)

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

    if '偏低' in price_assessment:
        return base + "價格也很合理，值得認真考慮。"
    elif '合理' in price_assessment:
        return base + "價格也在合理範圍內，可以考慮看房。"
    elif '略高' in price_assessment:
        return base + "建議與賣家商議價格後再決定。"
    else:
        return base + "建議尋找其他選項或進一步議價。"
