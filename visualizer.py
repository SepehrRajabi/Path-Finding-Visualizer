import pygame
import threading


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)


RESOLUTION = (885, 885)
CELL_WIDTH = 20
CELL_HEIGHT = 20
MARGIN = 2


pygame.init()
window = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("A star algorithm")
clock = pygame.time.Clock()


class Node:
    def __init__(self, row, column):
        self.neighbors = []
        self.parent = None

        self.is_obstacle = False
        self.is_visited = False

        self.row = row
        self.column = column

        self.color = WHITE
        self.lock = threading.Lock()

    def get_position(self):
        return self.row, self.column

    def make_visited(self):
        with self.lock:
            self.is_visited = True
            self.color = BLUE

    def make_obstacle(self):
        with self.lock:
            self.is_obstacle = True
            self.color = BLACK

    def make_start(self):
        with self.lock:
            self.color = GREEN

    def make_end(self):
        with self.lock:
            self.color = RED

    def make_path(self):
        with self.lock:
            self.color = PURPLE

    def reset(self):
        with self.lock:
            self.color = WHITE
            self.is_obstacle = False
            self.is_visited = False
            self.parent = None
            self.neighbors = []


def check_coords(grid, row, column):
    row_inbound = 0 <= row < len(grid)
    column_inbound = 0 <= column < len(grid[0])

    return row_inbound and column_inbound


def update_neighbors(grid, row, column):
    node = grid[row][column]
    indices = [
        (row - 1, column),
        (row, column + 1),
        (row, column - 1),
        (row + 1, column)
    ]
    for r, c in indices:
        if check_coords(grid, row=r, column=c) and not grid[r][c].is_obstacle:
            node.neighbors.append(grid[r][c])


def make_grid(total_rows, total_columns):
    return [[Node(row, column) for column in range(total_columns)] for row in range(total_rows)]


def draw_grid(window, grid):
    total_rows = len(grid)
    total_columns = len(grid[0])

    for row in range(total_rows):
        for column in range(total_columns):
            node = grid[row][column]
            with node.lock:
                color = node.color
            pygame.draw.rect(
                window,
                color,
                [
                    (MARGIN + CELL_WIDTH) * column + MARGIN,
                    (MARGIN + CELL_HEIGHT) * row + MARGIN,
                    CELL_WIDTH,
                    CELL_HEIGHT]
            )


class AStarThread(threading.Thread):
    def __init__(self, grid, start, end):
        super().__init__(daemon=True)
        self.grid = grid
        self.start_node = start
        self.end_node = end
        self.path = []
        self.running = True
        self.finished = False

    def stop(self):
        self.running = False

    def heuristic(self, node_1, node_2):
        x1, y1 = node_1.get_position()
        x2, y2 = node_2.get_position()

        return abs(x1 - x2) + abs(y1 - y2)

    def run(self):
        grid = self.grid
        start = self.start_node
        end = self.end_node

        local_values = {node: float("inf") for row in grid for node in row}
        global_values = {node: float("inf") for row in grid for node in row}

        global_values[start] = self.heuristic(start, end)
        local_values[start] = 0

        nodes_to_test = {}
        nodes_to_test[start] = global_values[start]

        found = False

        while nodes_to_test and self.running:
            current_node = min(nodes_to_test, key=nodes_to_test.get)

            if current_node == end:
                end.make_end()
                found = True
                break

            for neighbor in current_node.neighbors:
                if neighbor.is_visited:
                    continue

                temp_local_value = local_values[current_node] + self.heuristic(current_node, neighbor)  # nopep8
                if temp_local_value < local_values[neighbor]:
                    neighbor.parent = current_node
                    local_values[neighbor] = temp_local_value
                    global_values[neighbor] = local_values[neighbor] + self.heuristic(neighbor, end)  # nopep8

                nodes_to_test[neighbor] = global_values[neighbor]

            current_node.make_visited()
            nodes_to_test.pop(current_node)
            start.make_start()

            # Small delay so we can see the animation
            pygame.time.wait(10)

        if found and self.running:
            # Reconstruct the path
            self.path.append(end)
            node = end
            while node != start and self.running:
                self.path.append(node.parent)
                node = self.path[-1]

            # Animate the path
            for node in self.path:
                if not self.running:
                    break
                node.make_path()
                pygame.time.wait(20)

            start.make_start()
            end.make_end()

        self.finished = True


def main():
    start = None
    end = None
    algorithm_thread = None

    total_rows = 40
    total_columns = 40
    grid = make_grid(total_rows, total_columns)

    done = False
    while not done:
        window.fill(BLACK)
        draw_grid(window, grid)
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if algorithm_thread and algorithm_thread.is_alive():
                    algorithm_thread.stop()
                    algorithm_thread.join()
                done = True

            # Don't allow interaction while algorithm is running
            if algorithm_thread and algorithm_thread.is_alive():
                continue

            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()

                column = x // (CELL_WIDTH + MARGIN)
                row = y // (CELL_HEIGHT + MARGIN)

                if row < total_rows and column < total_columns:
                    node = grid[row][column]

                    if not start and node != end:
                        start = node
                        start.make_start()

                    elif not end and node != start:
                        end = node
                        end.make_end()

                    elif node != start and node != end:
                        node.make_obstacle()

            elif pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()

                column = x // (CELL_WIDTH + MARGIN)
                row = y // (CELL_HEIGHT + MARGIN)

                if row < total_rows and column < total_columns:
                    node = grid[row][column]
                    node.reset()

                    if node == start:
                        start = None

                    if node == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in range(total_rows):
                        for column in range(total_columns):
                            update_neighbors(grid, row, column)

                    algorithm_thread = AStarThread(grid, start, end)
                    algorithm_thread.start()

                if event.key == pygame.K_r:
                    if algorithm_thread and algorithm_thread.is_alive():
                        algorithm_thread.stop()
                        algorithm_thread.join()
                    algorithm_thread = None
                    start = None
                    end = None
                    grid = make_grid(total_rows, total_columns)

    pygame.quit()


if __name__ == "__main__":
    main()
