import sys
import os
from typing import List
import csv
import Schedules
import datetime

home_path = os.getenv('HOME')
if home_path is None:
    home_path = os.getenv('HOMEPATH')

path_to_storage = ''
if sys.platform == 'linux':
    path_to_storage = home_path + '/.ctztt'
elif sys.platform == 'darwin':
    path_to_storage = home_path + '/Library/Application Support/ctztt'
elif sys.platform == 'win32':
    home_path.replace('\\', '/')
    path_to_storage = home_path + '/AppData/Local/ctztt'

file = 'ctztt.csv'
storage_csv = os.path.join(path_to_storage, file)


def write_csv(timetable: List[Schedules.Schedules]) -> None:
    """Save the timetable into the ctztt.csv file for later usage.

    :param timetable: list of Schedules that need to be saved as new timetable
    :return:None
    """

    with open(storage_csv, 'w') as csvfile:
        header = ['Name', 'Day', 'Start Time', 'End Time', 'Color']
        writer = csv.DictWriter(csvfile, fieldnames=header)

        writer.writeheader()
        for schedule in timetable:
            writer.writerow({'Name': schedule.name, 'Day': schedule.day,
                             'Start Time': schedule.start_time,
                             'End Time': schedule.end_time,
                             'Color': schedule.color})


if not os.path.exists(path_to_storage):
    os.mkdir(path_to_storage)
    write_csv([])


def create_schedule(row: list) -> Schedules.Schedules:
    """Create a schedule from a row in the ctztt.csv file

    :param row: the row of the ctztt file
    :return: The Schedule from the given row
    """
    return Schedules.Schedules(name=row[0], day=int(row[1]),
                               start_time=str_to_time(row[2]),
                               end_time=str_to_time(row[3]),
                               is_shifted=False, color=row[4])


def str_to_time(time_string: str) -> datetime.time:
    """Converts string entries of time into datetime.time

    :param time_string: string data
    :return: datetime.time version of the string
    """
    hm = time_string.split(":")
    return datetime.time(int(hm[0]), int(hm[1]))


def read_csv() -> List[Schedules.Schedules]:
    """Read the timetable that is saved in ctztt.csv file to display saved timetable

    :return:List of schedules from 'ctztt.csv'
    """
    with open(storage_csv) as csv_reader:
        reader = csv.reader(csv_reader)
        next(reader)

        timetable = [create_schedule(row) for row in reader]
        return timetable
