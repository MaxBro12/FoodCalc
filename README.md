# Foodapp

Это приложение для отслеживания калорий, полезных веществ в еде.

## Запуск

### Docker

```zsh
docker-compose up
```

### Ручной

#### Frontend

```zsh
cd frontend
npm run build
...
```

#### Backend

```zsh
cd backend
uv pip sync
uvicorn app.__main__:app --host 0.0.0.0 --port 8001 --workers 2
```

При ошибке `Failed to canonicalize script path`:

```zsh
python -m uvicorn app.__main__:app --host 0.0.0.0 --port 8001 --workers 2
```

## Backend

### DB

#### Keys

|name|type|desc|
|----|----|----|
|id|INT PRYMARY KEY| - |
|hash|VARCHAR UNIQUE| - |
|is_admin|BOOLEAN| - |

#### Users

|name|type|desc|
|----|----|----|
|id|INT PRYMARY KEY|-|
|name|VARCHAR UNIQUE|-|
|password|VARCHAR|save only hashed|
|is_admin|BOOLEAN|-|
|last_active|DATETIME|-|

#### Minerals

Minerals & Vitamins & Energy in 1 table

|name|type|desc|
|----|----|----|
|id|INT PRYMARY KEY|-|
|name|VARCHAR|-|
|description|TEXT|-|
|intake|FLOAT|in milligrams per day|
|type|INT FOREIGN KEY MineralTypes.id|

#### Minerals Types

Подробная информация о типе минерала.

|name|type|desc|
|----|----|----|
|id|INT PRYMARY KEY|-|
|name|VARCHAR|-|
|description|TEXT|-|

#### Products

|name|type|desc|
|----|----|----|
|id|INT PRYMARY KEY|-|
|name|VARCHAR|-|
|description|TEXT|-|
|added_by|INT FOREIGN KEY Users.id|-|

#### Products - Minerals & Vitamins

|name|type|desc|
|----|----|----|
|product_id|INT PRYMARY KEY FOREIGN KEY Products.id|-|
|mineral_id|INT PRYMARY KEY FOREIGN KEY Minerals.id|-|
|content|FLOAT|in milligrams per 100 gram|

#### Dish

|name|type|desc|
|----|----|----|
|dish_id|INT PRYMARY KEY|-|
|added_by|INT FOREIGN KEY Users.id|-|
||||
