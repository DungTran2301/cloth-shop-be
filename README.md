# cloth-shop-be
## Setup MySQL DB
Open your MySQL and create new database "clothshop"

```python
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        "ENGINE": 'django.db.backends.mysql',
        "NAME": 'clothshop', # Or path to database file...
        "USER": '', # Replace with your mysql user name
        "PASSWORD": '', # Replace with your mysql password
        "HOST": '', # Set to empty string for localhost....
        "PORT": '', 
    }
}
```
**Deprecated**
1. Open mysql in terminal
* Open a terminal or command prompt.
* Type the following command to log in to MySQL:
```terminal
mysql -u <username> -p
```
Replace <username> with the username that you use to connect to your MySQL server.
* Press Enter. You'll be prompted to enter your MySQL password.
* Type your MySQL password and press Enter.
* If the login is successful, you'll see the MySQL prompt, which looks like this:

2. Execute the following commands in sequence: 
```terminal
mysql> CREATE DATABASE bookstore CHARACTER SET utf8; 
Query OK, 1 row affected (0.00 sec) 
mysql> CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY '2001'; 
Query OK, 0 rows affected (0.00 sec) 
mysql> GRANT ALL ON bookstore.* TO 'root'@'localhost'; 
Query OK, 0 rows affected (0.00 sec) 
```
## Migrate db
```terminal
\cloth-shop-be\ecomstore> py manage.py migrate      
\cloth-shop-be\ecomstore> py manage.py makemigrations
```

## Run server
```terminal
\cloth-shop-be\ecomstore> py manage.py runserver
```
