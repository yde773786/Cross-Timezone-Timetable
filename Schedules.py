from typing import Tuple


class ConflictingScheduleError(Exception):
    pass


class Schedules:
    used_colors = []
    used_slot = []

    def __init__(self, name, day_offset, start_time, end_time):
        if Schedules.schedule_conflict(day_offset, start_time, end_time):
            raise ConflictingScheduleError
        self.name = name
        self.day_offset = day_offset
        self.start_time = start_time
        self.end_time = end_time
        self.color = Schedules.generate_color()

    @classmethod
    def generate_color(cls) -> Tuple[int, int, int]:
        return 0, 0, 0

    @classmethod
    def schedule_conflict(cls, day_offset, start_time, end_time) -> bool:
        return True
