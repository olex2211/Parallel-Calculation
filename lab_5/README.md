# Clinic Management System — Lab 4

Мікросервісна архітектура для управління клінікою, реалізована за допомогою **FastAPI**, **PostgreSQL**, **Docker** та **Nginx**.

## Про проєкт

Ця лабораторна робота демонструє міграцію монолітного додатку на мікросервісну архітектуру. Система розділена на 4 незалежні сервіси, кожен з яких відповідає за свою бізнес-логіку та має власну базу даних.

## Архітектура

Система складається з наступних компонентів:

- **Patient Service** — Управління даними пацієнтів та лікарів.
- **Appointment Service** — Планування візитів до лікарів.
- **Treatment Service** — Облік аналізів, діагнозів та планів лікування.
- **Billing Service** — Розрахунок вартості послуг та керування платежами.
- **API Gateway (Nginx)** — Єдина точка входу (`routing`) для всіх сервісів.

## Технології

- **Backend:** Python + FastAPI, SQLAlchemy, Alembic, Pydantic
- **База даних:** PostgreSQL
- **Інфраструктура:** Docker, Docker Compose, Nginx
- **Міжсервісна взаємодія:** HTTP Clients

## Швидкий старт

1. Переконайтеся, що на вашому комп'ютері встановлено **Docker** та **Docker Compose**.
2. Відкрийте термінал у кореневій папці проєкту (там, де знаходиться `docker-compose.yml`).
3. Виконайте команду для збирання та запуску всіх контейнерів у фоновому режимі:

```bash
docker-compose up -d --build
```

4. Після успішного запуску API Gateway буде доступний за адресою: `http://localhost/`

## Документація API (Swagger UI)

Завдяки Nginx, кожен сервіс має власну інтерактивну документацію, доступну за єдиним хостом:

- 🧑‍⚕️ **Patient Service:** [http://localhost/docs/patients/](http://localhost/docs/patients/)
- 📅 **Appointment Service:** [http://localhost/docs/appointments/](http://localhost/docs/appointments/)
- 💊 **Treatment Service:** [http://localhost/docs/treatments/](http://localhost/docs/treatments/)
- 💳 **Billing Service:** [http://localhost/docs/billing/](http://localhost/docs/billing/)

---
*Лабораторна робота 4*
