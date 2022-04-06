import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
#AP scheduler Imports
from datetime import datetime
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"];
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope);

client = gspread.authorize(creds);

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1ACc_c67UGzhEs3M0a9XFuhQ8ltPV46mreeYqSFsTAB8").sheet1;
#out of sheet create a dataframe
df = pd.DataFrame(sheet.get_all_records());
#convert the dataframe to csv
df.to_csv("attendance.csv");


print(df)

newdf = pd.DataFrame(df, columns=['Timestamp','First Name','Last Name','MSU Email'])
newdf







