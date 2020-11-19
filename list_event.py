from datetime import datetime, timedelta
from cal_setup import get_google_cal
from tzlocal import get_localzone

def main():
    service = get_google_cal() # Call the Calendar API
    local_tz = get_localzone() # Call the Local Timezone

    now = datetime.utcnow() # Get the datetime now in UTC Timezone

    # Precondition: Events are planned for starting the day after 'now'.
    # Start of the day (07:00:00) and the end of the day (23:00:00)       
    beginning = datetime(now.year, now.month, now.day, 7).astimezone(local_tz)+timedelta(days=1) # Start of the day is 07:00:00 tomorrow 
    beginning_format = beginning.isoformat() # Format for Google Calendar API
    ending = datetime(now.year, now.month, now.day, 23).astimezone(local_tz)+timedelta(days=1) # End of the day is 23:00:00 tomorrow.
    ending_format = ending.isoformat() # Format for Google Calendar API
    print(beginning_format)
    print(ending_format)

    # Get list of calendars
    cal_ids = list()
    page_token = None
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    calendars = calendar_list.get('items', [])
    for calendar in calendars:
        cal_ids.append(calendar['id'])
    print(cal_ids)
    # Getting list of events 
    print('Getting List Events')
    for cal_id in cal_ids:
        events_result = service.events().list(
            calendarId=cal_id, timeMin=beginning_format, timeMax=ending_format,
            timeZone=local_tz, maxResults=1000, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

    # Print list of events in the calendar
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        print(start, end, event['summary'])

if __name__ == '__main__':
    main()