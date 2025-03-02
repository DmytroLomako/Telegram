import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .models import User, Session

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "" #Ваш ID таблицы
path_to_json = os.path.abspath(__file__+f'/..')
 # Назва аркуша і діапазон


def connection():
    creds = None
    path = os.path.join(path_to_json, 'token.json')
    if os.path.exists(path):
        creds = Credentials.from_authorized_user_file(path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            path = os.path.join(path_to_json, 'credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(path, SCOPES)
        creds = flow.run_local_server(port = 0)
    path = os.path.join(path_to_json, 'token.json')
    with open(path, "w") as token:
        token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials = creds)  
        return service  
    except HttpError as err:
        print(err)
    
def read(service, RANGE_NAME):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId = SAMPLE_SPREADSHEET_ID, range = RANGE_NAME).execute()
    values = result.get("values", [])
    print(values)
    session = Session()
    for value in values:
        user = User(username=value[0], password=value[1], email=value[2])
        session.add(user)
        session.commit()
    session.close()
    

service = connection()  