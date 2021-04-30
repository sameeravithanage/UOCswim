import json, yaml, os, shutil, gspread, time, re, glob, csv
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials
from swimanager.filereader import readfile,filewriter
from swimanager.drivemeet import sheet_deleter

import pprint

def meetfolder(meetid):
        my_file = Path("swimanager/meet_data/entries/"+str(meetid))
        if my_file.is_dir():
                data = {
                        'message':'',
                        'category':'light',
                        'file':True
                        }
                # open entry files if exists
                entry_file = Path('swimanager/meet_data/entries/'+str(meetid)+'/'+str(meetid)+'_men.json')
                if entry_file.is_file():
                        with open('swimanager/meet_data/entries/'+str(meetid)+'/'+str(meetid)+'_men.json') as json_file:  
                                men = json.load(json_file)
                        with open('swimanager/meet_data/entries/'+str(meetid)+'/'+str(meetid)+'_women.json') as json_file:  
                                women = json.load(json_file)
                else:
                        data = {
                                'message':'Please sync with drive to view entries',
                                'category':'info',
                                'file':False
                                }
                        men = {}
                        women = {}
        return data,men,women

def drivesync(meetid,sheetname):

        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name('swimanager/swimanager.json', scope)
        gc = gspread.authorize(credentials)
        sh = gc.open(sheetname)
        worksheet_list = sh.worksheets()
        menentries = []
        womenentries = []
        for i in worksheet_list:
            team = {}
            i = str(i)
            item = i.split()
            item[1] = item[1].replace("'","")
            worksheet = sh.worksheet(item[1])
            list_of_lists = worksheet.get_all_values()
            teamName = item[1]
            teamName = list(teamName)
            teamName[0] = teamName[0].upper()
            teamName = "".join(teamName)
            teamName = re.findall('[A-Z][^A-Z]*', teamName)
            team["Name"] = teamName[0]
            team["Gender"] = teamName[1]
            team["Events"] = list_of_lists[0]
            team["Entries"] = list_of_lists[1:]
            if teamName[1] == 'Men':
                    menentries.append(team)
            else:
                    womenentries.append(team)
        return menentries,womenentries

def event_organizer(data,gender,meetid):
        event_data = {}
        tmp = data[0]
        tmp = tmp["Events"]
        events = tmp[2:]
        for k in events:
                event_data[k] = []

        for teamData in data:
                for i in teamData["Entries"]:
                        entry = i[0:2]
                        team = teamData["Name"]
                        entry.append(team)
                        checklist = i[2:]
                        for ind,val in enumerate(checklist):
                                if val != '':
                                        event_data[events[ind]].append(entry)
        
        filewriter('swimanager/meet_data/entries/'+str(meetid)+'/'+str(meetid)+'_'+gender+'.json',event_data)

def statusUpdate(status,meetid):
        meet = readfile(meetid)
        # meet = data['meets'][meetid]

        meet[status] = True
        sheetname = str(meet['meetid']) + ' ' + meet['meettype'] + ' - Events'
        meet['eventsheet'] = sheetname

        files = glob.glob('swimanager/meet_data/entries/'+str(meetid)+'/*.json')       

        # create sheet here
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name('swimanager/swimanager.json', scope)
        gc = gspread.authorize(credentials)
                        
        if len(meet['eventid']) > 1:
                gc.del_spreadsheet(meet['eventid'])
                        	
        sh = gc.create(sheetname)
        sh.share('uocswimmingteam@gmail.com', perm_type='user', role='writer')
        sh = gc.open(sheetname)


        meet['eventid'] = sh.id
        # filename = file_name + '.json'
        filewriter('swimanager/meet_data/'+meetid+'.json',meet)
        
        for i in files:
                gender = i.split('_')
                gender = gender[-1]
                gender = gender.split('.')
                gender = gender[0]
                        
                with open(i) as json_file:  
                        data = json.load(json_file)
                        time.sleep(3)
                        header = [['Name','Reg No','Team','Time']]
                        for p in data:
                                # if data[p] == True:
                                event_data = header+data[p]
                                sh.add_worksheet(title=p+'-'+gender, rows="100", cols="20")
                                sh.values_update(p+'-'+gender+'!A1',params={'valueInputOption':'RAW'},body={'values': event_data})
        
        worksheet = sh.worksheet('Sheet1')
        sh.del_worksheet(worksheet)


def meet_publish(meetid):
        data = readfile('meets')
        meet = readfile(meetid)

        status = data['meets'][meetid]['meet']
        meet['pub_settings']['meet'] = data['meets'][meetid]['meet'] = not status

        filewriter('swimanager/meet_data/meets.json',data)
        filewriter('swimanager/meet_data/'+meetid+'.json',meet)
        
        return data['meets'][meetid]['meet']

def event_pub(meetid):
        src_files = os.listdir('swimanager/meet_data/entries/'+str(meetid))
        for file_name in src_files:
                full_file_name = os.path.join('swimanager/meet_data/entries/'+str(meetid), file_name)
                if os.path.isfile(full_file_name):
                        shutil.copy(full_file_name, 'swimanager/meet_data/publish/'+str(meetid)+'/events')

        data = readfile(meetid)
        status = data['pub_settings']['events']
        data['pub_settings']['events'] = not status

        filewriter('swimanager/meet_data/'+meetid+'.json',data)

        return data['pub_settings']['events']

def resultPull(meetid,sheet,event,gender):
        event_name = event+gender
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name('swimanager/swimanager.json', scope)
        gc = gspread.authorize(credentials)
        sh = gc.open_by_key(sheet)
        worksheet = sh.worksheet(event_name)
        result_list = worksheet.get_all_values()
        
        header = result_list[0]
        header.append("Place")
        result_list.pop(0)

        # time conversion
        for i in result_list:
                time_list = i[-1].split('.')
                i.append(time_list)
                if len(i[-1]) == 2:
                        miliseconds = int(i[-1][1])
                        seconds = int(i[-1][0])
                        sectomil = seconds*100
                        timemil = sectomil + miliseconds
                        i[-1] = str(timemil)
                elif len(i[-1]) == 3:
                        miliseconds = int(i[-1][2])
                        seconds = int(i[-1][1])
                        sectomil = seconds * 100
                        minutes = int(i[-1][0])
                        mintomil = minutes * 60 * 100 
                        timemil = mintomil + sectomil + miliseconds
                        i[-1] = str(timemil)
                else:
                        i[-1] = i[-1][0]
        
        footer = []
        times = []

        for i in result_list:
                if i[-1].isdigit():
                        times.append(i)
                else:
                        footer.append(i)
        
        # sorting of times
        times.sort(key=lambda x: int(x[-1]))

        # adding places to times array
        place = 1
        for i in times:
                i[-1] = place
                place += 1

        result_list = times + footer
        result_list.insert(0,header)

        # write file to results folder
        with open('swimanager/meet_data/results/'+meetid+'/'+event_name+'.csv', 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(result_list)

        return result_list

def saved_results(meetid,events):
        files = os.listdir('swimanager/meet_data/results/'+meetid)
        data = {
                'men':{},
                'women':{}
        }
        for i in files:
                with open('swimanager/meet_data/results/'+meetid+'/'+i) as csvfile:
                        readCSV = csv.reader(csvfile, delimiter=',')
                        result_data = []
                        next(readCSV)
                        for row in readCSV:
                                result_data.append(row)
                evt_list = i.split('-')
                event = evt_list[0]
                gender_list = evt_list[1].split('.')
                gender = gender_list[0]
                data[gender][event] = result_data
        return(data)

def result_publisher(meetid,event,gender):

        if gender =='-men':
                gen = 'boys'
        else:
                gen = 'girls'

        data = readfile(meetid)
        if event not in data['pub_settings']['results'][gen]:
                data['pub_settings']['results'][gen].insert(0,event)
                status = 'Published!'
        else:
                data['pub_settings']['results'][gen].remove(event)
                status ='Unpublished'

        shutil.copy('swimanager/meet_data/results/'+meetid+'/'+event+gender+'.csv', 'swimanager/meet_data/publish/'+meetid+'/results/'+event+gender+'.csv')

        filewriter('swimanager/meet_data/'+meetid+'.json',data)
        return status

def delete_meet(meetid):

        # delete meet folder in publish
        dirpath = os.path.join('swimanager/meet_data/publish', meetid)
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
                shutil.rmtree(dirpath, ignore_errors=True)

        # remove entries folder
        dirpath = os.path.join('swimanager/meet_data/entries', meetid)
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
                shutil.rmtree(dirpath, ignore_errors=True)

        # remove results folder
        dirpath = os.path.join('swimanager/meet_data/results', meetid)
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
                shutil.rmtree(dirpath, ignore_errors=True)

        # remove drive sheets
        data = readfile(meetid)
        sheet_deleter(data['entryid'],data['eventid']) 
        try:
                os.remove('swimanager/meet_data/'+meetid+'.json')
        except:
                print("Not able to delete the file %s" % filename)


        # delete meet from file
        meets_data = readfile('meets')
        del meets_data['meets'][meetid]
        filewriter('swimanager/meet_data/meets.json',meets_data)
        

def view_res(meetid):
        pub_res = readfile(meetid)
        meet = pub_res['pub_settings']

        # get the published entries
        if meet['events']:
                with open('swimanager/meet_data/publish/'+str(meetid)+'/events/'+str(meetid)+'_men.json') as json_file:  
                        men = json.load(json_file)
                with open('swimanager/meet_data/publish/'+str(meetid)+'/events/'+str(meetid)+'_women.json') as json_file:  
                        women = json.load(json_file)

                entries = [men,women]
        else:
                entries = []

        # get the published results
        data = {
                'men':{},
                'women':{}
        }
        genders = ['men','women']
        
        for g in genders:
                if g == 'men':
                        files = meet['results']['boys']
                else:
                        files = meet['results']['girls']
        
                for i in files:
                        filename = i + '-'+ g +'.csv'
                        # print(filename)
                        with open('swimanager/meet_data/publish/'+meetid+'/results/'+filename) as csvfile:
                                readCSV = csv.reader(csvfile, delimiter=',')
                                result_data = []
                                next(readCSV)
                                for row in readCSV:
                                        result_data.append(row)
                        data[g][i] = result_data
        return(meet,entries,data)

















