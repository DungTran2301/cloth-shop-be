# book-store-be
## Setup MySQL DB
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
\book-store-be\ecomstore> py manage.py migrate      
\book-store-be\ecomstore> py manage.py makemigrations
```

## Run server
```terminal
\book-store-be\ecomstore> py manage.py runserver
```
