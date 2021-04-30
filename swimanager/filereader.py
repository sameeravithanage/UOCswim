import json
from pathlib import Path
import os
import gspread
import time
import re
from oauth2client.service_account import ServiceAccountCredentials
from swimanager.drivemeet import eventreader



def readfile(file_name):
    filename = file_name + '.json'
    with open('swimanager/meet_data/'+filename) as f:
        data = json.load(f)
        return data

def filewriter(path,data):
    with open(path,'w') as outfile:
        json.dump(data, outfile,indent=4)

def eventLister(stat,mtype):
        if stat == True:
                events = eventreader(mtype)
        else:
                events = {}
        return events
