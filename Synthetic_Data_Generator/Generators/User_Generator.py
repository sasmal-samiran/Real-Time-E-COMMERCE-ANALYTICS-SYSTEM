import random
from datetime import datetime,timedelta

user_pool = []
user_profiles = {}
current_user_id = 0

countries = ["India", "Russia", "China"]
weights_of_countries = [0.7,0.2,0.1]
genders = ["male","female"]
membership_types = ["normal","prime"]
weights_of_membership = [0.7,0.3]


COUNTRY_IP_RANGES = {
    "India": [
        (0x01E00000, 0x01E0FFFF),   # 1.224.0.0  – Airtel
        (0x2D690000, 0x2D69FFFF),   # 45.105.0.0 – Jio
        (0x3E280000, 0x3E28FFFF),   # 62.40.0.0  – BSNL
        (0x71A00000, 0x71A0FFFF),   # 113.160.0.0– Vodafone IN
        (0x74780000, 0x7478FFFF),   # 116.120.0.0– ACT Fibernet
        (0x7B480000, 0x7B48FFFF),   # 123.72.0.0 – Hathway
        (0xC0A80000, 0xC0A8FFFF),   # 192.168.0.0– (fallback generic)
        (0xCB000000, 0xCB00FFFF),   # 203.0.0.0  – MTNL Mumbai
    ],
    "Russia": [
        (0x25000000, 0x2500FFFF),   # 37.0.0.0   – Rostelecom
        (0x3E800000, 0x3E80FFFF),   # 62.128.0.0 – MTS Russia
        (0x5F000000, 0x5F00FFFF),   # 95.0.0.0   – Beeline
        (0x59DC0000, 0x59DCFFFF),   # 89.220.0.0 – MegaFon
        (0xB9480000, 0xB948FFFF),   # 185.72.0.0 – TTK
    ],
    "China": [
        (0x01010000, 0x0101FFFF),   # 1.1.0.0    – ChinaNet
        (0x7B180000, 0x7B18FFFF),   # 123.24.0.0 – China Unicom
        (0x76400000, 0x7640FFFF),   # 118.64.0.0 – China Telecom
        (0x79480000, 0x7948FFFF),   # 121.72.0.0 – China Mobile
    ],
}
def _int_to_ip(n: int) -> str:
    return f"{(n >> 24) & 0xFF}.{(n >> 16) & 0xFF}.{(n >> 8) & 0xFF}.{n & 0xFF}"
def generate_ip_for_country(country: str) -> str:
    """Generate a random IP from a real ISP range for the given country."""
    ranges = COUNTRY_IP_RANGES.get(country, COUNTRY_IP_RANGES["India"])
    start, end = random.choice(ranges)
    return _int_to_ip(random.randint(start, end))


def get_user():
    global current_user_id
    if len(user_pool) == 0 or random.random() < 0.2:
        current_user_id += 1
        user_id = f"user_{str(current_user_id).zfill(5)}"
        user_pool.append(user_id)
        country = random.choices(countries,weights=weights_of_countries,k=1)[0]
        n_secondary = random.choices([0, 1, 2], weights=[0.10, 0.60, 0.30])[0]
        secondary_ips = [generate_ip_for_country(country) for _ in range(n_secondary)]
        user_profiles[user_id] = {
            "user_id":user_id,
            "age":random.randint(18,60),
            "gender":random.choice(genders),
            "country":country,
            "signup_date":datetime.now() - timedelta(days=random.randint(1,1000)),
            "membership_type":random.choices(membership_types,weights=weights_of_membership,k=1)[0],
            "total_orders":0,
            "IPs":{
                "Primary_IP":generate_ip_for_country(country=country),
                "seconday_ips":secondary_ips
            }
        }
        return user_id
    return random.choice(user_pool)

def get_user_details(user_id):
    return user_profiles[user_id]
    