# nanosemantica_task
simple aiohttp app

Реализован API для хранения информации о сотрудниках в БД (Postgresql) с использованием фреймворка aiohttp. 

CRUD - эндпоинты:
* POST: /create (необходимые данные - body: {"name": str, "age": int, "department": str}) - создание нового сотрудника.
* GET: /read/all - получение информации о всех имеющихся сотрудниках.
* GET: /read/read_by_name (необходимые данные - querystring: name=str) - поиск сотрудников по имени.
* GET: /read/read_by_age (необходимые данные - querystring: age=int) - поиск сотрудников по возрасту.
* GET: /read/read_by_department (необходимые данные - querystring: department=department) - поиск сотрудников по отделу.
* PUT: /update (необходимые данные - body: {"name": str, "age": int, "department": str, "new_name": str, "new_age": int, "new_department": str}) - обновление информации о сотруднике.
* DELETE: /delete (необходимые данные - body: {"name": str, "age": int, "department": str}) - удаление информации о сотруднике.

**Примечания:**
* Проект живет на localhost:8080.
* При первом запуске контейнера следует, в строчке 21 файла docker-compose.yaml установить 1 (то есть create_dummy_data=1). Это создаст тестовые записи в БД (dummy data). При последующих запусках следует 1 заменить на 0.
* Тесты запускаются командой pytest (из корня проекта). Директория с тестами - src/tests. (Для этого необходимо предварительно создать виртуальное окружение и установить зависимости).

**Руководство по запуску:**
* Склонировать данный репозиторий (команда: git clone https://github.com/fl1p3mth3b1rd/nanosemantica_task).
* Перейти в корень проекта.
* Собрать Docker-compose контейнеры (команда: docker-compose build).
* Запустить контейнеры (команда: docker-compose up).
