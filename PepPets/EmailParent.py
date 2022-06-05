# Import Google Sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Import email modules
import smtplib
from email.message import EmailMessage
EMAIL_ADDRESS = 'peppetsteam@gmail.com'
EMAIL_PASSWORD = 'zzjbxeosrfohcecv'

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("Website/token.json", SCOPES)
online_client = gspread.authorize(credentials)
sheet = online_client.open("PepPet Users").sheet1

msg = EmailMessage()
msg['Subject'] = 'Pep Pet found a new Friend!'
msg['From'] = EMAIL_ADDRESS

msg.set_content("Hello, your child's Pep Pet has made a brand new friend!")

# Get email by pet ID
def get_email(user_pet_id):
    # Query sheet
    email = 0
    for row in range(1, len(sheet.col_values(2))+1):
        if (sheet.cell(row, 2).value == user_pet_id):
            email = sheet.cell(row, 1).value

    return email

# Send email by pet ID
def send_email(user_pet_id):
    email = get_email(user_pet_id)
    if email is None:
        print("No Email was found")
        exit

    msg['To'] = email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

send_email("Kendrick")