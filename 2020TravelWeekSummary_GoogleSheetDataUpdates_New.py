import pandas as pd
import numpy as np
import pygsheets
import os
import json
from google.oauth2 import service_account

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# read Google APIs through Github secrets
gapi = os.environ.get('GAPI')

# customize the authorization 
SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
service_account_info = json.loads(gapi)
my_credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

client = pygsheets.authorize(custom_credentials =my_credentials)
print("-----------------Authorized--------------------")
sheet = client.open('2020TravelWeekSummary')
print("-----------------Sheet Opened------------------")

# tabledf = pd.read_csv(path+"MTA_recent_ridership_data_20210311.csv", header= 0, index_col=False)
rawdf = pd.read_csv("https://data.ny.gov/api/views/vxuj-8kew/rows.csv?accessType=DOWNLOAD&sorting=true", header= 0, index_col=False)

rawdf = rawdf.drop_duplicates(subset='Date', keep="first")
rawdf.reset_index(drop=True)
rawdf =  rawdf.iloc[::-1]

rawColList = rawdf.columns.tolist()

for i in range(1, 15):
    #rawdf[rawColList[i]] = rawdf[rawColList[i]].astype(str).str.rstrip('%').astype('float') / 100.0
    rawdf[rawColList[i] + ' Avg.'] = rawdf[rawColList[i]].rolling(7, min_periods=1).mean()
    rawdf.loc[rawdf["Date"]=="03/01/2020", rawColList[i] + ' Avg.'] = np.nan
    rawdf.loc[rawdf["Date"]=="03/01/2020", rawColList[i]] = np.nan
    rawdf.loc[rawdf["Date"]=="03/02/2020", rawColList[i] + ' Avg.'] = np.nan
    rawdf.loc[rawdf["Date"]=="03/02/2020", rawColList[i]] = np.nan
    rawdf.loc[rawdf["Date"]=="03/03/2020", rawColList[i] + ' Avg.'] = np.nan
    rawdf.loc[rawdf["Date"]=="03/03/2020", rawColList[i]] = np.nan
    rawdf.loc[rawdf["Date"]=="03/04/2020", rawColList[i] + ' Avg.'] = np.nan
    rawdf.loc[rawdf["Date"]=="03/04/2020", rawColList[i]] = np.nan
    rawdf.loc[0, rawColList[i] + ' Avg.'] = np.nan
    rawdf.loc[0, rawColList[i]] = np.nan

tabledf1 = rawdf[rawColList]
tabledf2 = rawdf[['Date'] + list(set(rawdf.columns.tolist()).difference(set(rawColList)))]
tabledf2.columns = tabledf2.columns.str.replace(' Avg.', '')
        
        
tabledf1["Calculation"] = "Daily Ridership"
tabledf2["Calculation"] = "7-Day Moving Averages"

tabledf =  pd.concat([tabledf1, tabledf2])

tabledf['Dates'] = pd.to_datetime(tabledf['Date'], format='%m/%d/%Y')
tabledf["Period"] = np.where(tabledf["Dates"] < pd.to_datetime("01/01/2021", format='%m/%d/%Y'),"2020", \
                             np.where(tabledf["Dates"] < pd.to_datetime("01/01/2022", format='%m/%d/%Y'),"2021", \
                             np.where(tabledf["Dates"] < pd.to_datetime("01/01/2023", format='%m/%d/%Y'),"2022","2023")))

wks = sheet[1]
print("-----------------Second Sheet Accessed----------")

wks.set_dataframe(tabledf,(1,1))
print("-----------------Data Updated------------------")



# rawdf = rawdf.fillna(0)
resultdf = rawdf[rawColList].copy()
resultdf = resultdf[['Date', 'Subways: Total Estimated Ridership','Buses: Total Estimated Ridership','LIRR: Total Estimated Ridership',\
       'Metro-North: Total Estimated Ridership','Access-A-Ride: Total Scheduled Trips','Bridges and Tunnels: Total Traffic']]

resultdf.columns = ['Date', 'Subway Ridership','Bus Ridership','LIRR Ridership','Metro-North Ridership','Access-A-Ride Trips','MTA Bridges and Tunnels Traffic']

ridershipCol = ['Subway Ridership','Bus Ridership','LIRR Ridership','Metro-North Ridership','Access-A-Ride Trips','MTA Bridges and Tunnels Traffic']
    
percentCol = ["Subway Percent Change", "Bus Percent Change", "LIRR Percent Change", "MNR Percent Change", \
              "Access-A-Ride Percent Change", "MTA Bridges and Tunnels Traffic Percent Change"]

for i in range(0, len(ridershipCol)):
    resultdf[ridershipCol[i]] = resultdf[ridershipCol[i]].astype(float) 
    
#tabledf[ridershipCol] = tabledf[ridershipCol].fillna(0)
#tabledf[ridershipCol] = tabledf[ridershipCol].astype(int)        
resultdf['Dates'] = pd.to_datetime(resultdf['Date'], format='%m/%d/%Y')
resultdf['DayofWeek'] = resultdf['Dates'].dt.dayofweek
resultdf['Weekday'] = np.where(resultdf['DayofWeek'].isin([0,1,2,3,4]), "Weekday", "Weekend")

#startDate = pd.to_datetime("03/09/2020", format='%m/%d/%Y')

resultdf["weekOrder"] = np.nan
for i in range(0, resultdf.shape[0]):
    if resultdf.loc[i, "Dates"]<= pd.to_datetime("01/03/2021", format='%m/%d/%Y'):
        resultdf.loc[i, "weekOrder"] = resultdf.loc[i, "Dates"].isocalendar()[1] - 9
    elif resultdf.loc[i, "Dates"]<= pd.to_datetime("01/02/2022", format='%m/%d/%Y'):
        resultdf.loc[i, "weekOrder"] = resultdf.loc[i, "Dates"].isocalendar()[1] + 44
    elif resultdf.loc[i, "Dates"]<= pd.to_datetime("01/01/2023", format='%m/%d/%Y'):
        resultdf.loc[i, "weekOrder"] = resultdf.loc[i, "Dates"].isocalendar()[1] + 96
    else:
        resultdf.loc[i, "weekOrder"] = resultdf.loc[i, "Dates"].isocalendar()[1] + 148
    
resultdf["daySum"] = 1   
weekdaydf = resultdf.groupby(['weekOrder', 'Weekday'], as_index=False).agg({'Date': 'last','Dates': 'last', 'daySum': 'sum', 'Subway Ridership': 'sum', \
                                                                           'Bus Ridership': 'sum', 'LIRR Ridership': 'sum', \
                                                                           'Metro-North Ridership': 'sum', 'Access-A-Ride Trips': 'sum', \
                                                                           'MTA Bridges and Tunnels Traffic': 'sum'})


weekdaydf = weekdaydf.loc[((weekdaydf["daySum"]==2) & (weekdaydf["Weekday"]=="Weekend")) | \
                          ((weekdaydf["daySum"]==5) & (weekdaydf["Weekday"]=="Weekday"))]

print(weekdaydf.loc[1, "Subway Ridership"])
print(type(weekdaydf.loc[1, "Subway Ridership"]))
for i in range(0, len(ridershipCol)):
    print(ridershipCol[i])
    print(weekdaydf[ridershipCol[i]])
    weekdaydf[percentCol[i]] = weekdaydf[ridershipCol[i]].pct_change(periods=2)  

weekdaydf = weekdaydf.replace([np.inf, -np.inf], np.nan)

weekdaydf["Week"] = [("Week of "  + x) for x in weekdaydf["Date"]]

weekdaydf["Period"] = np.where(weekdaydf["Dates"] < pd.to_datetime("01/01/2021", format='%m/%d/%Y'),"2020", \
                               np.where(weekdaydf["Dates"] < pd.to_datetime("01/01/2022", format='%m/%d/%Y'), "2021", \
                               np.where(weekdaydf["Dates"] < pd.to_datetime("01/01/2023", format='%m/%d/%Y'),"2022","2023")))

weekdaydf.drop('Dates', axis=1, inplace=True)

wks = sheet[0]
print("-----------------First Sheet Accessed----------")

wks.set_dataframe(weekdaydf,(1,1))
print("-----------------Data Updated------------------")
