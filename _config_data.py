import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',]
SPREADSHEET_ID = '12B5ilZlcCaEHvR1HbPrBKCAMJHc3OA_oookHDrQjHlQ'
ACTION_RANGE_NAME = 'action_sequence!A1:D'
#CONFIG_NAME = 'config!A1:B'
LOG_NAME = 'LOG!A1:I'

def get_action_sheet_data():
   creds=None
   if os.path.exists('token.json'):
      creds=Credentials.from_authorized_user_file('token.json',SCOPES)
   if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
         creds.refresh(Request())
      else:
         flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
         creds = flow.run_local_server(port=0)
         # Save the credentials for the next run
         with open('token.json', 'w') as token:
             token.write(creds.to_json())
   try:
      service=build('sheets','v4',credentials=creds); sheet=service.spreadsheets()
      #config=sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=CONFIG_NAME).execute()
      #c=config.get('values',[]); url=c[0]
      result=sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=ACTION_RANGE_NAME).execute()
      values=result.get('values',[])
      if not values:
        print('No data found.')
        return
      return values
   except HttpError as err:
      print(err)

def append_log_data(rows:list()=[]):
   creds=None
   if os.path.exists('token.json'):
      creds=Credentials.from_authorized_user_file('token.json',SCOPES)
   if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
         creds.refresh(Request())
      else:
         flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
         creds = flow.run_local_server(port=0)
         # Save the credentials for the next run
         with open('token.json', 'w') as token:
             token.write(creds.to_json())
   try:
      service=build('sheets','v4',credentials=creds)
      sheet=service.spreadsheets()
      vls=sheet.values()
      request=vls.append(spreadsheetId=SPREADSHEET_ID,range=LOG_NAME,
      valueInputOption='USER_ENTERED',body={'values':rows},)
      request.execute()
   except HttpError as err:
      print(err)

def clear_log():
   creds=None
   if os.path.exists('token.json'):
      creds=Credentials.from_authorized_user_file('token.json',SCOPES)
   if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
         creds.refresh(Request())
      else:
         flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
         creds = flow.run_local_server(port=0)
         # Save the credentials for the next run
         with open('token.json', 'w') as token:
             token.write(creds.to_json())
   try:
      service=build('sheets','v4',credentials=creds); sheet=service.spreadsheets()
      vls=sheet.values()
      request=vls.clear(spreadsheetId=SPREADSHEET_ID,range=LOG_NAME)
      request.execute()
   except HttpError as err:
      print(err)
