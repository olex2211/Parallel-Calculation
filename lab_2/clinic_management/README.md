# Clinic Management API

Система управління медичною клінікою — Лабораторна робота №2.

**Стек:** Python, FastAPI, Pydantic v2, Uvicorn. In-memory зберігання (без БД).

## Запуск

```bash
cd clinic_management
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Структура

```
clinic_management/
├── app/
│   ├── main.py              # FastAPI app + exception handlers
│   ├── core/                # config, exceptions
│   ├── api/                 # routes, dependencies, router
│   ├── models/              # domain models (plain Python classes)
│   ├── schemas/             # Pydantic schemas (Create/Update/Response)
│   ├── repositories/        # in-memory repositories (BaseRepository)
│   └── services/            # business logic
└── requirements.txt
```

## API Ендпоінти

| Метод  | URL                                    | Опис                         |
|--------|----------------------------------------|------------------------------|
| GET    | /api/v1/patients                       | Список пацієнтів             |
| POST   | /api/v1/patients                       | Створити пацієнта            |
| GET    | /api/v1/doctors                        | Список лікарів               |
| POST   | /api/v1/doctors                        | Створити лікаря              |
| POST   | /api/v1/visits                         | Створити візит               |
| PATCH  | /api/v1/visits/{id}/complete           | Завершити візит              |
| POST   | /api/v1/diagnoses                      | Додати діагноз               |
| POST   | /api/v1/prescriptions                  | Додати призначення           |
| POST   | /api/v1/payments                       | Створити платіж (авторозрах) |
| PATCH  | /api/v1/payments/{id}/pay              | Оплатити                     |
| GET    | /api/v1/treatment-history/{patient_id} | Історія лікування            |
