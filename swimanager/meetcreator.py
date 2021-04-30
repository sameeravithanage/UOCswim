import json,os
import datetime
from swimanager.drivemeet import file_creator
from swimanager.filereader import readfile

def convert(tup, di): 
	for a, b in tup: 
		di.setdefault(a, b) 
	return di 

def arraycreator(entered):
	teams = ['ucsc', 'med', 'sci', 'mgt', 'tech', 'nur', 'sri', 'law', 'art']
	teams_set = list(zip(teams, entered))
	dic = {}
	final_teams = convert(teams_set, dic)
	return final_teams

def createfile(name, startdate, location, boysteams, girlsteams):
	meta_data = readfile('meets')
	now = datetime.datetime.now()
	now = str(now)
	date=now.split('-')
	meetname = name
	meetdate = date[0]

	count = meta_data['count']
	count += 1
	meta_data['count'] = count

	sheetname = str(count)+' Entries '+meetname+' '+meetdate

	data = {}
	meta_new = {}
	meta_new['meetid'] = data['meetid'] = count
	meta_new['meetype'] = data['meettype'] = name
	data['time_created'] = now
	meta_new['startdate'] = data['startdate'] = str(startdate)
	meta_new['location'] = data['location'] = location
	data['boys'] = boysteams
	data['girls'] = girlsteams
	data['sheetname'] = sheetname
	data['eventstat'] = False
	data['eventid'] = ''

	if name == 'IF':
		meta_new['meettitle'] = data['meettitle'] = 'Inter Faculty Swimming Championship - ' + meetdate
		meta_new['shortname'] = data['shortname'] = 'Inter-Fac' + meetdate
		meta_new['image'] = data['image'] = 'images/IF.jpg'
	else:
		meta_new['meettitle'] = data['meettitle'] = 'Inter Faculty Freshers\' Swimming Championship - ' + meetdate
		meta_new['shortname'] = data['shortname'] = 'Inter-Fac Freshers\'' + meetdate
		meta_new['image'] = data['image'] = 'images/IFF.jpeg'


	meta_new['meet'] = False
	meta_data['meets'][count] = meta_new

	# publish details update
	# pub_data = readfile('publish')
	data['pub_settings'] = {
		'events': False,
		'meet': False,
		'results': {
			'boys': [],
			'girls': []
		}
	}

	# pub_data[count] = pub_settings

	# with open('swimanager/meet_data/publish.json','w') as outfile:
	# 	json.dump(pub_data, outfile,indent=4)

	# create the meet folders needed
	if not os.path.exists("swimanager/meet_data/entries/"+str(count)):
			os.makedirs("swimanager/meet_data/entries/"+str(count))

	if not os.path.exists("swimanager/meet_data/publish/"+str(count)):
			os.makedirs("swimanager/meet_data/publish/"+str(count))

	if not os.path.exists("swimanager/meet_data/publish/"+str(count)+"/events"):
			os.makedirs("swimanager/meet_data/publish/"+str(count)+"/events")

	if not os.path.exists("swimanager/meet_data/publish/"+str(count)+"/results"):
			os.makedirs("swimanager/meet_data/publish/"+str(count)+"/results")

	if not os.path.exists("swimanager/meet_data/results/"+str(count)):
			os.makedirs("swimanager/meet_data/results/"+str(count))

	file_creator(sheetname,meetname,boysteams,girlsteams,meta_data,data,count)