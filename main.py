import pygame
from typing import Optional
from threading import Thread


from src.grid import Grid, Node
from src.path_finder import PathFinder
from src.constants import MARGIN, CELL_HEIGHT, CELL_WIDTH, RESOLUTION, Colors, TOTAL_COLUMNS, TOTAL_ROWS, NodeState


class Renderer:
    def __init__(self, window: pygame.Surface) -> None:
        self.window: pygame.Surface = window
        self.font: pygame.font.Font = pygame.font.SysFont("monospace", 20)

    def draw_grid(self, grid: Grid) -> None:
        for node in grid:
            pygame.draw.rect(
                self.window,
                node.color,
                [
                    (MARGIN + CELL_WIDTH) * node.column + MARGIN,
                    (MARGIN + CELL_HEIGHT) * node.row + MARGIN,
                    CELL_WIDTH,
                    CELL_HEIGHT,
                ],
            )

    def draw_hud(self, pathfinder: PathFinder) -> None:
        y: int = RESOLUTION[1] - 30
        text: str = (
            f"Algorithm: {pathfinder.algorithm.name} (A) | "
            f"Heuristic: {pathfinder.heuristic.name} (H) | "
            f"SPACE=Run  R=Reset"
        )
        surface: pygame.Surface = self.font.render(text, True, Colors.BLACK)  # nopep8
        self.window.blit(surface, (10, y))


class App:
    def __init__(self) -> None:
        pygame.init()
        self.window: pygame.Surface = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Pathfinding Visualizer")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.renderer: Renderer = Renderer(self.window)

        self.grid: Grid = Grid(TOTAL_ROWS, TOTAL_COLUMNS)
        self.pathfinder: PathFinder = PathFinder()
        self.start: Optional[Node] = None
        self.end: Optional[Node] = None

        self.algorithm_thread: Optional[Thread] = None
        self.running_flag: dict[str, bool] = {"active": False}

    @property
    def is_algorithm_running(self) -> bool:
        return self.algorithm_thread is not None and self.algorithm_thread.is_alive()

    def handle_left_click(self, pos: tuple[int, int]) -> None:
        if self.is_algorithm_running:
            return

        x, y = pos
        col: int = x // (CELL_WIDTH + MARGIN)
        row: int = y // (CELL_HEIGHT + MARGIN)

        if not self.grid.in_bounds(row, col):
            return

        node: Node = self.grid[row][col]

        if not self.start and node != self.end:
            self.start = node
            self.start.set_state(NodeState.START)
        elif not self.end and node != self.start:
            self.end = node
            self.end.set_state(NodeState.END)
        elif node != self.start and node != self.end:
            node.set_state(NodeState.OBSTACLE)

    def handle_right_click(self, pos: tuple[int, int]) -> None:
        if self.is_algorithm_running:
            return

        x, y = pos
        col: int = x // (CELL_WIDTH + MARGIN)
        row: int = y // (CELL_HEIGHT + MARGIN)

        if not self.grid.in_bounds(row, col):
            return

        node: Node = self.grid[row][col]
        node.reset()

        if node == self.start:
            self.start = None
        if node == self.end:
            self.end = None

    def run_algorithm(self) -> None:
        self.grid.reset_search()
        self.grid.update_all_neighbors()

        self.start.set_state(NodeState.START)
        self.end.set_state(NodeState.END)

        self.running_flag["active"] = True

        def on_visit() -> None:
            pygame.time.wait(10)

        def thread_target() -> None:
            path: list[Node] = self.pathfinder.run(
                self.grid, self.start, self.end,
                self.running_flag, on_visit
            )

            if path and self.running_flag["active"]:
                for node in path:
                    if not self.running_flag["active"]:
                        break
                    node.set_state(NodeState.PATH)
                    pygame.time.wait(20)

                self.start.set_state(NodeState.START)
                self.end.set_state(NodeState.END)

        self.algorithm_thread = Thread(
            target=thread_target,
            daemon=True
        )
        self.algorithm_thread.start()

    def reset(self) -> None:
        self.running_flag["active"] = False
        if self.is_algorithm_running:
            self.algorithm_thread.join()
        self.algorithm_thread = None
        self.start = None
        self.end = None
        self.grid.reset()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if pygame.mouse.get_pressed()[0]:
                self.handle_left_click(pygame.mouse.get_pos())
            elif pygame.mouse.get_pressed()[2]:
                self.handle_right_click(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.start and self.end:
                    if not self.is_algorithm_running:
                        self.run_algorithm()

                elif event.key == pygame.K_r:
                    self.reset()

                elif event.key == pygame.K_a and not self.is_algorithm_running:
                    self.pathfinder.cycle_algorithm()

                elif event.key == pygame.K_h and not self.is_algorithm_running:
                    self.pathfinder.cycle_heuristic()

        return True

    def run(self) -> None:
        running: bool = True
        while running:
            running = self.handle_events()
            self.window.fill(Colors.BLACK)
            self.renderer.draw_grid(self.grid)
            self.renderer.draw_hud(self.pathfinder)
            pygame.display.flip()
            self.clock.tick(60)

        self.running_flag["active"] = False
        if self.is_algorithm_running:
            self.algorithm_thread.join()
        pygame.quit()


if __name__ == "__main__":
    app: App = App()
    app.run()
