"""
Schedule class and associated exceptions.
"""

import datetime
from typing import List
from Managers.ColorManager import get_next_color
from Managers.TimeManager import shifted_time


class ConflictingScheduleError(Exception):
    """
    If this error is thrown, the schedule coincides with
    a previously entered schedule.
    """
    pass


class EndBeforeStartError(Exception):
    """
    If this error is thrown, the end time is before the start time.
    """
    pass


class Schedules:
    used_slot = []

    def __init__(self, name: str, day: int, start_time: datetime.time,
                 end_time: datetime.time, is_shifted: bool,
                 color=None):
        """Construct a new Schedule

        :param name: Name of new schedule
        :param day: Day when schedule takes place
        :param start_time: Time when schedule begins
        :param end_time: Time when schedule ends
        :param is_shifted: Checks if the schedule has been shifted.
        If so, there is no need to check for Conflicting Schedules.
        """

        if not is_shifted:
            if Schedules.schedule_conflict(day, start_time, end_time):
                raise ConflictingScheduleError
            elif end_time < start_time:
                raise EndBeforeStartError

        self.name = name
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

        if color is not None:
            self.color = color
        else:
            self.color = get_next_color()

    def shift_schedules(self, current_tz: str, target_tz: str) -> List[object]:
        """Return a list of schedules at the target timezone that are equivalent to the input
         schedule in current timezone.

        :param current_tz: current timezone
        :param target_tz: target timezone
        :return: list of shifted schedules
        """
        shifted = shifted_time(current_tz, target_tz, self.start_time)
        shifted_start_day = self.day + shifted[0]
        shifted_start_time = shifted[1]
        shifted = shifted_time(current_tz, target_tz, self.end_time)
        shifted_end_day = self.day + shifted[0]
        shifted_end_time = shifted[1]

        schedule_shift_list = []
        current_start_time = shifted_start_time
        if shifted_start_day < shifted_end_day:
            current_day = shifted_start_day % 7
            schedule_shift_list.append(Schedules(self.name, current_day, current_start_time,
                                                 datetime.time(23, 59), True, self.color))
            current_start_time = datetime.time(0, 0)

        schedule_shift_list.append(Schedules(self.name, shifted_end_day % 7, current_start_time,
                                             shifted_end_time, True, self.color))

        return schedule_shift_list

    def clear_slot(self) -> None:
        """Clears calling schedule's slot to avoid ConflictingScheduleError
        when resetting

        :return: None"""
        free_slot = (self.day, self.start_time, self.end_time)
        self.__class__.used_slot.remove(free_slot)

    @classmethod
    def schedule_conflict(cls, day: int, start_time: datetime.time, end_time: datetime.time) -> bool:
        """Checks if there is a conflict with a previously entered Schedule

        :param day: representing day of schedule
        :param start_time: representing start time of schedule
        :param end_time: end time of schedule
        :return: if schedule conflicts or not
        """

        for schedule in cls.used_slot:
            conflict_time = not (end_time <= schedule[1] or start_time >= schedule[2])
            if day == schedule[0] and conflict_time:
                return True

        cls.used_slot.append((day, start_time, end_time))
        return False

    @classmethod
    def clear_used(cls):
        """Clears all the used_slots to avoid ConflictingScheduleError
        when resetting

        :return: None
        """
        cls.used_slot = []
