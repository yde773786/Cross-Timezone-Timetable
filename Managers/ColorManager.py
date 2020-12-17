from typing import Tuple

all_colors = {'blue': (173, 216, 230),
              'green': (144, 238, 144),
              'brown': (195, 155, 119),
              'pink': (255, 182, 193),
              'yellow': (255, 255, 0),
              'orange': (255, 207, 158),
              'red': (202, 52, 51),
              'violet': (177, 156, 217),
              'gold': (212, 175, 55)}


def generate_rgb(str_color: str) -> Tuple[int, int, int]:
    """Generates the required rgb for the schedule's background

    :return: Tuple representing rgb of schedule's color
    """
    return all_colors[str_color]
