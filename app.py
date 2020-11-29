from flask import Flask, render_template, session, request, redirect, url_for, abort # Flask
from datetime import datetime, timedelta # Datetime
from tzlocal import get_localzone # Get local timezone
from check_available import vacancy_based_on_freq # Check available timeslot
from create_event import create_calendar, create_event # Create Calendar and Event
import webbrowser # To open new web tab

# Google Authentication 
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'new_credentials.json'

app = Flask(__name__)
app.secret_key = 'secret key'

def creds_dict(credentials):
  return { 'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

@app.route('/')
def index():
    local_tz = get_localzone() # Call the Local Timezone
    local_timezone = str(local_tz) # Convert to string 
    print(local_timezone)

    return render_template("index.html")          

@app.route('/auth')
def auth():
    flow = Flow.from_client_secrets_file(CREDENTIALS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    (auth_url, state) = flow.authorization_url(access_type='offline', include_granted_scopes='true')

    session['state'] = state

    return redirect(auth_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']

    flow = Flow.from_client_secrets_file(CREDENTIALS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_response = request.url
    if 'http:' in authorization_response:
        authorization_response = 'https:' + authorization_response[5:]
    flow.fetch_token(authorization_response=authorization_response)

    creds = flow.credentials
    session['creds'] = creds_dict(creds)

    return redirect(url_for('result'))  

@app.route('/automate', methods=['POST','GET'])
def automate():
    return render_template('automate.html')

@app.route('/result', methods=['POST','GET'])
def result():
    if 'creds' not in session:
        return redirect(url_for('auth'))
    creds = credentials.Credentials(**session['creds'])
    print(creds)
    service = build('calendar', 'v3', credentials=creds)

    # check available and create calendar/events
    if request.method == 'POST':
        title = request.form['Task Name']
        timezone = request.form['Timezone']
        length = request.form['Duration']
        frequency = request.form['Frequency']
        earliest_time = request.form['Earliest']
        latest_time = request.form['Latest']
            
        cal_id = create_calendar(service, title, timezone)

        vacant = vacancy_based_on_freq(service,int(length),int(frequency),int(earliest_time),int(latest_time),timezone)
            
        for index, value in vacant.items():
            available_start = vacant[index][0]
            start = (available_start + timedelta(minutes=15)).isoformat()
            end = (available_start + timedelta(minutes=(15+int(length)))).isoformat()
            result = create_event(service, cal_id, start, end, title, frequency, length, timezone)
            # session['result_link'] = str(result.get('htmlLink'))
    
    session['creds'] = creds_dict(creds)

    return render_template('result.html')

# @app.route('/result_link')
# def result_link():
#     link = session['result_link']
#     return redirect(link)

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
    app.run(threaded=True) 