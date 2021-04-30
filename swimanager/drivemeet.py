import gspread
import json
import yaml
import time
from oauth2client.service_account import ServiceAccountCredentials

def eventreader(meet):
	with open("swimanager/meet_data/events.yaml", 'r') as stream:
		try:
			data = yaml.safe_load(stream)
			events = data[meet]
		except yaml.YAMLError as exc:
			print(exc)
			events = []
	return events

def sheetcreator(dict,sh,gc,gender,events):
	info = ["Name", "Reg no"]
	header = []
	details = info + events 
	header.append(details)
	for key, value in dict.items():
		if value == True:
			sh.add_worksheet(title=key+gender, rows="100", cols="20")
			sh.values_update(key+gender+'!A1',params={'valueInputOption':'RAW'},body={'values': header})



def file_creator(sheetname,name,men,women,metadata,data,count):
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

	credentials = ServiceAccountCredentials.from_json_keyfile_name('swimanager/swimanager.json', scope)
	gc = gspread.authorize(credentials)

	# print(metadata)
	# print(data)
	
	# create a new google sheet
	sh = gc.create(sheetname)
	sh.share('uocswimmingteam@gmail.com', perm_type='user', role='writer')
	sh = gc.open(sheetname)
	
	data['entryid'] = sh.id

	with open('swimanager/meet_data/'+str(count)+'.json','w') as outfile:
		json.dump(data, outfile,indent=4)
	with open('swimanager/meet_data/meets.json','w') as outfile:
		json.dump(metadata, outfile,indent=4)

	
	# check for meet type and return entries
	events = eventreader(name)
	maleevents = events["boys"]
	femaleevents = events["girls"]

	#add new sheets to the worksheets based on the faculties entered 
	genderm = 'Men'
	genderf = 'Women'
	
	time.sleep(5)
	
	sheetcreator(men,sh,gc,genderm,maleevents)
	sheetcreator(women,sh,gc,genderf,femaleevents)
	
	worksheet = sh.worksheet('Sheet1')
	sh.del_worksheet(worksheet)

def sheet_deleter(entry,event):
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

	credentials = ServiceAccountCredentials.from_json_keyfile_name('swimanager/swimanager.json', scope)
	gc = gspread.authorize(credentials)

	gc.del_spreadsheet(entry)
	if len(event) > 1:
		gc.del_spreadsheet(event)



