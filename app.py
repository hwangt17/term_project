from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta # Datetime
from cal_setup import get_google_cal # Access Google Acc
from tzlocal import get_localzone # Get local timezone
from check_available import vacancy_based_on_freq # Check available timeslot
from create_event import create_calendar, create_event # Create Calendar and Event

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/automate')
def automate():
    return render_template("automate.html")

@app.route('/overview')
def overview():
    return render_template("overview.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/404')
def error():
    return render_template("404.html")

# @app.route('/fillup', methods=['GET','POST'])
# def fillup():
#     service = get_google_cal()

#     title = input("Enter Event Title -> ")
#     frequency = input("How many times a week -> ")
#     length = input("How long do you want the event to be? Enter in minutes -> ")
#     earliest_time = input("When do you want the events to start at the earliest? (Enter 0 ~ 23)-> ")
#     latest_time = input("When do you want the events to end at the lastest? (Enter 0 ~ 23) -> ")
#     print("-----------------------")
#     cal_id = create_calendar(service, title)

#     vacant = vacancy_based_on_freq(service,int(length),int(frequency),int(earliest_time),int(latest_time))
#     for index, value in vacant.items():
#         available_start = vacant[index][0]
#         start = (available_start + timedelta(minutes=15)).isoformat()
#         end = (available_start + timedelta(minutes=(15+int(length)))).isoformat()
#         create_event(service, cal_id, start, end, title, frequency, length)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)