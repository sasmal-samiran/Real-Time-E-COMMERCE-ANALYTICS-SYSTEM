import random
from datetime import datetime,timedelta

user_pool = []
user_profiles = {}
current_user_id = 0

countries = ["India","Russia","Chin","Germany","Canada"]
weights_of_countries = [0.75,0.1,0.025,0.05,0.025]
genders = ["male","female"]
membership_types = ["normal","prime"]
weights_of_membership = [0.7,0.3]

def get_user():
    global current_user_id
    if len(user_pool) == 0 or random.random() < 0.2:
        current_user_id += 1
        user_id = f"user_{str(current_user_id).zfill(5)}"
        user_pool.append(user_id)
        user_profiles[user_id] = {
            "user_id":user_id,
            "age":random.randint(18,60),
            "gender":random.choice(genders),
            "country":random.choices(countries,weights=weights_of_countries,k=1)[0],
            "signup_date":datetime.now() - timedelta(days=random.randint(1,1000)),
            "membership_type":random.choices(membership_types,weights=weights_of_membership,k=1)[0],
            "total_orders":0
        }
        return user_id
    return random.choice(user_pool)

def get_user_details(user_id):
    return user_profiles[user_id]
    