
# foodgram-project-react (API)
<div id="badges">
  <img src="https://img.shields.io/badge/JScript-yellow?style=for-the-badge&logo=JavaScript&logoColor=white" alt="JavaScript"/> <img src="https://img.shields.io/badge/React-informational?style=for-the-badge&logo=react&logoColor=white" alt="React 17.0.1"/> <img src="https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.7"/>  <img src="https://img.shields.io/badge/django-blue?style=for-the-badge&logo=django&logoColor=white" alt="Django 3.2.15"/>  <img src="https://img.shields.io/badge/Docker-yellow?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Desktop 4.11.1"/>
</div>

______________________________
### Project status
![Build status](https://github.com/Cognitoid/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
________________________

#### Описание:
«Продуктовый помощник» (Развитие проекта Яндекс.Практикум в рамках дипломной работы)
Данный интернет-сервис является социальной сетью для обмена кулинарными рецептами. Все пользователи могут читать любые рецепты и получать список продуктовых ингредиентов. Авторизованные пользователи могут создавать свои рецепты, подписываться на других авторов, добавлять полюбившиеся рецепты в избранное и в список покупок, загружать последний в текстовой формате.

Посмотреть развернутый проект можно здесь: http://foodgram-net.3utilities.com.
________________________

#### Основные технологии:
Сервис «Продуктовый помощник» в части бэкенда реализован на языке Python 3.7 на основе архитектуры REST API и использует Django REST Framework 3.13.1 c аутентификацией на базе DJoser 2.1.0, фронтенд - на языке JavaScript на основе фреймворка React 17.0.1. 
__________________________

#### Как запустить проект:
**Шаг 1. Проверка и установка Docker**
Убедитесь, что у вас установлен Docker. Для этого введите команды:
```
docker -v
```
При отсутствии скачайте и установите [Docker Desktop для своей версии ОС] (https://www.docker.com/products/docker-desktop/).

**Шаг 2. Клонирование репозитория с проектом на свой компьютер**
Введите команду:
```
git clone git@github.com:Cognitoid/foodgram-project-react.git
```

**Шаг 3. Создание файла с переменными окружения .env**
Пример:
```
SECRET_KEY=... (ключ к Джанго проекту, ни в коем случае не публикуйте его)
DB_ENGINE=django.db.backends.postgresql (указываем, что работаем с postgresql)
DB_NAME=postgres (имя базы данных)
POSTGRES_USER=... (указываем свой логин для подключения к базе данных)
POSTGRES_PASSWORD=... (указываем свой пароль для подключения к БД)
DB_HOST=db (название сервиса контейнера)
DB_PORT=5432 (порт для подключения к БД)
ALLOWED_HOSTS=localhost (через "пробел" указываем хосты, с которых разрешено обращение к сервису, среди них обязательно должен быть хост "backend")
DEBUG=True (по умолчанию режим отладки отключен, если нужно включить, то прописываем переменную и указываем "True")
EMPTY_VALUE=--пусто-- (здесь указываем значение, которое будет отражаться на месте пустых полей)
INGREDIENT_QUANTITY=4 (количество ингредиентов, отражаемых по умолчанию в админке)
```
**Шаг 4. Запуск docker-compose**
Для запуска необходимо выполнить из директории проекта infra/ команду:
```
docker-compose up -d
```

**Шаг 5. Задание структуры базы данных**
Примените миграции:
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

**Шаг 6. Подгрузка статики**
Выполните команду:
```
docker-compose exec web python manage.py collectstatic
```

**Шаг 7. Создание суперпользователя**
Выполните команду:
```
docker-compose exec web python manage.py createsuperuser
```

**Шаг 8. Заполнение базы тестовыми данными (необязательный шаг)**
Выполните команду:
```
docker-compose exec web python manage.py loaddata db.json
```
**Другие команды для работы с образами и контейнерами проекта**
Остановить работу всех контейнеров:
```
docker-compose down
```
Пересборка и запуск контейнеров:
```
docker-compose up -d --build 
```
Мониторинг запущенных контейнеров:
```
docker stats
```
Остановка и удаление контейнеров, томов и образов:
```
docker-compose down -v
```
______________________
#### Техническое описание проекта:
Список эндпойнтов и их описание доступны в формате Redoc по ссылке: http://localhost/api/docs/redoc.html
______________________
#### Автором данного кода является:
- [Владимир Мазняк](https://github.com/Cognitoid).
________________________
#### Образы ПО на DockerHub:
- Backend - enior/foodgram_backend:latest,
- Frontend - enior/foodgram_frontend:latest
- *Скачать с DockerHub:*
```
docker pull enior/foodgram_backend:latest
docker pull enior/foodgram_frontend:latest
```

________________________
© Яндекс.Практикум, Cognitoid, 2022
