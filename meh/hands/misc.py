"""
Miscellaneous handlers.

* SheetsSync - Syncs google sheets data with the database
"""

import time

import gspread
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials

from attendanceapp.models import Person, Group
from meh.hand import BaseHandler


class SheetsSync(BaseHandler):
    """
    Syncs the member data located in google sheets with the database.
    
    We are designed to do this process on demand.
    This process will likely be scheduled to run automatically.
    """
    
    ids = ['sync']
    
    def __init__(self, path='credentials.json', url='https://docs.google.com/spreadsheets/d/1ACc_c67UGzhEs3M0a9XFuhQ8ltPV46mreeYqSFsTAB8', group='msuai') -> None:
        
        super().__init__(name="SheetsSync")
         
        self.creds_path = path  # Path to credentials file
        self.url = url  # URL to sheet
        self.group = group  # Group to add members to

        # Scope to work with:
        self.scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

        self.creds = None  # Service Account Credentials

    def start(self):
        """
        Loads necessary files necessary for sync.
        
        If the file 'credentials.json' is not present for us to load,
        then we raise an exception, and will not be started.
        """
        
        # Load credentials:
        
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", self.scope)

    def handle(self, data: bytes):
        """
        Gets the data from the google sheet,
        and adds any new members.
        
        :return: Number of people added
        :rtype: int
        """
        
        # Create a client to work with:
        
        client = gspread.authorize(self.creds)
        
        # Get the sheet data:
        
        sheet = client.open_by_url(self.url).sheet1
        
        # Convert into a dataframe:
        
        df = pd.DataFrame(pd.DataFrame(sheet.get_all_records()), columns=['Timestamp','First Name','Last Name','MSU Email'])
                
        # Check if group exists:

        group = None

        if Group.objects.filter(name__exact=self.group).count() == 0:
            
            # Create the new group:
            
            group = Group(name=self.group)
            group.save()
        
        else:

            # Get group to work with:
            
            group = Group.objects.get(name=self.group)
        
        # Get set of all people to work with:
        
        people = group.person_set.all()
        
        # Iterate over members in dataframe:
        
        num = 0

        for index, row in df.iterrows():
                        
            # Check the email:
            
            if people.filter(email__exact=row['MSU Email']).count() > 0:
                
                # Already present, no change
                
                continue
            
            # Parse the time, we need to do some conversions:
            
            temp_time = time.strptime(row['Timestamp'], "%m/%d/%Y %H:%M:%S")

            # Convert the time into something Django likes:
            
            final_time = time.strftime("%Y-%m-%d %H:%M:%S", temp_time)
            
            # Create a new person:
            
            inst = Person(group=group, join_date = final_time, 
                          name = row['First Name'] + " " + row['Last Name'],
                          email = row['MSU Email']
            )
            
            inst.save()

            num += 1

        return num
