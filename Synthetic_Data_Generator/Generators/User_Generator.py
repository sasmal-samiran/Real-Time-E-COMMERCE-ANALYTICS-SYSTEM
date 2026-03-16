import random

user_pool = []
current_user_id = 0

def get_user():
    global current_user_id
    if len(user_pool) == 0 or random.random() < 0.2:
        current_user_id += 1
        user_id = f"user_{current_user_id}"
        user_pool.append(user_id)
        return user_id
    return random.choice(user_pool)