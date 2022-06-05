import mysql.connector as mysql

HOST= "db-mysql-sfo2-96686-do-user-11317347-0.b.db.ondigitalocean.com"
DATABASE="peppetEMAIL"
PORT=25060
USER="doadmin"
PASSWORD ="AVNS_1OJ-Nk7eUgMXbec"


def makeDB():
    db = mysql.connect(host=HOST, database=DATABASE,
                       user=USER, password=PASSWORD, port=PORT)
    print("connected to: ", db.get_server_info())

    cursor = db.cursor()

    table1 = """
        CREATE TABLE IF NOT EXISTS ID_Emails (
            id integer auto_increment primary key,
            petid varchar(32),
            owner varchar(32)
        );
        """
    cursor.execute(table1)

    table2 = """
        CREATE TABLE IF NOT EXISTS parentTask(
            id integer auto_increment primary key,
            petID varchar(32),
            task text,
            completed boolean,
            reward varchar(32)
        );
    """
    cursor.execute(table2)
    
    cursor.execute("SHOW TABLES")
    db.commit()
    db.close()

# makeDB()  careful if you call this 