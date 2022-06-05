# Import Google Sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("Website/token.json", SCOPES)
online_client = gspread.authorize(credentials)
sheet = online_client.open("PepPet Users").sheet1

# Get first-most unfinished task
def get_task(user_pet_id):
    # Query sheet
    task = 0
    for row in range(1, len(sheet.col_values(2))+1):
        if (sheet.cell(row, 2).value == user_pet_id and sheet.cell(row, 4).value == "FALSE"):
            task = sheet.cell(row, 3).value

    return task