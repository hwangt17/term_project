from datetime import datetime, timedelta
from cal_setup import get_google_cal


def main():
    # creates one hour event tomorrow 10 AM IST
    service = get_google_cal()

    d = datetime.now().date()
    tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
    start = tomorrow.isoformat()
    end = (tomorrow + timedelta(hours=1)).isoformat()
    title = input("Enter Event Title: ")

    # Calendar Parameter
    calendar = { 
        'summary': title,
        'timeZone': 'America/Los_Angeles' 
    }

    # Event Parameter
    event = {
        "summary": title,
        "description": 'This is a tutorial example of automating google calendar with python',
        "start": {"dateTime": start, "timeZone": 'Asia/Seoul'},
        "end": {"dateTime": end, "timeZone": 'Asia/Seoul'},
        "recurrence": [
        'RRULE:FREQ=DAILY;COUNT=2'
        ]
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