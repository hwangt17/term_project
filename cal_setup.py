import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_google_cal():

    SCOPES = ['https://www.googleapis.com/auth/calendar']

    CREDENTIALS_FILE = 'credentials.json'
    
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)

    creds = flow.run_local_server(port=0)

    service = build('calendar', 'v3', credentials=creds)
    return service

def main():
    service = get_google_cal()

if __name__ == '__main__':
    main()