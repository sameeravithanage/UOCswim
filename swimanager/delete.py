import gspread
from oauth2client.service_account import ServiceAccountCredentials

def file_creator(name):
	scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

	credentials = ServiceAccountCredentials.from_json_keyfile_name('swimanager/swimanager.json', scope)

	gc = gspread.authorize(credentials)

	sh = gc.create(name)
	sh.share('uocswimmingteam@gmail.com', perm_type='user', role='writer')
