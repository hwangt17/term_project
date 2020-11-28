from datetime import datetime, timedelta
from cal_setup import get_google_cal
from tzlocal import get_localzone
import list_event

class event:

    def __init__(self, summary='', duration=0, timing='', recurrance=[1,2,3,4,5,6,7], until=0):
        self.summary = summary
        self.duration = duration
        self.timing = timing
        self.recurrance = recurrance
        self.until = until

    def __str__(self):
        return (f'You have generated an event: {self.summary}, {self.recurrance} times.\nFor {self.duration} minutes at {self.timing}(s) for {self.until} days.')
    
    def generate_calendar(self):
        # creates one hour event tomorrow 10 AM IST
        service = get_google_cal()

        today = datetime.now().date()
        tomorrow = datetime(today.year, today.month, today.day, 10)+timedelta(days=1)
        start = tomorrow.isoformat()
        end = (tomorrow + timedelta(hours=1)).isoformat()
        local_tz = get_localzone()
        local_timezone = str(local_tz)

        # Calendar Parameter
        calendar = { 
            'summary': self.summary,
            'timeZone': local_timezone 
        }

        # Event Parameter
        event = {
            "summary": self.summary,
            "start": {"dateTime": start, "timeZone": local_timezone},
            "end": {"dateTime": end, "timeZone": local_timezone},
        }
    
        # Create Calendar
        created_calendar = service.calendars().insert(body=calendar).execute()
        # Create Event
        create_event = service.events().insert(calendarId=created_calendar['id'], body=event).execute()
        return f"Here's the calendar link: {create_event.get('htmlLink')}"

        

        
def main():
    user_summary = input("Title of event >> ")
    user_duration = int(input("How long will it be in minutes (please input integers only) >> "))
    user_timing = input("Morning or Afternoon (please input 'AM' or 'PM') >> ")
    user_recurrance = int(input("Please set the frequency (any frequency from 1 to 7) >> "))
    user_until = int(input("For how many days >> "))
    arthur = event(user_summary, user_duration, user_timing, user_recurrance, user_until)
    arthur.generate_calendar()
    print(arthur)
    print(arthur.generate_calendar())
    


if __name__ == "__main__":
    main()
        