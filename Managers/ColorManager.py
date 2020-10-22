from typing import Tuple
from random import randint

all_colors = [(0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0),
              (0, 0, 0)]


def random_color() -> Tuple[int, int, int]:
    """Generates a random color for the schedule's background

    :return: Tuple representing rgb of schedule's color
    """
    return all_colors[randint(0, 29)]
