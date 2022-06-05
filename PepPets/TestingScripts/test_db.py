import mysql.connector as mysql


HOST = "db-mysql-sfo2-96686-do-user-11317347-0.b.db.ondigitalocean.com"
DATABASE = "peppetEMAIL"
PORT = 25060
USER = "doadmin"
PASSWORD = "AVNS_1OJ-Nk7eUgMXbec"

db = mysql.connect(host=HOST, database=DATABASE,
                       user=USER, password=PASSWORD)
cursor = db.cursor()
print("connected to: ", db.get_server_info())