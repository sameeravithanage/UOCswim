from flask import render_template, url_for, flash, redirect, request, jsonify
from swimanager import app, db, bcrypt
from swimanager.forms import LoginForm, NewMeetForm
from swimanager.models import User
from flask_login import login_user, current_user, logout_user,login_required
from swimanager.meetcreator import createfile, arraycreator
from swimanager.filereader import readfile, eventLister
from swimanager.meethandler import meetfolder, drivesync,event_organizer,statusUpdate, resultPull, event_pub, saved_results,result_publisher, meet_publish, delete_meet, view_res


@app.route("/")
@app.route("/home")
def home():
    # pub_meets = readfile('publish')
    meets = readfile('meets')

    return render_template('home.html', meets=meets['meets'])

@app.route("/view_meet")
def view_meet():
    meetid = request.args.get('meet')
    pub,entries,results = view_res(meetid)
    
    meet = readfile(meetid)
    pools = readfile('pools')

    # get the meetid and find the relevant meet from the json file
    # meet = fulldata['meets'][meetid]
    meet['location'] = pools[meet['location']]['name']

    return render_template('view_meet.html', entries = entries, results = results, meet=meet)


@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data) 
            next_page = request.args.get('next')    
            flash(f'Welcome to SWIMANAGER UOC '+user.username+'!!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('admin'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title = 'Login', form = form)


@app.route("/admin", methods = ['GET', 'POST'])
@login_required
def admin():
    data = readfile('meets')
    pools = readfile('pools')
    for meetid,meet in data['meets'].items():
        location = meet['location']
        image_url = pools[location]['image']
        meet['image'] = image_url
        meet['location'] = pools[location]['name']

    return render_template('admin.html', title = 'Admin', meets = data['meets'])


@app.route("/createmeet", methods = ['GET', 'POST'])
@login_required
def createmeet():
    form = NewMeetForm()
    if form.validate_on_submit():
        name = form.meet_name.data
        startdate = form.start_date.data
        # enddate = form.end_date.data
        location = form.location.data
        # teams-boys
        ucscboys = form.ucscm.data
        medboys = form.medm.data
        sciboys = form.scim.data
        mgtboys = form.mgtm.data
        techboys = form.tecm.data
        nurboys = form.nurm.data
        sriboys = form.srim.data
        lawboys = form.lawm.data
        artboys = form.artm.data

        boys =[ucscboys, medboys, sciboys, mgtboys, techboys, nurboys, sriboys, lawboys, artboys]
        # teams-girls
        ucscgirls = form.ucscl.data
        medgirls = form.medl.data
        scigirls = form.scil.data
        mgtgirls = form.mgtl.data
        techgirls = form.tecl.data
        nurgirls = form.nurl.data
        srigirls = form.sril.data
        lawgirls = form.lawl.data
        artgirls = form.artl.data

        girls = [ucscgirls, medgirls, scigirls, mgtgirls, techgirls, nurgirls, srigirls, lawgirls, artgirls]

        boysteams = arraycreator(boys)
        girlsteams = arraycreator(girls)
        createfile(name, startdate, location, boysteams, girlsteams)
        flash(f'New Meet Created', 'success')
        return redirect(url_for('admin'))

    return render_template('createmeet.html', title = 'Create Meet', form = form)


@app.route("/meet", methods = ['GET', 'POST'])
@login_required
def meet():
    meetid = request.args.get('meet')
    meet = readfile(meetid)
    print(meet)

    # get the meetid and find the relevant meet from the json file
    
    # meet = fulldata['meets'][meetid]

    # check if entry folder is present and send a message
    data,men_ents,wmen_ents = meetfolder(meetid)
    flash(f''+data['message'], data['category'])

    ev_list = eventLister(data['file'],meet['meettype'])
    results = saved_results(meetid,ev_list)
    # get published results
    # pub_res_data = readfile('publish')
    # pub_res = pub_res_data[meetid]
    

    return render_template('meet.html', title = 'meet ' + str(meetid), meet= meet, men_ents = men_ents, wmen_ents = wmen_ents,file_status = data['file'],ev_list = ev_list,results = results)



@app.route("/entries", methods = ['GET', 'POST'])
@login_required
def entries():
    meetid = request.args.get('meet')

    meet = readfile(meetid)
    # meet = fulldata['meets'][meetid]

    men,wmen = drivesync(meetid,meet['sheetname'])
    event_organizer(men,'men',meetid)
    event_organizer(wmen,'women',meetid)
    
    return redirect(url_for('meet',meet=meetid))


@app.route("/meet_pub", methods = ['GET', 'POST'])
@login_required
def meet_pub():
    meetid = request.args.get('meet')
    
    status = meet_publish(meetid)
    if status:
        flash(f'Meet published!', 'success')
    else:
        flash(f'Meet unpublished!', 'info')
    
    return redirect(url_for('meet',meet=meetid))


@app.route("/events", methods = ['GET', 'POST'])
@login_required
def events():
    meetid = request.args.get('meet')
    statusUpdate('eventstat',meetid)
    flash(f'Event File Created on Drive', 'success')


    return redirect(url_for('meet',meet=meetid))

@app.route("/publish_events", methods = ['GET', 'POST'])
@login_required
def publish_events():
    meetid = request.args.get('meet')
    status = event_pub(meetid)

    if status:
        flash(f'Events published!', 'success')
    else:
        flash(f'Events unpublished!', 'info')

    return redirect(url_for('meet',meet=meetid))

@app.route("/process", methods = ['POST'])
def process():
    data = request.get_json()
    meetid = data['meetid']

    meet = readfile(meetid)
    # meet = fulldata['meets'][meetid]
    sheet = meet['eventid']

    results = resultPull(meetid,sheet,data['event'],data['gender'])
    return jsonify(results)

@app.route("/pub_res", methods = ['POST'])
def pub_res():
    data = request.get_json()
    status = result_publisher(data['meetid'],data['event'],data['gender'])
    return jsonify(status)

@app.route("/del_meet", methods = ['GET', 'POST'])
@login_required
def del_meet():
    meetid = request.args.get('meet')
    delete_meet(meetid)
    flash(f'Meet Deleted!', 'success')

    return redirect(url_for('admin'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

