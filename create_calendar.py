from datetime import datetime, timedelta
from cal_setup import get_google_cal



def main():
    service = get_google_cal()
    title = ("Title of the Event: ")
    calendar = { 
        'summary': title,
        'timeZone': 'America/Los_Angeles' 
    }
    
    created_calendar = service.calendars().insert(body='calendar').execute()
    
    print(created_calendar['id'])


if __name__ == "__main__":
    main()