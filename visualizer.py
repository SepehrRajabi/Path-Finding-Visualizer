import pygame


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
pygame.time.Clock().tick(60)


class Node:
    def __init__(self, row, column):
        self.neighbors = []
        self.parent = None

        self.is_obstacle = False
        self.is_visited = False

        self.row = row
        self.column = column

        self.color = WHITE

    def get_position(self):
        return self.row, self.column

    def make_visited(self):
        self.is_visited = True
        self.color = BLUE

    def make_obstacle(self):
        self.is_obstacle = True
        self.color = BLACK

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED

    def make_path(self):
        self.color = PURPLE


def check_coords(grid, row, column):
    row_inbound = 0 <= row and row < len(grid)
    column_inbound = 0 <= column and column < len(grid[0])
    
    return row_inbound and column_inbound


def update_neighbors(grid, row, column):
    node = grid[row][column]
    #                  Down                Up               Left                Right  
    indecies = [(row - 1, column), (row, column + 1), (row, column - 1), (row + 1, column)]
    for r, c in indecies:
        if check_coords(grid, row=r, column=c) and not grid[r][c].is_obstacle:
            node.neighbors.append(grid[r][c])


def make_grid(total_rows, total_columns):
    return [[Node(row, column) for row in range(total_rows)] for column in range(total_columns)]


def draw_grid(window, grid):
    total_rows = len(grid)
    total_columns = len(grid[0])

    for row in range(total_rows):
        for column in range(total_columns):
            node = grid[row][column]
            pygame.draw.rect(window,
                             node.color,
                             [(MARGIN + CELL_WIDTH) * column + MARGIN,
                              (MARGIN + CELL_HEIGHT) * row + MARGIN,
                              CELL_WIDTH,
                              CELL_HEIGHT])


def heuristic(node_1, node_2):
    x1, y1 = node_1.get_position()
    x2, y2 = node_2.get_position()

    return abs(x1 - x2) + abs(y1 - y2)


# def reconstruct_path(window, path: list):
#     length = len(path)
#     for i in range(1, length + 1):
#         current_node = path[-i]
#         current_node.make_path()
#         pygame.draw.line(window, TURQUOISE, start_pos, end_pos)


def a_star_search(grid, start, end):
    path = []
    path.append(end)

    local_values = {node: float("inf") for row in grid for node in row}
    global_values = {node: float("inf") for row in grid for node in row}
    
    global_values[start] = heuristic(start, end)
    local_values[start] = 0

    nodes_to_test = {}
    nodes_to_test[start] = global_values[start]
    while nodes_to_test:
        current_node = min(nodes_to_test, key=nodes_to_test.get)

        if current_node == end:
            end.make_end()
            break

        for neighbor in current_node.neighbors:
            nodes_to_test[neighbor] = global_values[neighbor]
            
            temp_local_value = local_values[current_node] + heuristic(current_node, neighbor)
            if temp_local_value < local_values[neighbor]:
                neighbor.parent = current_node
                local_values[neighbor] = temp_local_value
                global_values[neighbor] = local_values[neighbor] + heuristic(neighbor, end)

        current_node.make_visited()
        nodes_to_test.pop(current_node)
        # making the start node's color green because "technically" we are not visiting the node we are starting on
        start.make_start()
    
    node = path[-1]
    while node != start:
        path.append(node.parent)
        node = path[-1]

    return path


def main():
    start = None
    end = None

    total_rows = 40
    total_columns = 40
    grid = make_grid(total_rows, total_columns)

    done = False
    while not done:
        draw_grid(window, grid)
        pygame.display.flip() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # handle the left mouse button click
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()

                column = x // (CELL_WIDTH + MARGIN)
                row = y // (CELL_HEIGHT + MARGIN)

                node = grid[row][column]

                # setting the start node if it is not already set and the node pressed is not the end node
                if not start and node != end:
                    start = node
                    start.make_start()

                # setting the end node if it is not already set and the node pressed is not the start node
                elif not end and node != start:
                    end = node
                    end.make_end()

                # setting the obstacles if the start and end nodes are both chosen
                elif node != start and node != end:
                    node.make_obstacle()

            # handle the left mouse button click
            # right clicking on a node will reset that node
            elif pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()

                column = x // (CELL_WIDTH + MARGIN)
                row = y // (CELL_HEIGHT + MARGIN)

                node = grid[row][column]
                node.color = WHITE

                if node == start:
                    start = None

                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in range(total_rows):
                        for column in range(total_columns):
                            # print(f"{row}, {column} --- updating neighbors")
                            update_neighbors(grid, row, column)

                    a_star_search(grid, start, end)

                # when the r key is pressed the entire grid is reset
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(total_rows, total_columns)
                    draw_grid(window, grid)

        window.fill(BLACK)
    pygame.quit()


if __name__ == "__main__":
    main()
