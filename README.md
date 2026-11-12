# Лабораторна робота №9 — контейнеризація Flask-застосунку (ЛР №8)

Застосунок: сесії в пам'яті, вхід/вихід, CSRF, `login_required`, SQLite (студенти/дисципліни/оцінки).
Структура: `app.py`, `auth.py`, `init_db.py`, `templates/` (`login.html`, `_auth_nav.html`), `Dockerfile`, `requirements.txt`.

## Конфігурація (змінні оточення)
- `PORT` — порт процесу в контейнері (за замовчуванням 5000);
- `DATA_DIR` — каталог даних; БД: `$DATA_DIR/app.sqlite3`.
Приклад — `.env.example`. Секретів в образі немає: сесії серверні, випадкові id генеруються при роботі.
Тестові облікові записи (admin / teacher1 / викладач) створюються лише в порожній БД, паролі змініть для реального використання.

## Збирання
    docker build -f Dockerfile -t flask-app:lab9 .

## Запуск 1: порт за замовчуванням (5000:5000)
    docker run -d --name flask-default -p 127.0.0.1:5000:5000 flask-app:lab9
    docker ps -a && docker logs flask-default && docker port flask-default
    curl -i http://127.0.0.1:5000/
    docker stop flask-default && docker rm flask-default

## Запуск 2: PORT=8080, відображення 5001:8080, монтування даних
    mkdir -p data
    docker run -d --name flask-data \
      -e PORT=8080 -e DATA_DIR=/app/data \
      -p 127.0.0.1:5001:8080 -v "${PWD}/data:/app/data" flask-app:lab9
    docker logs flask-data && docker port flask-data
Відкрити http://127.0.0.1:5001, увійти (admin / ChangeMe#3), змінити оцінку.
SELinux: `-v "${PWD}/data:/app/data:Z"`.

## Ініціалізація SQLite
Автоматична при старті, недеструктивна (`CREATE TABLE IF NOT EXISTS`, навчальні дані — лише в порожню БД).
Вручну: `docker exec flask-data python init_db.py`.
Щоб використати власну БД з ЛР №8 — покласти її копію в `data/app.sqlite3` до запуску (застосунок зупинено).

## Перевірка збереження
    ls -l data
    docker exec flask-data ls -l /app/data
    docker inspect flask-data            # розділ Mounts
    docker stop flask-data && docker rm flask-data
    docker run -d --name flask-restored \
      -e PORT=8080 -e DATA_DIR=/app/data \
      -p 127.0.0.1:5001:8080 -v "${PWD}/data:/app/data" flask-app:lab9
Оцінки збережені; потрібно увійти повторно, бо сесії зберігаються в пам'яті процесу (як в експерименті 7 ЛР №8).

## Podman
Замінити `docker` на `podman`; правила `.containerignore` = `.dockerignore`.

## Передача БД
Зупинити контейнер, `sqlite3 data/app.sqlite3 "PRAGMA wal_checkpoint(TRUNCATE);"`,
файл `app.sqlite3` подати окремо в Classroom (не в репозиторій).
