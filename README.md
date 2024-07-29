# drf-testovoe
___
## Разработан API для работы со балансом пользователя и перемещении денег между пользователями системы.

Стэк:
PostgreSQL
Django
___
### Установка 
```
git clone https://github.com/Flowmikro/drf-testovoe.git
```
Перейти в директорию 
```
drf-testovoe
```
#### Через Docker
Прописать `.env.docker` и `.env.db.user`. Есть примеры `.env.docker.example` и `.env.db.user.example`  
Запустить билд 
```
docker-compose up -d --build  
```
Создать суперпользователя 
```
docker-compose exec web python manage.py createsuperuser
```
Документация
```
http://localhost:8000/api/docs/
```
