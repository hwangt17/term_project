from datetime import datetime, timedelta
from cal_setup import get_google_cal
from tzlocal import get_localzone
from list_event import get_list_event
import create_event 
from tzlocal import get_localzone

def store_events(count):
    """
    This function reads the user's schedule for a given day, detecting start and end time of each event. 
    """
    store_event = dict()
    event_vessel = list()
    events = get_list_event(count)
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
    return index_events

def check_vacancy(duration,count):
    """
    Check vacant time block of a given duration.
    """
    local_tz = get_localzone() # Call the Local Timezone
    vacant_times = {}
    events = store_events(count)

    # List all vacant timeslots and it's duration in order.
    for i in range(len(events)+1):
        # from 7:00:00 to the start of first event.
        if i == 0: 
            end = events[i][0]
            start = datetime(end.year, end.month, end.day, 7).astimezone(local_tz)
        # from end of the last event to 23:00:00.
        elif i >= len(events):
            start = events[i-1][1]
            end = events[i] = datetime(start.year, start.month, start.day, 23).astimezone(local_tz)
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

def main():
    print(check_vacancy(60,1))

if __name__ == '__main__':
    main()