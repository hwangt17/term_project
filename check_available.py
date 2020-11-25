from datetime import datetime, timedelta
from cal_setup import get_google_cal
from tzlocal import get_localzone
from list_event import get_list_event
import create_event 

def store_events(count):
    """

    """
    store_event = dict()
    event_vessel = list()
    events = get_list_event(count)
    i = 1
    
    for event in events:
        start = (event['start'].get('dateTime'))
        end = (event['end'].get('dateTime'))

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
            store_event[f'event{i}'] = str(event_vessel)    
            i += 1 # event number
        event_vessel = [] # reset

        # elapsed = no_isoformat_end - no_isoformat_start
    return store_event

def main():
    print(store_events(1))

if __name__ == '__main__':
    main()