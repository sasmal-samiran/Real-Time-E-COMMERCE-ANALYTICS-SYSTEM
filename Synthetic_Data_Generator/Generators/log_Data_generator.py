import json
import random
from datetime import datetime
 
# from Generators.User_Generator import get_user, user_profiles
# from Generators.product_details import products, BRANDS, product_price,products_details
# from Generators.session_generator import generate_sessions
from Synthetic_Data_Generator.Generators.User_Generator import get_user, user_profiles
from Synthetic_Data_Generator.Generators.product_details import products, BRANDS, product_price,products_details
from Synthetic_Data_Generator.Generators.session_generator import generate_sessions

OS_MAP = {
    "mobile":  ["Android", "iOS"],
    "desktop": ["Windows", "macOS", "Linux"],
    "tablet":  ["Android", "iPadOS"],
}


def _status(event_type: str, page: str) -> str:
    """Derive a realistic status string from the event type."""
    if page == "payment_failure":
        return "failed"
    if event_type in ("purchase_complete", "login", "signup", "apply_coupon"):
        return random.choices(["success", "failed"], weights=[0.95, 0.05])[0]
    return "success"

def format_log(event: dict) -> dict:
    """
    Transform one flat session event dict → nested log dict matching the
    target schema:
      timestamp, event_type, user{}, session{}, product{}, location{}, action_details{}, status
    """
    user_id    = event["user_id"]
    profile    = user_profiles[user_id]
    device     = event["device_type"]
    product_id = event.get("product_id")
    # category   = event.get("category")
    is_logged_in = event["event_type"] not in ("login", "signup", "page_view")


    user_block = {
        "user_id":        user_id,
        "age":            profile["age"],
        "gender":         profile["gender"],
        "membership":     profile["membership_type"],
        "is_logged_in":   is_logged_in,
        "signup_date":    profile["signup_date"].strftime("%Y-%m-%d"),
        "total_orders":   profile["total_orders"],
    }

    session_block = {
        "session_id":      event["session_id"],
        "device":          device,
        "browser":         event["browser"],
        "os":              random.choice(OS_MAP.get(device, ["Unknown"])),
        "traffic_source":  event["traffic_source"],
        "page":            event["page"],
        "page_url":        event["page_url"],
        "referrer_url":    event.get("referrer_url"),
        "time_on_page_sec": round(event["time_on_page"], 1),
    }

    if product_id:
        product_block = {
            "product_id": product_id,
            "category":   products_details[product_id]['category'],
            "brand":      products_details[product_id]['brand'],
            "price":      products_details[product_id]['price']
        }
    else:
        product_block = None
    location_block = {
        "ip_address": event["ip_address"],
        "city":       event["location"],
        "country":    event["country"],
    }
    action_block = {
        "quantity":   event.get("quantity"),
        "cart_value": event.get("cart_value"),
        "is_purchase": event.get("is_purchase", False),
        "coupon_applied": event["event_type"] == "apply_coupon",
    }
    action_block = {k: v for k, v in action_block.items() if v is not None}

    log = {
        "timestamp":      event["timestamp"],
        "event_id":       event["event_id"],
        "event_type":     event["event_type"],
        "user":           user_block,
        "session":        session_block,
        "product":        product_block,
        "location":       location_block,
        "action_details": action_block,
        "status":         _status(event["event_type"], event["page"]),
    }
    return log

def generate_logs():
    pass