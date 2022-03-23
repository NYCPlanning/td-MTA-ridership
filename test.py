import pandas as pd
import numpy as np
import pygsheets
import os
import json
from google.oauth2 import service_account

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

gapi = os.environ.get('GAPI')
print(gapi)
