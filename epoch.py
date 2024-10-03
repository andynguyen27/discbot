from datetime import datetime

# Example datetime
def eptime(hour: int, minute: int, am_pm: str) -> str:

# Convert to epoch time
    if am_pm.upper() == "PM" and hour != 12:
        hour += 12
    elif am_pm.upper() == "AM" and hour == 12:
        hour = 0

    now = datetime.now()
    current_date = now.date()

    datetime_obj = datetime(
        current_date.year, current_date.month, current_date.day, hour, minute
    )

    formatted_time = (f"<t:{int(datetime_obj.timestamp())}:x>")
    # epoch_time = int(datetime_obj.timestamp())
    # return "<t:int(datetime_obj.timestamp()):t>"
    return formatted_time

# input_hour = input('Enter hours: ')
# input_minutes = input('Enter minutes: ')
# input_am_pm = input("Enter AM or PM: ")
# print(eptime(int(input_hour),int(input_minutes),input_am_pm))
# print(f"Epoch time: {eptime(10, 30, 'PM')}")