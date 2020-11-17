import datetime
from cal_setup import get_google_cal

def main():
    service = get_google_cal()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting List Events')
    events_result = service.events().list(
    calendarId='primary', timeMin=now,
        maxResults=1000, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        print(start, end, event['summary'])

if __name__ == '__main__':
    main()