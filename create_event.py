from datetime import datetime, timedelta
from cal_setup import get_google_cal
from tzlocal import get_localzone
import check_available

def create_calendar(service, title):
    """
    Create an calendar with the same name as the new event.
    """
    local_tz = get_localzone() # Call the Local Timezone
    local_timezone = str(local_tz) # Convert to string
    
    # Calendar Parameter
    calendar = {
        'summary': title,
        'timeZone': local_timezone
    }

    # Create Calendar
    created_calendar = service.calendars().insert(body=calendar).execute()
    return created_calendar['id']

def create_event(service, cal_id, title, frequency, length):
    """
    Create event.
    """
    local_tz = get_localzone() # Call the Local Timezone
    local_timezone = str(local_tz) # Convert to string 

    checked = check_available.check_vacancy(int(length),1)
    available_start = checked[0]
    available_end = checked[1]

    start = (available_start + timedelta(minutes=15)).isoformat()
    end = (available_start + timedelta(minutes=(15+int(length)))).isoformat()

    # Event Parameter
    event = {
        "summary": title,
        "start": {"dateTime": start, 'timeZone': local_timezone},
        "end": {"dateTime": end, 'timeZone': local_timezone}
    }
    
    # Create Event
    create_event = service.events().insert(calendarId=cal_id, body=event).execute()   

    # Print on Terminal
    print("created calendar")
    print("calendar id: ", cal_id)
    print("created event")
    print("event id: ", create_event['id'])
    print("summary: ", create_event['summary'])
    print("starts at: ", create_event['start']['dateTime'])
    print("ends at: ", create_event['end']['dateTime'])
    print("calendar link: ", create_event.get('htmlLink'))


def main():
    service = get_google_cal()

    title = input("Enter Event Title: ")
    frequency = input("How many times a week: ")
    length = input("How long do you want the event to be? Enter in minutes: ")
    cal_id = create_calendar(service, title)

    create_event(service, cal_id, title, frequency, length)

if __name__ == '__main__':
    main()