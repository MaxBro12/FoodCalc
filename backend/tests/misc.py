data = {
    'products': [
        {
            'id': 1000000000000,
            'name': 'Тест Протеиновый Батончик',
            'description': 'Тестовое описание Протеинового Батончика',
            'calories': 200,
            'energy': 100,
            'added_by': 1,
            'minerals': [
                {
                    'product_id': 1000000000000,
                    'mineral_id': 1,
                    'content': 100,
                },
                {
                    'product_id': 1000000000000,
                    'mineral_id': 2,
                    'content': 50,
                },
                {
                    'product_id': 1000000000000,
                    'mineral_id': 3,
                    'content': 10,
                },
            ],
        },
        {
            'id': 1000000000001,
            'name': 'Тест Боночка с Яблочныйм Вареньем',
            'description': 'Тестовое описание яблочного варенья',
            'calories': 100,
            'energy': 50,
            'added_by': 1,
            'minerals': [
                {
                    'product_id': 1000000000001,
                    'mineral_id': 1,
                    'content': 100,
                },
                {
                    'product_id': 1000000000001,
                    'mineral_id': 2,
                    'content': 50,
                },
                {
                    'product_id': 1000000000001,
                    'mineral_id': 3,
                    'content': 10,
                },
                {
                    'product_id': 1000000000001,
                    'mineral_id': 10,
                    'content': 20,
                },
            ],
        },
        {
            'id': 1000000000002,
            'name': 'Тест Самый свежий Хлеб',
            'description': 'Тестовое описание очень свежего хлеба',
            'calories': 100,
            'energy': 50,
            'added_by': 1,
            'minerals': [
                {
                    'product_id': 1000000000002,
                    'mineral_id': 1,
                    'content': 10,
                },
                {
                    'product_id': 1000000000002,
                    'mineral_id': 2,
                    'content': 100,
                },
                {
                    'product_id': 1000000000002,
                    'mineral_id': 3,
                    'content': 50,
                },
                {
                    'product_id': 1000000000002,
                    'mineral_id': 15,
                    'content': 100,
                },
                {
                    'product_id': 1000000000002,
                    'mineral_id': 30,
                    'content': 10,
                },
            ],
        },
        {
            'id': 1000000000003,
            'name': 'Тест Масло',
            'description': 'Тестовое описание очень жирного масла',
            'calories': 600,
            'energy': 100,
            'added_by': 1,
            'minerals': [
                {
                    'product_id': 1000000000003,
                    'mineral_id': 1,
                    'content': 10,
                },
                {
                    'product_id': 1000000000003,
                    'mineral_id': 2,
                    'content': 1000,
                },
                {
                    'product_id': 1000000000003,
                    'mineral_id': 3,
                    'content': 50,
                },
                {
                    'product_id': 1000000000003,
                    'mineral_id': 16,
                    'content': 10,
                },
            ],
        },
        {
            'id': 1000000000004,
            'name': 'Тест Овсянка',
            'description': 'Тестовое описание овсянка она везде овсянка',
            'calories': 1000,
            'energy': 500,
            'added_by': 1,
            'minerals': [
                {
                    'product_id': 1000000000004,
                    'mineral_id': 1,
                    'content': 5,
                },
                {
                    'product_id': 1000000000004,
                    'mineral_id': 2,
                    'content': 50,
                },
                {
                    'product_id': 1000000000004,
                    'mineral_id': 3,
                    'content': 300,
                },
                {
                    'product_id': 1000000000004,
                    'mineral_id': 28,
                    'content': 300,
                },
                {
                    'product_id': 1000000000004,
                    'mineral_id': 17,
                    'content': 300,
                },
            ],
        }
    ]
}

import json

with open('data/products.json', 'w') as f:
    json.dump(data, f)
