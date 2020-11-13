from typing import Tuple

all_colors = {'A': (0, 0, 0),
              'B': (0, 0, 0),
              'C': (0, 0, 0),
              'D': (0, 0, 0),
              'E': (0, 0, 0),
              'F': (0, 0, 0),
              'G': (0, 0, 0),
              'H': (0, 0, 0)}


def generate_rgb(str_color: str) -> Tuple[int, int, int]:
    """Generates the required rgb for the schedule's background

    :return: Tuple representing rgb of schedule's color
    """
    return all_colors[str_color]
