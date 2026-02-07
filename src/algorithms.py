from abc import ABC, abstractmethod
from typing import Callable, Optional

from .grid import Grid, Node
from .heuristics import Heuristic
from .constants import NodeState


class SearchAlgorithm(ABC):
    @abstractmethod
    def search(
        self,
        grid: Grid,
        start: Node,
        end: Node,
        heuristic: Heuristic,
        running_flag: dict[str, bool],
        on_visit: Optional[Callable[[], None]] = None,
    ) -> list[Node]:
        """
        Returns a list of nodes representing the path, or empty list if no path found.
        on_visit: optional callback called each time a node is visited (for animation).
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def reconstruct_path(self, start: Node, end: Node) -> list[Node]:
        path: list[Node] = []
        node: Optional[Node] = end
        while node is not None and node != start:
            path.append(node)
            node = node.parent
        path.append(start)
        path.reverse()
        return path


class AStarSearch(SearchAlgorithm):
    @property
    def name(self) -> str:
        return "A*"

    def search(
        self,
        grid: Grid,
        start: Node,
        end: Node,
        heuristic: Heuristic,
        running_flag: dict[str, bool],
        on_visit: Optional[Callable[[], None]] = None,
    ) -> list[Node]:
        g_score: dict[Node, float] = {node: float("inf") for node in grid}
        f_score: dict[Node, float] = {node: float("inf") for node in grid}

        g_score[start] = 0
        f_score[start] = heuristic(start, end)

        open_set: dict[Node, float] = {start: f_score[start]}

        while open_set and running_flag["active"]:
            current: Node = min(open_set, key=open_set.get)

            if current == end:
                return self.reconstruct_path(start, end)

            for neighbor in current.neighbors:
                if neighbor.is_visited:
                    continue

                tentative_g: float = g_score[current] + 1

                if tentative_g < g_score[neighbor]:
                    neighbor.parent = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, end)

                open_set[neighbor] = f_score[neighbor]

            current.set_state(NodeState.VISITED)
            open_set.pop(current)
            start.set_state(NodeState.START)

            if on_visit:
                on_visit()

        return []


class DijkstraSearch(SearchAlgorithm):
    """Dijkstra is just A* with h(n) = 0, but this is a standalone implementation."""

    @property
    def name(self) -> str:
        return "Dijkstra"

    def search(
        self,
        grid: Grid,
        start: Node,
        end: Node,
        heuristic: Heuristic,
        running_flag: dict[str, bool],
        on_visit: Optional[Callable[[], None]] = None,
    ) -> list[Node]:
        dist: dict[Node, float] = {node: float("inf") for node in grid}
        dist[start] = 0

        open_set: dict[Node, float] = {start: 0}

        while open_set and running_flag["active"]:
            current: Node = min(open_set, key=open_set.get)

            if current == end:
                return self.reconstruct_path(start, end)

            for neighbor in current.neighbors:
                if neighbor.is_visited:
                    continue

                tentative_dist: float = dist[current] + 1

                if tentative_dist < dist[neighbor]:
                    neighbor.parent = current
                    dist[neighbor] = tentative_dist

                open_set[neighbor] = dist[neighbor]

            current.set_state(NodeState.VISITED)
            open_set.pop(current)
            start.set_state(NodeState.START)

            if on_visit:
                on_visit()

        return []


class BFSSearch(SearchAlgorithm):
    """Breadth-First Search — unweighted, guarantees shortest path."""

    @property
    def name(self) -> str:
        return "BFS"

    def search(
        self,
        grid: Grid,
        start: Node,
        end: Node,
        heuristic: Heuristic,
        running_flag: dict[str, bool],
        on_visit: Optional[Callable[[], None]] = None,
    ) -> list[Node]:
        from collections import deque

        queue: deque[Node] = deque([start])
        start.set_state(NodeState.VISITED)

        while queue and running_flag["active"]:
            current: Node = queue.popleft()

            if current == end:
                return self.reconstruct_path(start, end)

            for neighbor in current.neighbors:
                if neighbor.is_visited or neighbor.state == NodeState.OBSTACLE:
                    continue

                neighbor.parent = current
                neighbor.set_state(NodeState.VISITED)
                queue.append(neighbor)

            start.set_state(NodeState.START)
            end.set_state(NodeState.END)

            if on_visit:
                on_visit()

        return []
