# Scored

## Описание проекта

Scored — это веб-приложение для управления успеваемостью студентов. Преподаватели могут добавлять и редактировать информацию о студентах, учебных планах и оценках, а студенты могут просматривать свои результаты.

## Установка

Для установки и запуска проекта выполните следующие шаги:

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Silen/Scored.git
    ```

2. Перейдите в директорию проекта:
    ```bash
    cd Scored
    ```

3. Создайте виртуальное окружение и активируйте его:
    ```bash
    python -m venv venv
    source venv/bin/activate   # Для Windows используйте `venv\Scripts\activate`
    ```

4. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

5. Сбросьте и заполните базу данных:
    ```bash
    python reset_db.py
    python seed_db.py
    ```

6. Запустите приложение:
    ```bash
    python run.py
    ```

Приложение будет доступно по адресу `http://127.0.0.1:5000/`.

## Схемы

### Use Case Diagram

![Use Case Diagram](app/static/images/ucd.png)

### Data Flow Diagram (DFD)

![Data Flow Diagram](app/static/images/dfd.png)

### Entity Relationship Diagram (ERD)

![Entity Relationship Diagram](app/static/images/edf.png)

## Структура проекта

- `app/` — основной код приложения
  - `__init__.py` — инициализация приложения и конфигурация базы данных
  - `routes/` — маршруты приложения
  - `models/` — модели базы данных
  - `forms/` — формы ввода
  - `templates/` — HTML шаблоны
  - `static/` — статические файлы (CSS, JS, изображения)
- `reset_db.py` — скрипт для сброса базы данных
- `seed_db.py` — скрипт для заполнения базы данных начальными данными
- `run.py` — запуск приложения
- `requirements.txt` — зависимости проекта

## Контакты

Для вопросов и предложений обращайтесь по адресу: [silennemoy@gmail.com](mailto:silennemoy@gmail.com)
