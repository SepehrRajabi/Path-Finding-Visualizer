from enum import Enum, auto


class Colors:
    RED: tuple[int, int, int] = (255, 0, 0)
    GREEN: tuple[int, int, int] = (0, 255, 0)
    BLUE: tuple[int, int, int] = (0, 0, 255)
    YELLOW: tuple[int, int, int] = (255, 255, 0)
    WHITE: tuple[int, int, int] = (255, 255, 255)
    BLACK: tuple[int, int, int] = (0, 0, 0)
    PURPLE: tuple[int, int, int] = (128, 0, 128)
    ORANGE: tuple[int, int, int] = (255, 165, 0)
    TURQUOISE: tuple[int, int, int] = (64, 224, 208)
    GREY: tuple[int, int, int] = (128, 128, 128)


class NodeState(Enum):
    EMPTY = auto()
    START = auto()
    END = auto()
    OBSTACLE = auto()
    VISITED = auto()
    PATH = auto()


STATE_COLORS: dict[NodeState, tuple[int, int, int]] = {
    NodeState.EMPTY: Colors.WHITE,
    NodeState.START: Colors.GREEN,
    NodeState.END: Colors.RED,
    NodeState.OBSTACLE: Colors.BLACK,
    NodeState.VISITED: Colors.BLUE,
    NodeState.PATH: Colors.PURPLE,
}


RESOLUTION: tuple[int, int] = (885, 885)
CELL_WIDTH: int = 20
CELL_HEIGHT: int = 20
MARGIN: int = 2
TOTAL_ROWS: int = 40
TOTAL_COLUMNS: int = 40
