from typing import Callable, Optional

from .algorithms import AStarSearch, DijkstraSearch, BFSSearch, SearchAlgorithm
from .heuristics import Heuristic, ManhattanDistance, EuclideanDistance, ChebyshevDistance, ZeroHeuristic
from .grid import Grid, Node


class PathFinder:
    ALGORITHMS: list[SearchAlgorithm] = [
        AStarSearch(), DijkstraSearch(), BFSSearch()]
    HEURISTICS: list[Heuristic] = [
        ManhattanDistance(),
        EuclideanDistance(),
        ChebyshevDistance(),
        ZeroHeuristic(),
    ]

    def __init__(self) -> None:
        self._algorithm_index: int = 0
        self._heuristic_index: int = 0

    @property
    def algorithm(self) -> SearchAlgorithm:
        return self.ALGORITHMS[self._algorithm_index]

    @property
    def heuristic(self) -> Heuristic:
        return self.HEURISTICS[self._heuristic_index]

    def cycle_algorithm(self) -> None:
        self._algorithm_index = (
            self._algorithm_index + 1) % len(self.ALGORITHMS)

    def cycle_heuristic(self) -> None:
        self._heuristic_index = (
            self._heuristic_index + 1) % len(self.HEURISTICS)

    def run(
        self,
        grid: Grid,
        start: Node,
        end: Node,
        running_flag: dict[str, bool],
        on_visit: Optional[Callable[[], None]] = None,
    ) -> list[Node]:
        return self.algorithm.search(grid, start, end, self.heuristic, running_flag, on_visit)
