from datetime import datetime, timedelta
from cal_setup import get_google_cal
from tzlocal import get_localzone
import list_event

def main():
    # creates one hour event tomorrow 10 AM IST
    service = get_google_cal()

    today = datetime.now().date()
    tomorrow = datetime(today.year, today.month, today.day, 10)+timedelta(days=1)
    start = tomorrow.isoformat()
    end = (tomorrow + timedelta(hours=1)).isoformat()
    title = input("Enter Event Title: ")
    frequency = input("How many times a week: ")
    local_tz = get_localzone() # Call the Local Timezone
    local_timezone = str(local_tz) # Convert to string

    # Calendar Parameter
    calendar = { 
        'summary': title,
        'timeZone': local_timezone
    }

    # Event Parameter
    event = {
        "summary": title,
        "start": {"dateTime": start, 'timeZone': local_timezone},
        "end": {"dateTime": end, 'timeZone': local_timezone}
    }
    
    # Create Calendar
    created_calendar = service.calendars().insert(body=calendar).execute()
    # Create Event
    create_event = service.events().insert(calendarId=created_calendar['id'], body=event).execute()
    
    # Print on Terminal
    print("created calendar")
    print("calendar id: ", created_calendar['id'])
    print("created event")
    print("event id: ", create_event['id'])
    print("summary: ", create_event['summary'])
    print("starts at: ", create_event['start']['dateTime'])
    print("ends at: ", create_event['end']['dateTime'])
    print("calendar link: ", create_event.get('htmlLink'))

if __name__ == '__main__':
    main()