# LittleLemonAPI
## Introduction
Welcome to the LittleLemon API, a powerful tool designed specifically for the LittleLemon restaurant. Our API empowers users to seamlessly book tables, place food orders, and efficiently manage the entire process. With comprehensive features tailored to streamline operations for managers, delivery crew, and users alike.
## Prerequistes
* Git
* Python
* Mysql
## Installation Guide
* Clone this repository
```bash
git clone https://github.com/oel21sakka/LittlelemonAPI LittleLemon
```
* Run pipenv install to install all dependcies
```bash
pipenv install
```
* Activate the virtual environment if it's not already activated
```bash
pipenv shell
```
* Create database for the app from the mysql shell
```bash
CREATE DATABASE [LittleLemon]
```
* add your database configrations in database.cnf
```
database = littlelemon
user = django
password = 1234@Django
host = 127.0.0.1
port = 3306
```
* Run the migrations to create the necessary database tables and schema
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
* To load some data we have made to test the app easily use the fixtures file
```bash
python3 manage.py loaddata fixtures.json
```
### Usage
To run the server and start using the API, follow these steps:
```bash
python3 manage.py runserver
```
### API Endpoints
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| POST | /auth/users/ | Sign up a new user account |
| POST | /auth/token/login | Log in an existing user account |
| GET / POST | /api/categories | Get all categories / Add a new category |
| GET / POST | /api/menu-items | To get all menu-items / add new menu-itemGet all menu items / Add a new menu item |
| GET / PUT / PATCH / DELETE | /api/menu-items/:Id |  Get/Update/Delete a menu item by ID |
| GET / POST / DELETE | /api/cart/menu-items | Get all items in the cart / Add/Delete an item |
| GET / POST | /api/orders | Get all orders / Add a new order |
| GET / PUT / PATCH / DELETE | /api/orders/:Id | Get/Update/Delete an order by ID |
| GET / POST / DELETE | /api/managers/users |  Get all managers / Add/Revoke manager role |
| GET / POST / DELETE | /api/delivery-crew/users |  Get all delivery crew / Add/Revoke crew role |
