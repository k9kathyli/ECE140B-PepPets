import mysql.connector as mysql
import os
from dotenv import load_dotenv

load_dotenv('credentials.env')

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']

db = mysql.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
)

cursor = db.cursor()
cursor.execute("USE Lab8")
