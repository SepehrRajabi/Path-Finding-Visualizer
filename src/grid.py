import threading
from typing import Optional, List

from .constants import NodeState, STATE_COLORS


class Node:
    def __init__(self, row: int, column: int) -> None:
        self.row: int = row
        self.column: int = column
        self.neighbors: List[Node] = []
        self.parent: Optional[Node] = None
        self.state: NodeState = NodeState.EMPTY
        self.lock: threading.Lock = threading.Lock()

    @property
    def position(self) -> tuple[int, int]:
        return self.row, self.column

    @property
    def is_obstacle(self) -> bool:
        return self.state == NodeState.OBSTACLE

    @property
    def is_visited(self) -> bool:
        return self.state == NodeState.VISITED

    @property
    def color(self) -> tuple[int, int, int]:
        with self.lock:
            return STATE_COLORS[self.state]

    def set_state(self, state: NodeState) -> None:
        with self.lock:
            self.state = state

    def reset(self) -> None:
        with self.lock:
            self.state = NodeState.EMPTY
            self.parent = None
            self.neighbors = []


class Grid:
    def __init__(self, rows: int, columns: int) -> None:
        self.rows: int = rows
        self.columns: int = columns
        self.cells: List[List[Node]] = [
            [Node(r, c) for c in range(columns)] for r in range(rows)
        ]

    def __getitem__(self, index: int) -> List[Node]:
        return self.cells[index]

    def __iter__(self):
        for row in self.cells:
            yield from row

    def in_bounds(self, row: int, column: int) -> bool:
        return 0 <= row < self.rows and 0 <= column < self.columns

    def update_all_neighbors(self) -> None:
        directions: List[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for node in self:
            node.neighbors = []
            for dr, dc in directions:
                r, c = node.row + dr, node.column + dc
                if self.in_bounds(r, c) and not self.cells[r][c].is_obstacle:
                    node.neighbors.append(self.cells[r][c])

    def reset(self) -> None:
        self.cells = [
            [Node(r, c) for c in range(self.columns)] for r in range(self.rows)
        ]

    def reset_search(self) -> None:
        """Reset only visited/path nodes, keep obstacles and start/end."""
        for node in self:
            if node.state in (NodeState.VISITED, NodeState.PATH):
                node.reset()
            node.neighbors = []
