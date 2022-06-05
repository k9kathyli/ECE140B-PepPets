# Import Google Sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("Website/token.json", SCOPES)
online_client = gspread.authorize(credentials)
sheet = online_client.open("PepPet Users").sheet1

# Get task
def get_task(user_pet_id):
    # Query sheet
    task = 0
    for row in range(1, len(sheet.col_values(2))+1):
        if (sheet.cell(row, 2).value == user_pet_id):
            task = sheet.cell(row, 3).value

    return task

# Check if task is finished
def check_task(user_pet_id):
    task = get_task(user_pet_id)

    return bool(task)


# Main entrypoint
if __name__ == '__main__':
    print(check_task("Kendrick"))
