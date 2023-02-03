# SICK LOOT
## About project:
### It`s Dota 2 open case RESTful API
### This API contains most of the possible options for sites with case openings such as:
- User registration and authorization by JWT Token
- Balance replenish and winraw
- Viewing and selling items from inventory
- The ability to add your own things and cases
- Open different cases with random drop
- Account level which depends of count of open cases
---
## Stack:
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
---
## Instalation:
In terminal:
```
git clone https://github.com/OneFallDen/sickloot
```
```
setup requirements.txt install
```
In PostgreSQL:
```
CREATE DATABASE sickloot;
```
In terminal:
```
python sql/models.py createdb
```
```
uvicorn main:app
```
In PostgreSQL:
```
\i sql/items_cases_sets.sql
```
---
### So we run the server
---
#### There you can try all fucntional of RESTful API
#### For documantion you can use:
- localhost:8000/docs
- localhost:8000/redoc