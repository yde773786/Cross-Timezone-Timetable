import sys
import os
from typing import List
import Schedules

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

if not os.path.exists(path_to_storage):
    os.mkdir(path_to_storage)


def write_csv(timetable: List[Schedules]) -> None:
    """Save the timetable into the ctztt.csv file for later usage.

    :param timetable: list of Schedules that need to be saved as new timetable
    :return:None
    """
    pass


def read_csv() -> List[Schedules]:
    """Read the timetable that is saved in ctztt.csv file to display saved timetable

    :return:None
    """
    pass
