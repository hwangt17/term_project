from flask import Flask, render_template, session, request, redirect, url_for, abort
from datetime import datetime, timedelta # Datetime
from tzlocal import get_localzone # Get local timezone
from check_available import vacancy_based_on_freq # Check available timeslot
from create_event import create_calendar, create_event # Create Calendar and Event
import webbrowser
import pickle
import os.path
import json
import httplib2
import random
from oauth2client import client
from googleapiclient.discovery import build, build_from_document
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/', methods=['POST','GET'])
def index():
    return render_template("index.html")

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'credentials.json',
        scope='https://www.googleapis.com/auth/calendar',
        redirect_uri=url_for('oauth2callback', _external=True))

    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('result'))

@app.route('/automate', methods=['POST','GET'])
def automate():
    return render_template("automate.html")

@app.route('/result', methods=['POST','GET'])
def result():
    if 'credentials' not in session:
        return redirect(url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        service = build('calendar', 'v3', http = http_auth)

        if request.method == 'POST':
            title = request.form['Task Name']
            length = request.form['Duration']
            frequency = request.form['Frequency']
            earliest_time = request.form['Earliest']
            latest_time = request.form['Latest']
            
            cal_id = create_calendar(service, title)

            vacant = vacancy_based_on_freq(service,int(length),int(frequency),int(earliest_time),int(latest_time))
            
            for index, value in vacant.items():
                available_start = vacant[index][0]
                start = (available_start + timedelta(minutes=15)).isoformat()
                end = (available_start + timedelta(minutes=(15+int(length)))).isoformat()
                result = create_event(service, cal_id, start, end, title, frequency, length)

        return render_template('result.html'), webbrowser.open_new_tab(result)

@app.route('/overview')
def overview():
    return render_template("overview.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(threaded=True, port=5000) 