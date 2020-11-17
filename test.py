class event:

    def __init__(self, summary=None, duration=0, timing=None, recurrance=[1,2,3,4,5,6,7]):
        self.summary = summary
        self.duration = duration
        self.timing = timing
        self.recurrance = recurrance

    def __str__(self):
        print(f'You have generated an event: {self.summary}, {self.recurrance} times.\nFor {self.duration} minutes at {self.timing}(s) this week.')
        


def main():
    user_summary = str(input("Title of event >> "))
    user_duration = int(input("How long will it be in minutes(please input integers only) >> "))
    user_timing = str(input("Morning or Afternoon >> "))
    user_recurrance = int(input("Please set the frequency (any frequency from 1 to 7) >> "))


    arthur = event(user_summary, user_duration, user_timing, user_recurrance)
    print(arthur)


if __name__ == "__main__":
    main()
        