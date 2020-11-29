from datetime import datetime, timedelta # Datetime
from cal_setup import get_google_cal # Access Google Acc
from tzlocal import get_localzone # Get local timezone
from list_event import get_list_event # Get list of all events
import pytz

def store_events(service,count, earliest, latest):
    """
    This function reads the user's schedule for a given day, detecting start and end time of each event. 
    """
    store_event = dict()
    event_vessel = list()
    events = get_list_event(service,count,earliest,latest)
    i = 1
    
    for event in events:
        start = (event['start'].get('dateTime'))
        end = (event['end'].get('dateTime'))
        title = event['summary']

        # Get Time Only (start)
        if start == None:
            pass
        else:
            no_isoformat_start = datetime.fromisoformat(str(start))
            event_vessel.append(no_isoformat_start)

        # Get Time Only (end)
        if end == None:
            pass
        else:
            no_isoformat_end = datetime.fromisoformat(str(end))
            event_vessel.append(no_isoformat_end)

        if event_vessel == []:
            pass
        else:
            store_event[title] = (event_vessel)    
            i += 1 # event number
        event_vessel = [] # reset

    # Sort events in order
    sorted_values = sorted(store_event.values()) # Sort the values
    sorted_events = {}

    for i in sorted_values:
        for k in store_event.keys():
            if store_event[k] == i:
                sorted_events[k] = store_event[k]
                break
    
    # Index events
    index_events = {}
    for index, (key, (start, end)) in enumerate(sorted_events.items()):
        index_events[index] = (start, end)
    print("Indexing events in order...")
    return index_events

### BOTTLENECK! NEED FIXING ###
def check_vacancy(service,duration,count,earliest,latest, local_timezone):
    """
    Check vacant time block of a given duration.
    """
    local_tz = pytz.timezone(local_timezone) # Call the Local Timezone
    vacant_times = {}
    events = store_events(service,count,earliest,latest)
    
    # List all vacant timeslots and it's duration in order.
    for i in range(len(events)+1):
        # from 7:00:00 to the start of first event.
        if i == 0: 
            if not events:
                now = datetime.utcnow() # Get the datetime now in UTC Timezone
                start = datetime(now.year, now.month, now.day, earliest).astimezone(local_tz)+timedelta(days=count)
                end = datetime(now.year, now.month, now.day, latest).astimezone(local_tz)+timedelta(days=count)
            else:
                end = events[i][0]
                start = datetime(end.year, end.month, end.day, earliest).astimezone(local_tz)
        # from end of the last event to 23:00:00.
        elif i >= len(events):
            start = events[i-1][1]
            end = events[i] = datetime(start.year, start.month, start.day, latest).astimezone(local_tz)
        # inbetween events (end of the one to start of next).
        else:
            if events[i-1][1] == events[i][0]:
                pass
            else:
                start = events[i-1][1]
                end = events[i][0]
        length = end - start # length of each time block
        vacant_times[i+1] = (start, end, length)

    # Finds the vacant timeslot from the list of vacant timeslots that works with the duration set by the user.
    for index, (start,end,length) in vacant_times.items():
        if vacant_times[index][2] >= timedelta(seconds=(duration+30)*60):
            return vacant_times[index]
        else:
            pass

def vacancy_based_on_freq(service,duration,frequency,earliest,latest,local_timezone):
    """
    Check vacant timeslot with the user inputed duration for the frequency/week the user inputed.
    """
    result = {}
    week = 7
    for i in range(week):
        if check_vacancy(service,duration,i+1,earliest,latest,local_timezone) == None:
            print(f'No slots left on this date. Still {frequency} spots left in the week to fill.')
            pass
        else:
            result[i+1] = check_vacancy(service,duration,i+1,earliest,latest,local_timezone)
            frequency -= 1
            print(f'Yes! There is a timeslot! Now {frequency} spots left in the week.')
        if frequency == 0:
            break
    return result


def main():
    service = get_google_cal() # Call the Calendar API
    timezone = 'Asia/Seoul'
    
    vacant = vacancy_based_on_freq(service,60,2,7,23,timezone)
    for index, value in vacant.items():
        a = vacant[index][0]
        print(a)
    # print(check_vacancy(service,60,2,7,23))


if __name__ == '__main__':
    main()