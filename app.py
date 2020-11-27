from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta # Datetime
from cal_setup import get_google_cal # Access Google Acc
from tzlocal import get_localzone # Get local timezone
from check_available import vacancy_based_on_freq # Check available timeslot
from create_event import create_calendar, create_event # Create Calendar and Event
import webbrowser

import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/automate')
def automate():
    return render_template("automate.html")

@app.route('/result', methods=['POST','GET'])
def result():

    SCOPES = ['https://www.googleapis.com/auth/calendar']

    CREDENTIALS_FILE = 'credentials.json'

    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)

    creds = flow.run_console()

    service = build('calendar', 'v3', credentials=creds)

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

        return webbrowser.open_new_tab(service), render_template("result.html"), webbrowser.open_new_tab(result)

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