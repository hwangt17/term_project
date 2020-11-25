from datetime import datetime, timedelta
from cal_setup import get_google_cal
from tzlocal import get_localzone
from list_event import get_list_event
import create_event 

def check_vacancy(count):
    
    events = get_list_event(count)
    
    for event in events:
        start = str(event['start'].get('dateTime'))
        end = str(event['end'].get('dateTime'))

        # Get Time Only (start)
        if start == "None":
            pass
        else:
            no_isoformat_start = datetime.fromisoformat(start)
        
        # Get Time Only (end)
        if end == "None":
            pass
        else:
            no_isoformat_end = datetime.fromisoformat(end)
        
        elapsed = no_isoformat_end - no_isoformat_start
        print(elapsed)

def main():
    print(check_vacancy(1))

if __name__ == '__main__':
    main()