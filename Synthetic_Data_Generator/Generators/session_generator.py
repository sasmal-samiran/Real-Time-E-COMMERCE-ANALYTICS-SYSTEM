import random
from datetime import datetime,timedelta
# from Generators.User_Generator import user_profiles,generate_ip_for_country
# from Generators.product_details import products,product_price
from Synthetic_Data_Generator.Generators.User_Generator import user_profiles, generate_ip_for_country
from Synthetic_Data_Generator.Generators.product_details import products, product_price
# from User_Generator import user_profiles
TRANSITIONS = {
    "home": {
        "search":0.30,
        "category":0.25,
        "product":0.20,
        "deals":0.10,
        "login":0.05,
        "signup":0.05,
        "wishlist":0.03,
        "account":0.02
    },
    "search": {
        "product":0.45,
        "category":0.20,
        "search":0.15,
        "filters":0.10,
        "home":0.10
    },
    "category": {
        "product":0.65,
        # "subcategory":0.15,
        "search":0.15,
        "filters":0.10,
        "home":0.1
    },
    "product": {
        "product":0.35,
        "cart":0.15,
        "wishlist":0.10,
        "reviews":0.10,
        "compare":0.10,
        "search":0.10,
        "category":0.05,
        "home":0.05
    },
    "cart": {
        "checkout":0.40,
        "product":0.20,
        "home":0.15,
        "search":0.10,
        "wishlist":0.10,
        "coupon":0.05
    },
    "checkout": {
        "payment":0.70,
        "cart":0.15,
        "address":0.10,
        "login":0.05
    },
    "payment": {
        "order_confirmation":0.85,
        "payment_failure":0.15
    },
    "payment_failure": {
        "payment":0.50,
        "cart":0.30,
        "home":0.20
    },
    "order_confirmation": {
        "home":0.50,
        "account":0.30,
        "order_tracking":0.20
    },
    "account": {
        "order_tracking":0.30,
        "wishlist":0.20,
        "address":0.20,
        "home":0.20,
        "logout":0.10
    },
    "logout": {
        "home":1.0
    }
}
EVENT_TYPES = {
    "home":"page_view",
    "search":"search",
    "category":"browse_category",
    # "subcategory":"browse_category",
    "filters":"apply_filter",
    "product":"view_product",
    "reviews":"view_reviews",
    "compare":"compare_products",
    "seller_profile":"view_seller",
    "wishlist":"add_to_wishlist",
    "cart":"add_to_cart",
    "coupon":"apply_coupon",
    "checkout":"start_checkout",
    "address":"enter_address",
    "payment":"payment_attempt",
    "payment_failure":"payment_failed",
    "order_confirmation":"purchase_complete",
    "order_tracking":"track_order",
    "account":"account_view",
    "login":"login",
    "signup":"signup",
    "logout":"logout"
}
# event_id_dict = {
#     "page_view":f"E{str(1).zfill(5)}"
# }
event_id_dict = {
    v: f"E{str(i).zfill(5)}"
    for i, v in enumerate(EVENT_TYPES.values(),start=1)
}
# products = [f"P{i}" for i in range(1000,1200)] PRODUCT_CATALOG


device_types = ["mobile", "desktop", "tablet"]
weights_of_device_types = [0.65,0.3,0.05]
browsers = { 
    "mobile": ["chrome_mobile", "Brave_mobile"], 
    "desktop": ["chrome", "firefox", "edge"], 
    "tablet": ["chrome", "safari"] 
}
countries = ["India", "Russia", "China"]
weights_of_countries = [0.7,0.2,0.1]

locations = {
    "India": [
        "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata",
        "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
        "Surat", "Kanpur", "Nagpur", "Visakhapatnam", "Indore",
        "Thane", "Bhopal", "Patna", "Vadodara", "Coimbatore",
        "Agra", "Madurai", "Nashik", "Varanasi", "Meerut",
        "Rajkot", "Amritsar", "Aurangabad", "Jodhpur", "Ranchi",
        "Guwahati", "Chandigarh", "Kochi", "Mysuru", "Srinagar"],
    "Russia": ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg","Kazan", "Nizhny Novgorod", "Chelyabinsk", "Samara","Omsk", "Vladivostok"],
    "China": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu"]
}
traffic_sources = ["organic", "ads", "email", "social"]
weights_of_traffic_sources = [0.6,0.15,0.05,0.2]
def generate_page_url(page,product_id = None, category = None):
    if page == "product" and product_id:
        return f"/product/{product_id}"
    if page == "category" and category:
        return f"/category/{category}"
    if page == "search": 
        return "/search"
    return f"/{page}"
EXIT_PROBABILITY = 0.10
MIN_STEPS = 6
MAX_STEPS = 20

def next_page(current_page='home'):
    possible_transactions = TRANSITIONS.get(current_page)
    if possible_transactions is None:
        return "home"
    pages = list(possible_transactions.keys())
    weights = list(possible_transactions.values())
    return random.choices(pages,weights=weights,k=1)[0]

def generate_sessions(user_id):
    session_id = f"S{random.randint(100000,999999)}"
    current_page = "home"
    timestamp = datetime.now()
    session_events = []
    current_category = None
    cart_value = 0
    device = random.choices(device_types,weights=weights_of_device_types,k=1)[0]
    browser = random.choice(browsers[device])
    country = random.choices(countries,weights=weights_of_countries,k=1)[0]
    traffic = random.choices(traffic_sources,weights=weights_of_traffic_sources,k=1)[0]
    referrer = None
    steps = random.randint(MIN_STEPS,MAX_STEPS)
    # ── Pick ONE IP for the entire session (before the loop) ──────
    ip_data       = user_profiles[user_id]['IPs']
    primary_ip    = ip_data['Primary_IP']
    secondary_ips = ip_data['seconday_ips']     

    PRIMARY_WEIGHT   = 0.85
    RANDOM_TAIL      = 0.05
    secondary_budget = 1.0 - PRIMARY_WEIGHT - RANDOM_TAIL  

    pool    = [primary_ip]
    weights = [PRIMARY_WEIGHT]

    if secondary_ips:
        per_secondary = secondary_budget / len(secondary_ips)
        for ip in secondary_ips:
            pool.append(ip)
            weights.append(per_secondary)
    else:
        RANDOM_TAIL += secondary_budget   

    pool.append("__random__")
    weights.append(RANDOM_TAIL)

    chosen_ip = random.choices(pool, weights=weights, k=1)[0]
    if chosen_ip == "__random__":
        session_ip = generate_ip_for_country(country)  
    else:
        session_ip = chosen_ip
    for _ in range(steps):
        product_id = None
        price = None
        quantity = None
        is_purchase = False
        if current_page == "category":
            current_category = random.choice(list(products.keys()))

        if current_page == 'product':
            if current_category is None:
                current_category = random.choice(list(products.keys()))
            product_id = random.choice(products[current_category])
            price = product_price.get(product_id)

        '''-----------Cart Option----------'''
        if current_page == "cart" and product_id:
            quantity = random.randint(1,3)
            price = product_price.get(product_id)
            cart_value += price*quantity 

        if current_page == "order_confirmation": 
            is_purchase = True
            user_profiles[user_id]['total_orders'] += 1
        page_url = generate_page_url(current_page, product_id, current_category)
        event = {
            "timestamp":timestamp.isoformat(),
            "user_id":user_id,
            "session_id":session_id,
            "event_id":event_id_dict.get(EVENT_TYPES.get(current_page,"page_view")),
            "page":current_page,
            "event_type":EVENT_TYPES.get(current_page,"page_view"),
            "product_id":product_id,
            "category":current_category,
            "price":price,
            "quantity":quantity,
            "device_type": device, 
            "browser": browser, 
            "country": country, 
            "location":random.choice(locations[country]),
            "traffic_source": traffic,
            "page_url": page_url,
            "referrer_url": referrer,
            "time_on_page": random.uniform(5,60),
            "cart_value":cart_value if cart_value > 0 else None,
            "is_purchase":is_purchase,
            "ip_address":session_ip
        }
        session_events.append(event)
        referrer = page_url
        if random.random()<EXIT_PROBABILITY:
            break
        current_page = next_page(current_page)
        timestamp += timedelta(seconds=random.randint(5,45))
    return session_events