import random

products = {
    "electronics": [f"E{i}" for i in range(1000,1030)],
    "fashion": [f"F{i}" for i in range(2000,2030)],
    "books": [f"B{i}" for i in range(3000,3030)],
    "sports": [f"S{i}" for i in range(4000,4030)],
    "home": [f"H{i}" for i in range(5000,5030)]
}
BRANDS = {
    "electronics": ["Samsung","Apple","OnePlus","Xiaomi","boAt","Sony","LG","Realme","Lenovo","Noise"],
    "fashion": ["Fabindia","W for Woman","Manyavar","Peter England","Van Heusen","Biba","Raymond","Allen Solly","Aurelia","Jockey"],
    "books": ["Penguin India","Rupa Publications","Westland Books","Harper Collins India","Fingerprint Publishing","Notion Press","Jaico Publishing","Oxford India","Bloomsbury India","Scholastic India"],
    "sports": ["Nivia","Cosco","Vector X","SS Cricket","SG Cricket","Yonex","Adidas India","Nike India","Decathlon","OMTEX"],
    "home": ["Prestige","Bajaj Electricals","Havells","Milton","Cello","Godrej","Nilkamal","Asian Paints","Philips India","Pigeon"]
}
price_ranges = { 
    "electronics": (5000, 80000), 
    "fashion": (300, 5000), 
    "books": (150, 1200), 
    "sports": (500, 15000), 
    "home": (800, 25000) 
}
product_price = {}
for category,product_list in products.items():
    low, high = price_ranges[category]
    for product_id in product_list:
        price = random.randint(low,high)
        price = int(round(price/100)) * 100 - 1
        product_price[product_id] = price
DISCOUNT_RANGES = {
    "electronics": (5, 35),   
    "fashion":     (10, 80),  
    "books":       (10, 40),   
    "sports":      (10, 50),   
    "home":        (5, 60),    
}
def generate_discount(category: str) -> int:
    low, high = DISCOUNT_RANGES[category]
    return random.randint(low, high)


products_details = {}
for category in products.keys():
    for product_id in products[category]:
        data = {
            'product_id':product_id,
            'category':category,
            'brand':random.choice(BRANDS[category]),
            'price':product_price.get(product_id),
            'rating':round(random.uniform(2.5, 5.0), 1),
            'stock':random.randint(1000,10000),
            'discount':str(round(generate_discount(category),2))+'%'
        }
        products_details[product_id] = data

