# Import all the server libraries
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import FileResponse
from pyramid.renderers import render_to_response

# Import Google Sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# URL decoding
import urllib.parse

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("token.json", SCOPES)
online_client = gspread.authorize(credentials)
sheet = online_client.open("PepPet Users").sheet1

# Add to friends list
def add_friend(user_pet_id, friend_id):
    for row in range(1, len(sheet.col_values(2))+1):
        if (sheet.cell(row, 2).value == user_pet_id):
            new_friends_list = sheet.cell(row, 5).value + friend_id + "|"
            sheet.update_cell(row, 5, new_friends_list)

# Get friends list
def get_friends(user_pet_id):
    # Query sheet
    friends_list = 0
    for row in range(1, len(sheet.col_values(2))+1):
        if (sheet.cell(row, 2).value == user_pet_id):
            friends_list = sheet.cell(row, 5).value

    return friends_list.split("|")

# Get check if you have met this friend
def check_friend(user_pet_id, friend_id):
    friends_list = get_friends(user_pet_id)

    return friend_id in friends_list
