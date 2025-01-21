# Flower Delivery

Flower Delivery — это комплексное веб-приложение для заказа и доставки цветов, которое включает в себя интеграцию с Telegram-ботом для управления и мониторинга заказов.

## О проекте

Проект Flower Delivery предназначен для создания удобного веб-интерфейса, где пользователи могут легко выбирать и заказывать цветы с доставкой. Вся система поддерживает работу с возможностью отслеживания заказов и их управления через Telegram-бота.

### Основные возможности

- **Регистрация и авторизация пользователей**: пользователи могут создавать учетные записи, управлять своими данными и входить в систему.
- **Просмотр каталога цветов**: удобная навигация и поиск по каталогу с различными категориями и фильтрами.
- **Корзина и оформление заказа**: пользователи могут добавлять товары в корзину, оформлять заказы с указанием данных для доставки и просматривать историю заказов.
- **Telegram-бот**: интеграция с ботом для получения уведомлений о заказах и управления ими.
- **Административная панель**: управление продуктами, категориями и заказами.
- **Поддержка отзывов и рейтингов**: пользователи могут оставлять отзывы и ставить оценки купленным товарам.

## Структура проекта

Проект построен с использованием фреймворка Django на серверной стороне и Telegram API для бота. Основные компоненты включают:

- **Django-приложения**:
  - Управление заказами, продуктами, категориями и отзывами.
  - Управление пользователями и их профилями.
  - Модуль для работы с файлами и их отображения.
- **Telegram-бот**: работает на базе aiogram, используется для приема и управления заказами, а также отправки уведомлений.
- **База данных**: используется SQLite (возможно, другая СУБД на продакшене).
- **Статические файлы**: стили, иконки, скрипты.
- **Шаблоны**: HTML-шаблоны для рендеринга страниц.

### Основные технологии

- Python и Django для серверной части.
- HTML/CSS для фронтенда.
- aiogram для интеграции с Telegram.
- SQLite как база данных для локальной разработки.

## Установка

### Клонирование репозитория


git clone https://github.com/yourusername/flower_delivery.git
cd flower_delivery


### Установка зависимостей

Создайте виртуальное окружение и установите зависимости:


python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
pip install -r requirements.txt


### Настройка базы данных

Примените миграции для базы данных из директории `flower_delivery`:


python manage.py makemigrations
python manage.py migrate


### Создание суперпользователя

Для доступа к административной панели создайте суперпользователя:


python manage.py createsuperuser


### Запуск сервера разработки

Запустите сервер разработки из директории `flower_delivery`:

python manage.py runserver


Приложение будет доступно по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Доступ к административной панели

Административная панель доступна по адресу [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Запуск тестов

Выполняйте тесты из директории `flower_delivery`:


python manage.py test core_app.tests.test_models
python manage.py test core_app.tests.test_views
python manage.py test core_app.tests.test_urls
python manage.py test core_app.tests  # Для всех тестов сразу


## Запуск Telegram-бота

Предварительно добавьте в меню бота команды `/start` и `/exit` через BotFather. Затем выполните из корневой директории проекта:

python bot\bot.py


## Настройка переменных окружения

Создайте файл `.env` в директориях:

- **bot**:


BOT_TOKEN = "BOT_TOKEN"
DB_PATH = flower_delivery/db.sqlite3
MEDIA_PATH = flower_delivery/media


## Разработка

Проект разработан в среде PyCharm с использованием Django и aiogram.

## Структура проекта

```plaintext
flower_delivery_project/
├── .venv/                # Виртуальное окружение для Python
├── bot/                  # Папка с ботом для взаимодействия с системой
├── flower_delivery/      # Основной модуль Django проекта
│   ├── core_app/         # Основное приложение проекта
│   │   ├── migrations/   # Миграции базы данных для `core_app`
│   │   ├── templates/    # Шаблоны HTML для `core_app`
│   │   ├── __init__.py   # Указатель на то, что это пакет Python
│   │   ├── admin.py      # Конфигурация административной панели Django
│   │   ├── apps.py       # Конфигурация приложения `core_app`
│   │   ├── forms.py      # Файлы с формами Django
│   │   ├── models.py     # Определения моделей базы данных
│   │   ├── populate_db.py # Скрипт для заполнения базы данных
│   │   ├── tests.py      # Модуль для тестирования приложения
│   │   ├── urls.py       # URL-маршруты для приложения `core_app`
│   │   ├── views.py      # Логика обработки запросов для приложения `core_app`
│   ├── flower_delivery/  # Папка для конфигурации всего проекта
│   │   ├── __init__.py   # Указатель на то, что это пакет Python
├── media/                # Каталог для хранения загружаемых файлов
├── static/               # Статические файлы (CSS, JS, изображения)
├── templates/            # Общие шаблоны HTML для всего проекта
├── db.sqlite3            # SQLite база данных
├── manage.py             # Главный файл управления Django проектом
├── requirements.txt      # Список зависимостей проекта
├── .env                  # Конфиденциальная информация (токены, пароли)
├── .gitignore            # Исключения для Git
```

## Лицензия

Проект распространяется под лицензией MIT.
