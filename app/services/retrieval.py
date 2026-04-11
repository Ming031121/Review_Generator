import json

with open("app/data/restaurants_info.json","r") as f:
    restaurant_db = json.load(f)

def retrieve_context(restaurant_name: str):
    name = restaurant_name.lower()
    for r in restaurant_db:
        if r["restaurant_name"].lower() == name:
            return r
    return None

    
def format_context(r):
    return f"""
    Restaurant: {r['restaurant_name']}
    location:{r['location']}
    Cuisine: {', '.join(r['cuisine'])}

    Popular dishes:
    - {'; '.join(r['popular_dishes'])}

    Experience:
    - {'; '.join(r['experience'])}

    Common reviews:
    - {'; '.join(r['common_reviews'])}
    """.strip()