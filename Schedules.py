from typing import Tuple
import datetime
from Managers import ColorManager


class ConflictingScheduleError(Exception):
    """
    If this error is thrown, either the schedule entered is invalid or it coincides with
    a previously entered schedule.
    """
    pass


class Schedules:
    used_slot = []
    used_colors = []

    def __init__(self, name: str, day: int, start_time: datetime.time,
                 end_time: datetime.time, is_shifted: bool, color: Tuple[int, int, int]):
        """Construct a new Schedule

        :param name: Name of new schedule
        :param day: Day when schedule takes place
        :param start_time: Time when schedule begins
        :param end_time: Time when schedule ends
        :param is_shifted: Checks if the schedule has been shifted.
        If so, there is no need to check for Conflicting Schedules.
        """
        if Schedules.schedule_conflict(day, start_time, end_time) and not is_shifted:
            raise ConflictingScheduleError
        self.name = name
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.color = color

    @classmethod
    def generate_color(cls) -> Tuple[int, int, int]:
        """Generate a color for the schedule

        :return: color used to represent schedule
        """
        possible_color = ColorManager.random_color()
        while possible_color in cls.used_colors:
            possible_color = ColorManager.random_color()
        return possible_color

    @classmethod
    def schedule_conflict(cls, day: int, start_time: datetime.time, end_time: datetime.time) -> bool:
        """Checks if there is a conflict with a previously entered Schedule
        or if the end time if before start time

        :param day: representing day of schedule
        :param start_time: representing start time of schedule
        :param end_time: end time of schedule
        :return: if schedule conflicts or not
        """
        if start_time >= end_time:
            return True
        else:
            for schedule in cls.used_slot:
                conflict_time = not (end_time <= schedule[1] or start_time >= schedule[2])
                if day == schedule[0] and conflict_time:
                    return True

            cls.used_slot.append((day, start_time, end_time))
            return False
