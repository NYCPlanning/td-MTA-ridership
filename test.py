import pandas as pd
import numpy as np
import pygsheets
import os
import json
from google.oauth2 import service_account

print("hello")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

gapi = os.environ.get('GAPI')
print(gapi)

gapiStr = json.dumps(gapi)

SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
service_account_info = json.loads(gapiStr)
print("service_account_info")
print(type(service_account_info))
print(service_account_info)
my_credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
