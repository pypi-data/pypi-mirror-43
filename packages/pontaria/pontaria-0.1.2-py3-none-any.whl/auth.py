from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from sys import stdout
import gspread

SCOPES = ['https://www.googleapis.com/auth/drive']

print('Authenticating on GoogleAPI...')
stdout.write("\033[F\033[K")
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server()
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)


class Credentials():
  def __init__(self, creds=None):
    self.__creds = creds
    self.access_token = creds.token

# print(Credentials(creds))
gc = gspread.authorize(Credentials(creds))
