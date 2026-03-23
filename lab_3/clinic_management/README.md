# Clinic Management API

Система управління медичною клінікою — Лабораторна робота №3.

**Стек:** Python 3.10+, FastAPI, SQLAlchemy 2.0 (async), PostgreSQL, asyncpg, Alembic, Pydantic v2, Uvicorn.

## Що нового у 3 лабораторній:
- Перехід від In-Memory до реляційної БД (**PostgreSQL**).
- Асинхронна робота з БД через **SQLAlchemy 2.0 + asyncpg**.
- Міграції бази даних через **Alembic**.
- Уніфікована обробка помилок бази даних (наприклад, `IntegrityError` для унікальних полів).

## Вимоги
- Python 3.10+
- Docker та Docker Compose (для локальної бази даних)

## Запуск

1. **Запуск бази даних (PostgreSQL):**
   ```bash
   docker-compose up -d
   ```

2. **Встановлення залежностей:**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Застосування міграцій бази даних:**
   Перед першим запуском додатку потрібно створити таблиці в БД:

   ```bash
   alembic revision --autogenerate -m "initial"
   ```

   Далі оновлюємо БД:
    ```bash
   alembic upgrade head
   ```

4. **Запуск додатку:**
   ```bash
   uvicorn app.main:app --reload
   ```

Swagger UI буде доступний за посиланням: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Структура проекту

```
clinic_management/
├── alembic/                 # Налаштування та версії міграцій Alembic
├── app/
│   ├── main.py              # FastAPI app, lifespan
│   ├── core/                # config, exceptions, database engine, error_handlers
│   ├── api/                 # routes, dependencies
│   ├── models/              # SQLAlchemy ORM моделі
│   ├── schemas/             # Pydantic моделі (DTO)
│   ├── repositories/        # SQLAlchemy асинхронні репозиторії
│   └── services/            # Бізнес логіка
├── test_api.py              # E2E скрипт для тестування усіх CRUD операцій
├── alembic.ini              # Конфігурація Alembic
├── docker-compose.yml       # Конфіг для підняття PostgreSQL
├── .env                     # Змінні середовища (DATABASE_URL та ін.)
└── requirements.txt         # Залежності
```

## Тестування

Для перевірки всіх CRUD операцій, коректності статус-кодів (200, 201, 204, 404, 409, 422) та ідемпотентності запустіть скрипт:
```bash
python test_api.py
```
