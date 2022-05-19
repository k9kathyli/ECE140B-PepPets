import mysql.connector as mysql
import smtplib
from email.message import EmailMessage
EMAIL_ADDRESS ='peppetsteam@gmail.com'
EMAIL_PASSWORD = 'zzjbxeosrfohcecv' 

HOST= "db-mysql-sfo2-96686-do-user-11317347-0.b.db.ondigitalocean.com"
DATABASE="peppetEMAIL"
PORT=25060
USER="doadmin"
PASSWORD ="AVNS_1OJ-Nk7eUgMXbec"


msg= EmailMessage()
msg['Subject']='PepPet found a new Friend!'
msg['From'] = EMAIL_ADDRESS

msg.set_content('Hello, your childs PepPet has made a brand new friend!')



def getEmail(id):
    db = mysql.connect(host=HOST,database=DATABASE,user=USER,password=PASSWORD,port=PORT)
    print("connected to: ",db.get_server_info())

    cursor=db.cursor()
    query = "SELECT owner from ID_Emails WHERE petid='"+ id +"'"
    cursor.execute(query)
    record = cursor.fetchone()
    if record is None:
            return
    
    return record[0];

def sendEmail(id):
    email = getEmail(id)
    if email is None:
        print("No Email was found")
        exit;
    msg['To'] = email
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    
    
