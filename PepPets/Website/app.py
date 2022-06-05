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

# Return home page
def index_page(req):
   return FileResponse("index.html")

# Return task page
def task_page(req):
   return FileResponse("task.html")

def decode_url(url):
    result = urllib.parse.unquote(url)
    return result

# Function to access email and petID data
def register_user(req):
    # Get email from request
    user_email = decode_url(req.matchdict['email'])
    # Get petID from request
    user_pet_id = decode_url(req.matchdict['petID'])

    # Query sheet
    new_row = len(sheet.col_values(1)) + 1
    sheet.update_cell(new_row, 1, user_email)
    sheet.update_cell(new_row, 2, user_pet_id)

# Function to create task
def create_task(req):
    # Get petID from request
    user_pet_id = decode_url(req.matchdict['petID'])
    # Get task description from request
    user_task = decode_url(req.matchdict['task_description'])

    # Query sheet
    for row in range(1, len(sheet.col_values(2))+1):
        if (sheet.cell(row, 2).value == user_pet_id):
            sheet.update_cell(row, 3, user_task)

# Function to confirm completion/deletion of task
def finish_task(req):
    # Get petID from request
    user_pet_id = decode_url(req.matchdict['petID'])

    # Query sheet
    for row in range(1, len(sheet.col_values(2))+1):
        if (sheet.cell(row, 2).value == user_pet_id):
            sheet.update_cell(row, 3, "")

# Main entrypoint
if __name__ == '__main__':
   with Configurator() as config:
       # Create a route called home. Bind the view (defined by index_page) to the route named ‘home’
       config.add_route('home', '/')
       config.add_view(index_page, route_name='home')

       # Create a route called register. Bind the view to the route named ‘register’
       config.add_route('register_user', '/user/{email}/{petID}')
       config.add_view(register_user, route_name='register_user', renderer='json')

       # Create a route called task. Bind the view (defined by task_page) to the route named ‘task’
       config.add_route('task', '/task')
       config.add_view(task_page, route_name='task')

       # Create a route called create_task. Bind the view to the route named create_task
       config.add_route('create_task', '/task/{petID}/{task_description}')
       config.add_view(create_task, route_name='create_task', renderer='json')

       # Create a route called task. Bind the view (defined by task_page) to the route named ‘task’
       config.add_route('finish_task', '/finishedtask/{petID}')
       config.add_view(finish_task, route_name='finish_task', renderer='json')

       # Add a static view
       config.add_static_view(name='/', path='./public', cache_max_age=3600)

       # Create an app with the configuration specified above
       app = config.make_wsgi_app()

   # Start the application on port 6543
   server = make_server('0.0.0.0', 6543, app)
   server.serve_forever()
