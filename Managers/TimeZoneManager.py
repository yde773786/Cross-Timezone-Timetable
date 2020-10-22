import datetime
from typing import Tuple

all_timezones = ["UTC−12:00",
                 "UTC−11:00",
                 "UTC−10:00",
                 "UTC−09:30",
                 "UTC−09:00",
                 "UTC−08:00",
                 "UTC−07:00",
                 "UTC−06:00",
                 "UTC−05:00",
                 "UTC−04:00",
                 "UTC−03:30",
                 "UTC−03:00",
                 "UTC−02:00",
                 "UTC−01:00",
                 "UTC+00:00",
                 "UTC+01:00",
                 "UTC+02:00",
                 "UTC+03:00",
                 "UTC+03:30",
                 "UTC+04:00",
                 "UTC+04:30",
                 "UTC+05:00",
                 "UTC+05:30",
                 "UTC+05:45",
                 "UTC+06:00",
                 "UTC+06:30",
                 "UTC+07:00",
                 "UTC+08:00",
                 "UTC+08:45",
                 "UTC+09:00",
                 "UTC+09:30",
                 "UTC+10:00",
                 "UTC+10:30",
                 "UTC+11:00",
                 "UTC+12:00",
                 "UTC+12:45",
                 "UTC+13:00",
                 "UTC+14:00", ]


def shifted_time(current_tz: str, target_tz: str, current_time: datetime.time) -> Tuple[int, datetime.time]:
    """Returns the time provided shifted to that of the target timezone

    :param current_tz: The current time zone of the schedule
    :param target_tz: The target time zone of the schedule
    :param current_time: The current time slot
    :return: List with first element representing day
    (-1 if previous day, 0 if current day, 1 if next day)
    """
    current_tz_str = (current_tz.split('C')[1]).split(':')
    target_tz_str = (target_tz.split('C')[1]).split(':')
    time_to_shift_in_minutes = int(target_tz_str[0]) * 60 + int(target_tz_str[1]) - int(current_tz_str[0]) * 60 - int(current_tz_str[1])
    current_time_in_minutes = current_time.hour * 60 + current_time.minute
    shifted_time_in_minutes = current_time_in_minutes + time_to_shift_in_minutes
    shifted_hour = (shifted_time_in_minutes // 60) % 24
    shifted_min = shifted_time_in_minutes % 60
    day = shifted_time_in_minutes // 1440
    return day, datetime.time(shifted_hour, shifted_min)
