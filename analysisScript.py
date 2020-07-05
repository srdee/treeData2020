import pandas as pd
import pytz
import datetime as dt
import sys

loadFile = sys.argv[1]
tiltFile = sys.argv[2]

dfLoads = pd.read_csv(loadFile , parse_dates=True, infer_datetime_format=True)
dfTilts = pd.read_csv(tiltFile, skiprows = 22, parse_dates=True, infer_datetime_format=True)

#WORK WITH LOADS
#add column of seconds
dfLoads['ElapsedSeconds'] = dfLoads['Elapsed mS'].apply(lambda x:x/1000)

#create date object 
dfLoads['dateObject'] = dfLoads['Date'].apply(lambda x: dt.datetime.strptime("-".join(x.split('/')[::-1]), "%Y-%d-%m"))

#strip AM from Time by removing three characters from string, register as time
dfLoads['timeObject'] = dfLoads['Time'].apply(lambda x: dt.datetime.strptime(x[:-3], "%H:%M:%S"))

#create dateTime object that can be manipulated
dfLoads['dateTimeObject'] = dfLoads.apply(lambda x: dt.datetime.combine(x.dateObject, x.timeObject.time()), axis=1)

#WORK WITH TILTS
#Find mode
dfTilts['tiltMode160ch5'] = dfTilts['12160:ch5'].apply(lambda x: dfTilts['12160:ch5'].mode())

#OUTPUT DATA
#write excel file with different dataframes on different sheets
dfs = {'Loads':dfLoads, 'Tilts':dfTilts}
writer = pd.ExcelWriter(loadFile[:-4] + tiltFile[:-4] +'.xlsx', engine='xlsxwriter')

for sheet_name in dfs.keys():
    dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    
writer.save()

print('File ' + loadFile[:-4] + tiltFile[:-4] +'.xlsx' + ' successfully created')





#NOTES FOR LATER:

#to replace missing values
#.fillna(new_value)

## Delete the "Area" column from the dataframe
#data = data.drop("Area", axis=1)

## Rename multiple columns in one go with a larger dictionary
#data.rename(
  #  columns={
       #    #    #     "Area": "place_name",
       #    #    #    #     "Y2001": "year_2001"
     #    #   },
     #   inplace=True
# )   

