# Foodapp

Это приложение для отслеживания калорий, полезных веществ в еде. Приложение позволяет пользователям отслеживать калорийность и содержание полезных веществ в еде.

Приложение разделено на несколько микросервисов:

- frontend - фронтенд с использованием Vite React js
- backend - главный бэкенд
- blocker_service - сервис для блокировки пользователей
- auth_service - сервис для аутентификации пользователей

Так же приложение использует:
- redis - для кэширования результатов некоторых эндпойнтов
- postgres - для хранения данных, используется единая база данных для всех микросервисов, скрипт инициализации `init.sql`

Для упрощения работы с микросервисной архитектурой многие методы были вынесены в пакет core. Для работы backend, backend_service и auth_service требуется установить пакет core. Подробнее можно узнать в [README.md](https://github.com/MaxBro12/FoodCalc/blob/master/core/README.md)

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
```

#### Blocker Service

```zsh
cd blocker_service
uv pip sync
pip install -e ../core

uvicorn app.__main__:app --host 127.0.0.1 --port 8002 --workers 2
python app # поддерживается и такой запуск
```

При ошибке `Failed to canonicalize script path`:

```zsh
python -m uvicorn app.__main__:app --host 0.0.0.0 --port 8001 --workers 2
```

#### Auth Service

```zsh
cd auth_service
uv pip sync
pip install -e ../core

uvicorn app.__main__:app --host 127.0.0.1 --port 8003 --workers 2
python app # поддерживается и такой запуск
```

При ошибке `Failed to canonicalize script path`:

```zsh
python -m uvicorn app.__main__:app --host 0.0.0.0 --port 8001 --workers 2
```

#### Backend

```zsh
cd backend
uv pip sync
pip install -e ../core

uvicorn app.__main__:app --host 127.0.0.1 --port 8001 --workers 2
python app # поддерживается и такой запуск
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
