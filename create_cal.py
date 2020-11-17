from datetime import datetime, timedelta
from cal_setup import get_google_cal


def main():
   # creates one hour event tomorrow 10 AM IST
   google_cal = get_google_cal()

   d = datetime.now().date()
   tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
   start = tomorrow.isoformat()
   end = (tomorrow + timedelta(hours=1)).isoformat()

   create_event = google_cal.events().insert(calendarId='primary',
       body={
           "summary": 'Automating calendar',
           "description": 'This is a tutorial example of automating google calendar with python',
           "start": {"dateTime": start, "timeZone": 'Asia/Seoul'},
           "end": {"dateTime": end, "timeZone": 'Asia/Seoul'},
       }
   ).execute()

   print("created event")
   print("id: ", create_event['id'])
   print("summary: ", create_event['summary'])
   print("starts at: ", create_event['start']['dateTime'])
   print("ends at: ", create_event['end']['dateTime'])
   print("calendar link: ", create_event.get('htmlLink'))

if __name__ == '__main__':
   main()