from random import randint
import json


new= []
with open('data/products.json') as f:
    data = json.load(f)
    for product in data['products']:
        new_product = {
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'calories_per_100g': product['calories'],
            'proteins_per_100g': randint(0, product['calories']),
            'fats_per_100g': randint(0, product['calories']),
            'carbs_per_100g': randint(0, product['calories']),
            'fiber_per_100g': randint(0, product['calories']),
            'sugar_per_100g': randint(0, product['calories']),
        }
        new.append(new_product)

with open('data/new_products.json', 'w') as f:
    json.dump({'products': new}, f)
