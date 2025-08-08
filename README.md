# Social Media API

This is a RESTful API for a simple social media application built with Django and Django REST Framework.

## Features

- User registration and authentication (JWT)
- Create, update, and delete posts
- Like and unlike posts
- Add and delete comments on posts
- View user profiles and their posts
- Admin panel for managing all resources

## Technologies Used

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- Simple JWT for authentication

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/UrbanAstronaut88/social-media-api.git
cd social-media-api
```

2. **Create a .env file in the root directory**
3. **Build and run with Docker**
```bash
docker-compose up --build
```
4. **Run migrations and create a superuser**
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser 
```

5. **Access the application**

* API Root: http://127.0.0.1:8000/api/

* Admin Panel: http://127.0.0.1:8000/admin/

## Run the tests with the command

```bash
docker-compose exec web python manage.py test posts.tests.test_likes_comments
```
