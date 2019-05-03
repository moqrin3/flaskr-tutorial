#!/bin/sh

mkdir instance

cat <<EOL >> ./instance/config.py
import os

SECRET_KEY= 'your secret_key'
SQLALCHEMY_DATABASE_URI = 'mysql://'+ os.environ["USER_NAME"] +':' + os.environ["USER_PASS"] + '@' + os.environ["DB_ENDPOINT"] + '/' + os.environ["DB_NAME"]

EOL

echo "SELECT 1 FROM user LIMIT 1;" | mysql -h $DB_ENDPOINT -u $USER_NAME -p$USER_PASS $DB_NAME

if [ $? = 0 ]; then
    python run.py
else
    flask db init
    flask db migrate
    flask db upgrade
    
    sleep 5;
    python run.py
fi