import pytest

from app.database import DB


async def test_product_new(test_client, test_db):
    ans = await test_client.post('/v1/products/new', json={
        'id': 1234567890123,
        'name': 'Test Product',
        'description': 'Test Product Description',
        'minerals': [
            {
                'id': 1,
                'content': 100
            },
            {
                'id': 2,
                'content': 50
            },
            {
                'id': 3,
                'content': 25
            }
        ],
        'calories': 100,
        'energy': 100
    })

    assert ans.status_code == 200
    assert ans.json().get('ok') == True

    test_min = await DB.products.by_name('Test Product', session=test_db)
    assert test_min is not None
    assert test_min.id == 1234567890123
    assert test_min.description == 'Test Product Description'
    assert test_min.calories == 100
    assert test_min.energy == 100


async def test_product_pagination(test_client):
    ans = await test_client.get('/v1/products/', params={
        'skip': 0,
        'limit': 1
    })
    assert ans.status_code == 200
    assert len(ans.json().get('products')) == 1
    assert ans.json().get('products')[0].get('id') == 1234567890123
    assert ans.json().get('products')[0].get('name') == 'Test Product'
    assert ans.json().get('products')[0].get('description') == 'Test Product Description'
    assert ans.json().get('products')[0].get('calories') == 100
    assert ans.json().get('products')[0].get('energy') == 100
    assert ans.json().get('products')[0].get('added_by_id') == 1


async def test_product_by_id(test_client):
    ans = await test_client.get(f'/v1/products/{1234567890123}')
    assert ans.status_code == 200
    assert ans.json().get('id') == 1234567890123
    assert ans.json().get('name') == 'Test Product'
    assert ans.json().get('description') == 'Test Product Description'
    assert ans.json().get('calories') == 100
    assert ans.json().get('energy') == 100
    assert ans.json().get('added_by_id') == 1


async def test_product_by_id_wrong(test_client):
    ans = await test_client.get(f'/v1/products/{1234567890123123}')
    assert ans.status_code == 404
    assert ans.json().get('detail') == 'Продукт с данным кодом не найден'


async def test_product_search(test_client):
    ans = await test_client.post(f'/v1/products/search', json={
        'id_or_name': 'Test Product',
    })
    assert ans.json().get('id') == 1234567890123
    assert ans.json().get('name') == 'Test Product'
    assert ans.json().get('description') == 'Test Product Description'
    assert ans.json().get('calories') == 100
    assert ans.json().get('energy') == 100
    assert ans.json().get('added_by_id') == 1


async def test_product_search_wrong(test_client):
    ans = await test_client.post(f'/v1/products/search', json={
        'id_or_name': 'Wrong Product',
    })
    assert ans.status_code == 404
    assert ans.json().get('detail') == 'Продукт по запросу Wrong Product не найден'


async def test_del_product(test_client):
    ans = await test_client.delete(f'/v1/products/{1234567890123}')
    assert ans.status_code == 200
    assert ans.json().get('ok') == True


async def test_del_product_wrong(test_client):
    ans = await test_client.delete(f'/v1/products/{1234567890123123}')
    assert ans.status_code == 200
    assert ans.json().get('ok') == False
