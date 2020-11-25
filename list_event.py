from datetime import datetime, timedelta
from cal_setup import get_google_cal
from tzlocal import get_localzone

def get_list_event(service, count, earliest, latest):
    """
    Get all events from all calendars.
    count: count of days (used for range)
    """
    local_tz = get_localzone() # Call the Local Timezone

    now = datetime.utcnow() # Get the datetime now in UTC Timezone
    # Precondition: Events are planned for starting the day after 'now'.
    # Start of the day (07:00:00) and the end of the day (23:00:00)       
    beginning = datetime(now.year, now.month, now.day, earliest).astimezone(local_tz)+timedelta(days=count) # Start of the day is 07:00:00 tomorrow 
    beginning_format = beginning.isoformat() # Format for Google Calendar API
    ending = datetime(now.year, now.month, now.day, latest).astimezone(local_tz)+timedelta(days=count) # End of the day is 23:00:00 tomorrow.
    ending_format = ending.isoformat() # Format for Google Calendar API
    # print(f'From: {beginning_format} \nTo: {ending_format}')

    # Get list of calendars
    cal_ids = list()
    page_token = None
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    calendars = calendar_list.get('items', [])
    for calendar in calendars:
        cal_ids.append(calendar['id'])
    # print(cal_ids)

    # Getting list of events from all calendars 
    events = list()
    for cal_id in cal_ids:
        events_result = service.events().list(
            calendarId=cal_id, timeMin=beginning_format, timeMax=ending_format,
            timeZone=local_tz, maxResults=1000, singleEvents=True,
            orderBy='startTime').execute()
        events.extend(events_result.get('items'))
    return events

def main():
    service = get_google_cal() # Call the Calendar API

    # Print on terminal
    events = get_list_event(service,3,7,23)
    print('Getting List Events')
    if not events:
        print('No upcoming events found.')

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        print([start, end, event['summary']])

if __name__ == '__main__':
    main()