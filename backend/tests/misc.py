import json
from pprint import pprint

types = []
with open('data/types.json', 'r') as f:
    types = json.load(f)['data']

new_types = []
for type in types:
    if type['id'] == 1:
        new_types.append({
            'id': type['id'],
            'name': type['name'],
            'description': type['description'],
            'minerals': [
                {
                    'id': 1,
                    'name': 'Белок',
                    'compact_name': 'Б',
                    'description': '\u0421\u0442\u0440\u043e\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b \u0434\u043b\u044f \u043a\u043b\u0435\u0442\u043e\u043a, \u0442\u043a\u0430\u043d\u0435\u0439 (\u043c\u044b\u0448\u0446\u044b, \u043a\u043e\u0436\u0430, \u0432\u043e\u043b\u043e\u0441\u044b), \u0444\u0435\u0440\u043c\u0435\u043d\u0442\u043e\u0432, \u0433\u043e\u0440\u043c\u043e\u043d\u043e\u0432, \u0430\u043d\u0442\u0438\u0442\u0435\u043b. \u0412\u0442\u043e\u0440\u0438\u0447\u043d\u044b\u0439 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u044d\u043d\u0435\u0440\u0433\u0438\u0438.',
                    'intake': 4,
                },
                {
                    'id': 2,
                    'name': 'Жиры',
                    'compact_name': 'Ж',
                    'description': '\u0421\u0430\u043c\u044b\u0439 \u043a\u043e\u043d\u0446\u0435\u043d\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u044d\u043d\u0435\u0440\u0433\u0438\u0438, \u0441\u0442\u0440\u043e\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b \u0434\u043b\u044f \u043a\u043b\u0435\u0442\u043e\u0447\u043d\u044b\u0445 \u043c\u0435\u043c\u0431\u0440\u0430\u043d \u0438 \u0433\u043e\u0440\u043c\u043e\u043d\u043e\u0432, \u0441\u0440\u0435\u0434\u0430 \u0434\u043b\u044f \u0443\u0441\u0432\u043e\u0435\u043d\u0438\u044f \u0436\u0438\u0440\u043e\u0440\u0430\u0441\u0442\u0432\u043e\u0440\u0438\u043c\u044b\u0445 \u0432\u0438\u0442\u0430\u043c\u0438\u043d\u043e\u0432 (A, D, E, K), \u0437\u0430\u0449\u0438\u0442\u0430 \u043e\u0440\u0433\u0430\u043d\u043e\u0432, \u0442\u0435\u0440\u043c\u043e\u0440\u0435\u0433\u0443\u043b\u044f\u0446\u0438\u044f.',
                    'intake': 9,
                },
                {
                    'id': 3,
                    'name': 'Углеводы',
                    'compact_name': 'У',
                    'description': '\u0411\u044b\u0441\u0442\u0440\u044b\u0439 \u0438 \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u044d\u043d\u0435\u0440\u0433\u0438\u0438 \u0434\u043b\u044f \u0442\u0435\u043b\u0430, \u043e\u0441\u043e\u0431\u0435\u043d\u043d\u043e \u0434\u043b\u044f \u043c\u043e\u0437\u0433\u0430 \u0438 \u043c\u044b\u0448\u0446.',
                    'intake': 4,
                },
                {
                    'id': 4,
                    'name': 'Клетчатка',
                    'compact_name': 'ПВ',
                    'description': 'Клетчатка (Пищевые волокна) - это сложные углеводы растительного происхождения, которые не перевариваются в ЖКТ человека, но жизненно важны для пищеварения, контроля веса и профилактики многих заболеваний, так как очищают кишечник, питают полезную микрофлору, снижают уровень сахара и холестерина, а также регулируют стул.',
                    'intake': 30000,
                },
            ]
        })
        continue

    new_minerals = []
    for mineral in type['minerals']:
        new_minerals.append({
            'id': mineral['id']+1,
            'name': mineral['name'],
            'compact_name': mineral['compact_name'],
            'description': mineral['description'],
            'intake': mineral['intake'],
        })

    new_types.append({
        'id': type['id'],
        'name': type['name'],
        'description': type['description'],
        'minerals': new_minerals
    })


with open('data/test.json', 'w') as f:
    json.dump({'data': new_types}, f, indent=4)
