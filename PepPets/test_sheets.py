import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("token.json", SCOPES)
online_client = gspread.authorize(creds)

sheet = online_client.open("PepPet Users").sheet1

user = ["anthony", "kendrick", "kathy", "alex"]
user_id = ["sussybaka", "fornite", "minecraft", "thanos"]

for i in range(4):
    new_row = len(sheet.col_values(1)) + 1
    sheet.update_cell(new_row, 1, user[i])
    sheet.update_cell(new_row, 2, user_id[i])
