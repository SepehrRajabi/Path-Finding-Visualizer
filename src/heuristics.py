from abc import ABC, abstractmethod
from .grid import Node


class Heuristic(ABC):
    @abstractmethod
    def __call__(self, node_a: Node, node_b: Node) -> float:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class ManhattanDistance(Heuristic):
    @property
    def name(self) -> str:
        return "Manhattan"

    def __call__(self, node_a: Node, node_b: Node) -> float:
        x1, y1 = node_a.position
        x2, y2 = node_b.position
        return abs(x1 - x2) + abs(y1 - y2)


class EuclideanDistance(Heuristic):
    @property
    def name(self) -> str:
        return "Euclidean"

    def __call__(self, node_a: Node, node_b: Node) -> float:
        x1, y1 = node_a.position
        x2, y2 = node_b.position
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class ChebyshevDistance(Heuristic):
    @property
    def name(self) -> str:
        return "Chebyshev"

    def __call__(self, node_a: Node, node_b: Node) -> float:
        x1, y1 = node_a.position
        x2, y2 = node_b.position
        return max(abs(x1 - x2), abs(y1 - y2))


class ZeroHeuristic(Heuristic):
    """h(n) = 0 always. Turns A* into Dijkstra's algorithm."""

    @property
    def name(self) -> str:
        return "Zero (Dijkstra)"

    def __call__(self, node_a: Node, node_b: Node) -> float:
        return 0
