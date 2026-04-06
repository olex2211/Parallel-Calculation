# Clinic Management System — Lab 5 (Redis Caching)

Повноцінна мікросервісна архітектура для управління клінікою. Система побудована з використанням **FastAPI**, **PostgreSQL**, **Redis**, **Docker** та **Nginx**.

Ця (П'ята) лабораторна робота є логічним продовженням розробки мікросервісної архітектури, до якої додано **швидкісний in-memory кеш на базі Redis** для оптимізації найчастіших GET-запитів.

---

## Архітектура системи

Система декомпозована на незалежні мікросервіси. Кожен має власну ізольовану базу даних (`Database-per-service pattern`) та спілкується з іншими через HTTP.

- **Patient Service** — Управління даними пацієнтів та лікарів.
- **Appointment Service** — Планування візитів до лікарів. (Взаємодіє з Patient Service).
- **Treatment Service** — Облік аналізів, діагнозів та планів лікування.
- **Billing Service** — Розрахунок вартості послуг та керування платежами.
- **API Gateway (Nginx)** — Єдина точка входу (`Reverse Proxy`) для зручного доступу клієнтів.
- **Redis Cache** — Глобальне in-memory сховище ключ-значення, яке розділене на дві бази (`0` для Patient, `1` для Appointment).

---

##  Нове у Лабораторній №5: Redis Кешування

Redis-контейнер (`redis:7-alpine`), що забезпечив кардинальне прискорення роботи найчастіших запитів, знявши навантаження з СУБД PostgreSQL.

### Як працює кешування?
- **@cache decorator:** API-ендпоінти огорнуті у декоратори (бібліотека `fastapi-cache2`), які перехоплюють відповіді і зберігають їх у Redis на 5 хвилин (`CACHE_TTL = 300`).
- **Data Invalidation (Інвалідація):** Щоб не віддавати застарілі ("stale") дані, будь-які мутації (створення, оновлення, видалення) викликають ручну або автоматичну інвалідацію конкретного ключа у Redis за ідентифікатором (`id`).

### Які ендпоінти кешуються?
1. `GET /api/doctors/{id}`
2. `GET /api/patients/{id}`
3. `GET /api/visits/{id}`

> **Перевірка швидкодії:** 
> Звичайний запит у базу може тривати секунду (або ми можемо зімітувати навантаження через `asyncio.sleep`). 
> З кешем Redis час виконання падає до **~0.015s**, адже відповідь віддається оперативно з оперативної пам'яті.

---

##  Технологічний стек

- **Backend:** Python + FastAPI, SQLAlchemy (просунутий ORM), Alembic (міграції), Pydantic
- **Databases:** PostgreSQL (Relational), Redis (In-memory Cache)
- **Infrastructure:** Docker, Docker Compose, Nginx, Linux (Alpine)
- **Communication:** HTTP Clients (`httpx`), RESTful API design.

---

##  Швидкий старт

1. Переконайтеся, що у вас встановлені **Docker** та **Docker Compose**.
2. Відкрийте термінал у папці `clinic_management` (там де лежить `docker-compose.yml`).
3. Виконайте команду збирання та запуску інфраструктури:

```bash
docker-compose up -d --build
```

4. Після успішного запуску вся система буде доступна за адресою `http://localhost/`

---

## 📖 Документація API (Swagger UI)

Завдяки Nginx API-роутингу, кожен сервіс має власну інтерактивну OpenAPI документацію:

- 🧑‍⚕️ **Patient API:** [http://localhost/docs/patients/](http://localhost/docs/patients/)
- 📅 **Appointment API:** [http://localhost/docs/appointments/](http://localhost/docs/appointments/)
- 💊 **Treatment API:** [http://localhost/docs/treatments/](http://localhost/docs/treatments/)
- 💳 **Billing API:** [http://localhost/docs/billing/](http://localhost/docs/billing/)

Також є окремі System/Healthcheck ендпоінти, наприклад `http://localhost/patients/health`, які показують "живість" бази даних та, відтепер, підключення до Redis (`"cache": "ok"`).
