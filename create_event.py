from datetime import datetime, timedelta # Datetime
from cal_setup import get_google_cal # Access Google Acc
from tzlocal import get_localzone # Get local timezone
from check_available import vacancy_based_on_freq # Check available timeslot

def create_calendar(service, title, local_timezone):
    """
    Create an calendar with the same name as the new event.
    """
    # local_tz = get_localzone() # Call the Local Timezone
    # local_timezone = str(local_tz) # Convert to string
    
    # Calendar Parameter
    calendar = {
        'summary': title,
        'timeZone': local_timezone
    }

    # Create Calendar
    created_calendar = service.calendars().insert(body=calendar).execute()
    print("\nCreated Calendar:")
    print("calendar Title: ", title)
    return created_calendar['id']

def create_event(service, cal_id, start, end, title, count, length, local_timezone):
    """
    Create Event.
    """
    # local_tz = get_localzone() # Call the Local Timezone
    # local_timezone = str(local_tz) # Convert to string 

    # Event Parameter
    event = {
        "summary": title,
        "start": {"dateTime": start, 'timeZone': local_timezone},
        "end": {"dateTime": end, 'timeZone': local_timezone}
    }
    
    # Create Event
    create_event = service.events().insert(calendarId=cal_id, body=event).execute()   

    # Print on Terminal
    print("\nCreated Event:")
    print("event id: ", create_event['id'])
    print("summary: ", create_event['summary'])
    print("starts at: ", create_event['start']['dateTime'])
    print("ends at: ", create_event['end']['dateTime'])
    print("calendar link: ", create_event.get('htmlLink'))
    return create_event


def main():
    service = get_google_cal()

    title = input("Enter Event Title -> ")
    frequency = input("How many times a week -> ")
    length = input("How long do you want the event to be? Enter in minutes -> ")
    earliest_time = input("When do you want the events to start at the earliest? (Enter 0 ~ 23)-> ")
    latest_time = input("When do you want the events to end at the lastest? (Enter 0 ~ 23) -> ")
    print("-----------------------")
    cal_id = create_calendar(service, title)

    vacant = vacancy_based_on_freq(service,int(length),int(frequency),int(earliest_time),int(latest_time))
    for index, value in vacant.items():
        available_start = vacant[index][0]
        start = (available_start + timedelta(minutes=15)).isoformat()
        end = (available_start + timedelta(minutes=(15+int(length)))).isoformat()
        create_event(service, cal_id, start, end, title, frequency, length)

if __name__ == '__main__':
    main()