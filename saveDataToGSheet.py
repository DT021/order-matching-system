import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM'
SAMPLE_RANGE_NAME = 'A1:AA1000'

def main():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/vishalbns/Desktop/angular-flask/credentials.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    if not values_input and not values_expansion:
        print('No data found.')

main()

df=pd.DataFrame(values_input[1:], columns=values_input[0])
print(df)

newData = {'ordertype': ['buy'], 'quantity': [500.0], 'price': [220.0]}
newDataList = ['buy', 500, 220.0]
#change this by your sheet ID
SAMPLE_SPREADSHEET_ID_input = '1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM'

#change the range if needed
SAMPLE_RANGE_NAME = 'A2:C2'

def Create_Service(client_secret_file, api_service_name, api_version, *scopes):
    global service
    SCOPES = [scope for scope in scopes[0]]
    #print(SCOPES)
    
    cred = None

    if os.path.exists('token_write.pickle'):
        with open('token_write.pickle', 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open('token_write.pickle', 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        #return service
    except Exception as e:
        print(e)
        #return None
        
# change 'my_json_file.json' by your downloaded JSON file.
Create_Service('/Users/vishalbns/Desktop/angular-flask/credentials.json', 'sheets', 'v4',['https://www.googleapis.com/auth/spreadsheets'])


def Export_Data_To_Sheets(orderList):
    response_date = service.spreadsheets().values().update(
        spreadsheetId='1WYScLRCDOXL1zZK6nma6InmkDDvjrOAN4I8gVo2I7uM',
        valueInputOption='RAW',
        range='NewOrders!A2:D2',
        body=dict(
            majorDimension='ROWS',
            values=[orderList])
    ).execute()
    print('Sheet successfully Updated')

