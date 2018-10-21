# flaskr-tutorial

mkdir instance
touch instance/config.py

# vi instance/config.py
SECRET_KEY= 'your secret_key'
SQLALCHEMY_DATABASE_URI = 'mysql:USER_NAME:USER_PASS@CONNECT_IP/DB_NAME'

# pip install
pip install flask-sqlalchemy mysqlclient flask-login flask-migrate

# For Migration
flask db init
flask db migrate
flask db upgrade
