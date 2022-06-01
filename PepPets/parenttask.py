import mysql.connector as mysql

HOST= "db-mysql-sfo2-96686-do-user-11317347-0.b.db.ondigitalocean.com"
DATABASE="peppetEMAIL"
PORT=25060
USER="doadmin"
PASSWORD ="AVNS_1OJ-Nk7eUgMXbec"


def getParentTask(id):
    db = mysql.connect(host=HOST,database=DATABASE,user=USER,password=PASSWORD,port=PORT)
    print("connected to: ",db.get_server_info())
    cursor=db.cursor()
    query = "SELECT task,reward from parentTask where petid='"+id+"';"
    cursor.execute(query)
    record = cursor.fetchall()
    if record is None:
            print("no custom task assigned yet")
            return None
    db.close()
    return(record[0][0],record[0][1])
    


def isCompleted(id):
    db = mysql.connect(host=HOST,database=DATABASE,user=USER,password=PASSWORD,port=PORT)
    print("connected to: ",db.get_server_info())
    cursor=db.cursor()
    query ="SELECT completed from parentTask where petid='"+id+"';"
    cursor.execute(query)
    record = cursor.fetchall()
    db.close()
    completed = record[0][0]

    if completed == 1:
        print("Task completed!")
        return True
    else:
        print("Task not Completed...")
        return False
# print(getParentTask(str(999555)))
# isCompleted(str(999555))
