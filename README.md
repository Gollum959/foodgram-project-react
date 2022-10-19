![statuspy workflow](https://github.com/Gollum959/foodgram-project-react/actions/workflows/cuisine_workflow.yml/badge.svg)

[Foodgram](http://51.250.44.121/)

[Admin](http://51.250.44.121/admin/)

[Redock](http://51.250.44.121/api/docs/)

[**Description of the project**](#description-of-the-project)

[**Filling the env file**](#filling-the-env-file)

[**Commands to run an application in containers**](#commands-to-run-an-application-in-containers)

[**Command to fill in the database**](#command-to-fill-in-the-database)

[**Backend author**](#backend-author)

[**Backend technologies**](#backend-technologies)


## Description of the project

On this service, users will be able to publish recipes, subscribe to publications of other users, add their favorite recipes to the "Favorites" list, and before going to the store, download a summary list of products needed to prepare one or more selected dishes. 

Frontend - React single page application.

Backend - Django REST framework

### Some examples of valid API requests

**Registration and authorization of a new user**
> POST |  [http://127.0.0.1:8000/api/users/](http://127.0.0.1:8000/api/users/)
```
{
    "email":"email@email.com",
    "username":"me",
    "first_name": "first_name",
    "last_name": "last_name",
    "password": "password"
}
```

Response samples
> 201
```
{
"email": "vpupkin@yandex.ru",
"id": 0,
"username": "vasya.pupkin",
"first_name": "Вася",
"last_name": "Пупкин"
}
> 200 OK
```

>  POST |  [http://127.0.0.1:8000/api/auth/token/login/](http://127.0.0.1:8000/api/auth/token/login/)
```
{
"password": "string",
"email": "string"
}
```
> 201 OK
```
{
"auth_token": "string"
}
```
**Getting a list of all recipes**
> GET |  [http://127.0.0.1:8000/api/recipes/](http://127.0.0.1:8000/api/recipes/)
> 200 OK

After deploying the server on the local machine, you can see all api requests at [Redock](http://localhost/api/docs/)

## Filling the env file

**DB_ENGINE**=django.db.backends.postgresql  # indicate that we are working with postgresql
**DB_NAME**=postgres  # database name
**POSTGRES_USER**=postgres  # database login
**POSTGRES_PASSWORD**=postgres  # database password
**DB_HOST**=db  # name of the service (container) 
**DB_PORT**=5432  # port for connecting to the database
**SECRET_KEY**=' ' # django Secret Key
**DEBUG**= # True or False
**ALLOWED_HOSTS**=[] # for example ['localhost', '127.0.0.1', 'web']

## Commands to run an application in containers
```
docker-compose up -d
docker-compose exec web python manage.py migrate 
docker-compose exec web python manage.py createsuperuser 
docker-compose exec web python manage.py collectstatic --no-input
```
## Command to fill in the database
```
docker-compose exec web python manage.py loaddata ingredient.json
```
## Backend author 
[Aleksandr Alekseev](https://github.com/Gollum959/)

## Backend technologies

Project is created with:
* Python 3.7
* PostgreSQL
* Django 2.2.16
* Django REST framework 3.12.4
* Docker version 20.10.12
* Docker Compose version v2.11.0
* Nginx/1.18.0 (Ubuntu)

