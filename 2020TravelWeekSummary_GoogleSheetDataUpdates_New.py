import pandas as pd
import numpy as np
import pygsheets
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

gapi = os.environ.get('GAPI')
print(os.environ.get('GAPI'))

client = pygsheets.authorize(service_account_env_var =gapi)
print("-----------------Authorized--------------------")


sheet = client.open('2020TravelWeekSummary')
print("-----------------Sheet Opened------------------")



# define file path and read raw data
path='/Users/rl/OneDrive - NYC O365 HOSTED/Desktop/subway ridership/Fare/'

# tabledf = pd.read_csv(path+"MTA_recent_ridership_data_20210311.csv", header= 0, index_col=False)
rawdf = pd.read_csv("https://new.mta.info/document/20441", header= 0, index_col=False)


idx = rawdf["LIRR: Total Estimated Ridership"]=="TBD"
rowidx = np.where(idx)[0]
if rowidx.tolist() != []:
    for k in reversed(rowidx):
        print(k)
        rawdf["LIRR: Total Estimated Ridership"] = pd.to_numeric(rawdf["LIRR: Total Estimated Ridership"],errors='coerce')
        rawdf.loc[k, "LIRR: Total Estimated Ridership"] = (rawdf.loc[k + 1, "LIRR: Total Estimated Ridership"] +rawdf.loc[k + 2, "LIRR: Total Estimated Ridership"]+rawdf.loc[k + 3, "LIRR: Total Estimated Ridership"])/3

        rawdf.loc[k, "LIRR: % of 2019 Monthly Weekday/Saturday/Sunday Average"] = "0%"

rawdf['LIRR: % of 2019 Monthly Weekday/Saturday/Sunday Average'] = rawdf['LIRR: % of 2019 Monthly Weekday/Saturday/Sunday Average'].str.rstrip('%').astype('float') / 100.0

if rowidx.tolist() != []:
    for k in reversed(rowidx):
        rawdf.loc[k, "LIRR: % of 2019 Monthly Weekday/Saturday/Sunday Average"] = (rawdf.loc[k + 1, "LIRR: % of 2019 Monthly Weekday/Saturday/Sunday Average"] +rawdf.loc[k + 2, "LIRR: % of 2019 Monthly Weekday/Saturday/Sunday Average"]+rawdf.loc[k + 3, "LIRR: % of 2019 Monthly Weekday/Saturday/Sunday Average"])/3



idx = rawdf["Metro-North: Total Estimated Ridership"]=="TBD"
rowidx = np.where(idx)[0]
if rowidx.tolist() != []:
    for k in reversed(rowidx):
        print(k)
        rawdf["Metro-North: Total Estimated Ridership"] = pd.to_numeric(rawdf["Metro-North: Total Estimated Ridership"],errors='coerce')
        rawdf.loc[k, "Metro-North: Total Estimated Ridership"] = (rawdf.loc[k + 1, "Metro-North: Total Estimated Ridership"] +rawdf.loc[k + 2, "Metro-North: Total Estimated Ridership"]+rawdf.loc[k + 3, "Metro-North: Total Estimated Ridership"])/3

        rawdf.loc[k, "Metro-North: % of 2019 Monthly Weekday/Saturday/Sunday Average"] = "0%"

rawdf['Metro-North: % of 2019 Monthly Weekday/Saturday/Sunday Average'] = rawdf['Metro-North: % of 2019 Monthly Weekday/Saturday/Sunday Average'].str.rstrip('%').astype('float') / 100.0

if rowidx.tolist() != []:
    for k in reversed(rowidx):
        rawdf.loc[k, "Metro-North: % of 2019 Monthly Weekday/Saturday/Sunday Average"] = (rawdf.loc[k + 1, "Metro-North: % of 2019 Monthly Weekday/Saturday/Sunday Average"] +rawdf.loc[k + 2, "Metro-North: % of 2019 Monthly Weekday/Saturday/Sunday Average"]+rawdf.loc[k + 3, "Metro-North: % of 2019 Monthly Weekday/Saturday/Sunday Average"])/3


rawdf



idx = rawdf["Bridges and Tunnels: Total Traffic"]=="TBD"
rowidx = np.where(idx)[0]
if rowidx.tolist() != []:
    rawdf["Bridges and Tunnels: Total Traffic"] = pd.to_numeric(rawdf["Bridges and Tunnels: Total Traffic"],errors='coerce')
    rawdf.loc[rowidx[0], "Bridges and Tunnels: Total Traffic"] = (rawdf.loc[rowidx[0] + 1, "Bridges and Tunnels: Total Traffic"] +rawdf.loc[rowidx[0] + 2, "Bridges and Tunnels: Total Traffic"]+rawdf.loc[rowidx[0] + 3, "Metro-North: Total Estimated Ridership"])/3

    rawdf.loc[rowidx[0], "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"] = "0%"
    rawdf['Bridges and Tunnels: % of Comparable Pre-Pandemic Day'] = rawdf['Bridges and Tunnels: % of Comparable Pre-Pandemic Day'].str.rstrip('%').astype('float') / 100.0
    rawdf.loc[rowidx[0], "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"] = (rawdf.loc[rowidx[0] + 1, "Metro-North: % of 2019 Monthly Weekday/Saturday/Sunday Average"] +rawdf.loc[rowidx[0] + 2, "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"]+rawdf.loc[rowidx[0] + 3, "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"])/3



idx = rawdf["Access-A-Ride: Total Scheduled Trips"]=="TBD"
rowidx = np.where(idx)[0]
if rowidx.tolist() != []:
    rawdf["Access-A-Ride: Total Scheduled Trips"] = pd.to_numeric(rawdf["Access-A-Ride: Total Scheduled Trips"],errors='coerce')
    rawdf.loc[rowidx[1], "Access-A-Ride: Total Scheduled Trips"] = (rawdf.loc[rowidx[1] + 1, "Access-A-Ride: Total Scheduled Trips"] +rawdf.loc[rowidx[1] + 2, "Access-A-Ride: Total Scheduled Trips"]+rawdf.loc[rowidx[1] + 3, "Access-A-Ride: Total Scheduled Trips"])/3
    rawdf.loc[rowidx[0], "Access-A-Ride: Total Scheduled Trips"] = (rawdf.loc[rowidx[0] + 1, "Access-A-Ride: Total Scheduled Trips"] +rawdf.loc[rowidx[0] + 2, "Access-A-Ride: Total Scheduled Trips"]+rawdf.loc[rowidx[0] + 3, "Access-A-Ride: Total Scheduled Trips"])/3
    
    
    rawdf.loc[rowidx[0], "Access-A-Ride: % of Comprable Pre-Pandemic Day"] = "0%"
    rawdf.loc[rowidx[1], "Access-A-Ride: % of Comprable Pre-Pandemic Day"] = "0%"
    rawdf['Access-A-Ride: % of Comprable Pre-Pandemic Day'] = rawdf['Access-A-Ride: % of Comprable Pre-Pandemic Day'].str.rstrip('%').astype('float') / 100.0
    rawdf.loc[rowidx[1], "Access-A-Ride: % of Comprable Pre-Pandemic Day"] = (rawdf.loc[rowidx[1] + 1, "Access-A-Ride: % of Comprable Pre-Pandemic Day"] +rawdf.loc[rowidx[1] + 2, "Access-A-Ride: % of Comprable Pre-Pandemic Day"]+rawdf.loc[rowidx[1] + 3, "Access-A-Ride: % of Comprable Pre-Pandemic Day"])/3
    rawdf.loc[rowidx[0], "Access-A-Ride: % of Comprable Pre-Pandemic Day"] = (rawdf.loc[rowidx[0] + 1, "Access-A-Ride: % of Comprable Pre-Pandemic Day"] +rawdf.loc[rowidx[0] + 2, "Access-A-Ride: % of Comprable Pre-Pandemic Day"]+rawdf.loc[rowidx[0] + 3, "Access-A-Ride: % of Comprable Pre-Pandemic Day"])/3



idx = rawdf["Bridges and Tunnels: Total Traffic"]=="TBD"
rowidx = np.where(idx)[0]
if rowidx.tolist() != []:
    #print("Bridges and Tunnels: % of Comparable Pre-Pandemic Day")
    rawdf["Bridges and Tunnels: Total Traffic"] = pd.to_numeric(rawdf["Bridges and Tunnels: Total Traffic"],errors='coerce')
    #rawdf.loc[rowidx[1], "Bridges and Tunnels: Total Traffic"] = (rawdf.loc[rowidx[1] + 1, "Bridges and Tunnels: Total Traffic"] +rawdf.loc[rowidx[1] + 2, "Bridges and Tunnels: Total Traffic"]+rawdf.loc[rowidx[1] + 3, "Bridges and Tunnels: Total Traffic"])/3
    rawdf.loc[rowidx[0], "Bridges and Tunnels: Total Traffic"] = (rawdf.loc[rowidx[0] + 1, "Bridges and Tunnels: Total Traffic"] +rawdf.loc[rowidx[0] + 2, "Bridges and Tunnels: Total Traffic"]+rawdf.loc[rowidx[0] + 3, "Bridges and Tunnels: Total Traffic"])/3
    
    
    rawdf.loc[rowidx[0], "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"] = "0%"
    #rawdf.loc[rowidx[1], "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"] = "0%"
    rawdf['Bridges and Tunnels: % of Comparable Pre-Pandemic Day'] = rawdf['Bridges and Tunnels: % of Comparable Pre-Pandemic Day'].str.rstrip('%').astype('float') / 100.0
    #rawdf.loc[rowidx[1], "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"] = (rawdf.loc[rowidx[1] + 1, "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"] +rawdf.loc[rowidx[1] + 2, "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"]+rawdf.loc[rowidx[1] + 3, "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"])/3
    rawdf.loc[rowidx[0], "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"] = (rawdf.loc[rowidx[0] + 1, "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"] +rawdf.loc[rowidx[0] + 2, "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"]+rawdf.loc[rowidx[0] + 3, "Bridges and Tunnels: % of Comparable Pre-Pandemic Day"])/3





tabledf = rawdf

# rawdf = rawdf.fillna(0)

tabledf = tabledf[['Date', 'Subways: Total Estimated Ridership','Buses: Total Estimated Ridership','LIRR: Total Estimated Ridership',\
       'Metro-North: Total Estimated Ridership','Access-A-Ride: Total Scheduled Trips','Bridges and Tunnels: Total Traffic']]

tabledf.columns = ['Date', 'Subway Ridership','Bus Ridership','LIRR Ridership','Metro-North Ridership','Access-A-Ride Trips','MTA Bridges and Tunnels Traffic']

ridershipCol = ['Subway Ridership','Bus Ridership','LIRR Ridership','Metro-North Ridership','Access-A-Ride Trips','MTA Bridges and Tunnels Traffic']
    
percentCol = ["Subway Percent Change", "Bus Percent Change", "LIRR Percent Change", "MNR Percent Change", \
              "Access-A-Ride Percent Change", "MTA Bridges and Tunnels Traffic Percent Change"]
    
tabledf[ridershipCol] = tabledf[ridershipCol].fillna(0)
    
    
tabledf[ridershipCol] = tabledf[ridershipCol].astype(int)
           
           
tabledf['Dates'] = pd.to_datetime(tabledf['Date'], format='%m/%d/%Y')

tabledf['DayofWeek'] = tabledf['Dates'].dt.dayofweek
tabledf['Weekday'] = np.where(tabledf['DayofWeek'].isin([0,1,2,3,4]), "Weekday", "Weekend")

#startDate = pd.to_datetime("03/09/2020", format='%m/%d/%Y')

tabledf["weekOrder"] = np.nan
for i in range(0, tabledf.shape[0]):
    if tabledf.loc[i, "Dates"]<= pd.to_datetime("01/03/2021", format='%m/%d/%Y'):
        tabledf.loc[i, "weekOrder"] = tabledf.loc[i, "Dates"].isocalendar()[1] - 9
    else:
        tabledf.loc[i, "weekOrder"] = tabledf.loc[i, "Dates"].isocalendar()[1] + 44
    
tabledf["daySum"] = 1   
weekdaydf = tabledf.groupby(['weekOrder', 'Weekday'], as_index=False).agg({'Date': 'last','Dates': 'last', 'daySum': 'sum', 'Subway Ridership': 'sum', \
                                                                           'Bus Ridership': 'sum', 'LIRR Ridership': 'sum', \
                                                                           'Metro-North Ridership': 'sum', 'Access-A-Ride Trips': 'sum', \
                                                                           'MTA Bridges and Tunnels Traffic': 'sum'})


weekdaydf = weekdaydf.loc[((weekdaydf["daySum"]==2) & (weekdaydf["Weekday"]=="Weekend")) | \
                          ((weekdaydf["daySum"]==5) & (weekdaydf["Weekday"]=="Weekday"))]

for i in range(0, len(ridershipCol)):
    weekdaydf[percentCol[i]] = weekdaydf[ridershipCol[i]].pct_change(periods=2)  

    
#weekdaydf[percentCol] = weekdaydf[percentCol].fillna(0)

weekdaydf = weekdaydf.replace([np.inf, -np.inf], np.nan)

weekdaydf["Week"] = [("Week of "  + x) for x in weekdaydf["Date"]]

weekdaydf["Period"] = np.where(weekdaydf["Dates"] < pd.to_datetime("01/01/2021", format='%m/%d/%Y'),"2020", np.where(weekdaydf["Dates"] < pd.to_datetime("01/01/2022", format='%m/%d/%Y'), "2021", "2022"))
    
weekdaydf.drop('Dates', axis=1, inplace=True)


#weekdaydf["Week"] = [("Week of "  + x[:-5]) for x in weekdaydf["Date"]]

# weekList = []

# for i in range(0, int(weekdaydf.weekOrder.max()) + 1):
#     if weekdaydf[weekdaydf.weekOrder == i].shape[0] ==2:
#         weekList.append(i)




wks = sheet[0]
print("-----------------First Sheet Accessed----------")

wks.set_dataframe(weekdaydf,(1,1))
print("-----------------Data Updated------------------")


rawdf['Dates'] = pd.to_datetime(rawdf['Date'], format='%m/%d/%Y')
rawdf["Period"] = np.where(rawdf["Dates"] < pd.to_datetime("01/01/2021", format='%m/%d/%Y'),"2020", np.where(rawdf["Dates"] < pd.to_datetime("01/01/2022", format='%m/%d/%Y'),"2021","2022"))

wks = sheet[1]
print("-----------------Second Sheet Accessed----------")

wks.set_dataframe(rawdf,(1,1))
print("-----------------Data Updated------------------")