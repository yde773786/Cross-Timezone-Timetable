from typing import Tuple

COLOR_QUEUE = [(173, 216, 230),
               (144, 238, 144),
               (195, 155, 119),
               (255, 182, 193),
               (255, 255, 0),
               (255, 207, 158),
               (202, 52, 51),
               (177, 156, 217),
               (212, 175, 55)]


def get_next_color() -> Tuple[int, int, int]:
    """Provides new color by using a circular queue

    :return: color required
    """
    color_req = COLOR_QUEUE.pop(0)
    COLOR_QUEUE.append(color_req)

    return color_req


def rotate_to_color(current: Tuple[int, int, int]) -> None:
    """Rotates the color queue till the color immediately after
    input is at start of queue.

    :param current: current schedule's color
    :return: None
    """
    while COLOR_QUEUE[-1] != current:
        get_next_color()
