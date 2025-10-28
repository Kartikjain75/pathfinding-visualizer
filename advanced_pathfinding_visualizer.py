import pygame
import math
from queue import PriorityQueue, Queue, LifoQueue

# ========== INITIAL SETUP ==========
import pygame
pygame.init()

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

WIDTH = int(min(screen_width, screen_height) * 0.85)

UI_HEIGHT = int(WIDTH * 0.12)

WIN = pygame.display.set_mode((WIDTH, WIDTH + UI_HEIGHT))
WIN.fill((255, 255, 255))
pygame.display.set_caption("Advanced Pathfinding Visualizer 🧭")

pygame.init()
pygame.font.init()


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (100, 149, 237)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (138, 43, 226)
ORANGE = (255, 165, 0)
GREY = (200, 200, 200)

# ========== NODE CLASS ==========
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self): return self.row, self.col
    def is_closed(self): return self.color == RED
    def is_open(self): return self.color == GREEN
    def is_barrier(self): return self.color == BLACK
    def is_start(self): return self.color == ORANGE
    def is_end(self): return self.color == PURPLE
    def reset(self): self.color = WHITE
    def make_start(self): self.color = ORANGE
    def make_closed(self): self.color = RED
    def make_open(self): self.color = GREEN
    def make_barrier(self): self.color = BLACK
    def make_end(self): self.color = PURPLE
    def make_path(self): self.color = YELLOW
    def draw(self, win): pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

# ========== UTILITIES ==========
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# ========== ALGORITHMS ==========

def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    f_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def dijkstra(draw, grid, start, end):
    pq = PriorityQueue()
    pq.put((0, start))
    dist = {node: float("inf") for row in grid for node in row}
    dist[start] = 0
    came_from = {}

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = pq.get()[1]

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp = dist[current] + 1
            if temp < dist[neighbor]:
                came_from[neighbor] = current
                dist[neighbor] = temp
                pq.put((temp, neighbor))
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def bfs(draw, grid, start, end):
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {start}

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = queue.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.put(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def dfs(draw, grid, start, end):
    stack = LifoQueue()
    stack.put(start)
    came_from = {}
    visited = {start}

    while not stack.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = stack.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.put(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False

# ========== DRAWING FUNCTIONS ==========
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([Node(i, j, gap, rows) for j in range(rows)])
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width, algo_name="None"):
    win.fill(WHITE)

    # Draw all grid cells
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)

    # --- Title Bar ---
    title_font = pygame.font.SysFont("arial", 26, bold=True)
    title_text = title_font.render("Pathfinding Visualizer", True, (25, 25, 112))
    title_rect = title_text.get_rect(center=(width // 2, 20))
    win.blit(title_text, title_rect)

    # --- Algorithm name display ---
    font = pygame.font.SysFont("arial", 20)
    text = font.render(f"Algorithm: {algo_name}", True, (0, 0, 0))
    win.blit(text, (20, 10))

    # --- Exit button ---
    button_font = pygame.font.SysFont("arial", 18)
    exit_text = button_font.render("Exit ✖", True, (255, 255, 255))
    exit_rect = pygame.Rect(width - 90, 15, 80, 30)
    pygame.draw.rect(win, (220, 20, 60), exit_rect, border_radius=6)
    win.blit(exit_text, (width - 75, 20))

    # --- Legend box (Colors) ---
    legend_x = 20
    legend_y = 50
    legend_font = pygame.font.SysFont("arial", 16)

    legend_items = [
        ("Start", (255, 165, 0)),    # Orange
        ("End", (128, 0, 128)),      # Purple
        ("Barrier", (0, 0, 0)),      # Black
        ("Open Set", (0, 0, 255)),   # Blue
        ("Closed Set", (255, 0, 0)), # Red
        ("Path", (255, 255, 0)),     # Yellow
        ("Empty", (255, 255, 255)),  # White
    ]

    pygame.draw.rect(win, (240, 240, 240), (legend_x - 5, legend_y - 5, 160, 200), border_radius=8)
    pygame.draw.rect(win, (180, 180, 180), (legend_x - 5, legend_y - 5, 160, 200), 2, border_radius=8)
    title = legend_font.render("Color Legend:", True, (0, 0, 0))
    win.blit(title, (legend_x, legend_y - 25))

    for i, (label, color) in enumerate(legend_items):
        y_offset = legend_y + i * 25
        pygame.draw.rect(win, color, (legend_x, y_offset, 20, 20))
        pygame.draw.rect(win, (0, 0, 0), (legend_x, y_offset, 20, 20), 1)
        text = legend_font.render(label, True, (0, 0, 0))
        win.blit(text, (legend_x + 30, y_offset + 2))

    # --- Algorithm Legend Box ---
    algo_legend_x = 260
    algo_legend_y = 50
    algo_items = [
        ("1 → A* (Fastest)", (30, 144, 255)),
        ("2 → Dijkstra’s", (50, 205, 50)),
        ("3 → BFS", (255, 140, 0)),
        ("4 → DFS", (138, 43, 226)),
        ("SPACE → Run", (0, 0, 0)),
        ("C → Clear Grid", (0, 0, 0)),
    ]

    pygame.draw.rect(win, (240, 240, 240), (algo_legend_x - 5, algo_legend_y - 5, 200, 180), border_radius=8)
    pygame.draw.rect(win, (180, 180, 180), (algo_legend_x - 5, algo_legend_y - 5, 200, 180), 2, border_radius=8)
    title2 = legend_font.render("Algorithms:", True, (0, 0, 0))
    win.blit(title2, (algo_legend_x, algo_legend_y - 25))

    for i, (label, color) in enumerate(algo_items):
        y_offset = algo_legend_y + i * 25
        text = legend_font.render(label, True, color)
        win.blit(text, (algo_legend_x, y_offset + 2))

    pygame.display.update()
    return exit_rect

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

# ========== MAIN LOOP ==========
def main(win, width):
    ROWS = 40
    grid = make_grid(ROWS, width)

    start = None
    end = None
    run = True
    algo = "None"

    while run:
        exit_rect = draw(win, grid, ROWS, width, algo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_rect.collidepoint(mouse_pos):
                    run = False
                    break

                row, col = get_clicked_pos(mouse_pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_1:
                    algo = "A*"

                if event.key == pygame.K_2:
                    algo = "Dijkstra"

                if event.key == pygame.K_3:
                    algo = "BFS"

                if event.key == pygame.K_4:
                    algo = "DFS"

                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    if algo == "A*":
                        a_star(lambda: draw(win, grid, ROWS, width, algo), grid, start, end)
                    elif algo == "Dijkstra":
                        dijkstra(lambda: draw(win, grid, ROWS, width, algo), grid, start, end)
                    elif algo == "BFS":
                        bfs(lambda: draw(win, grid, ROWS, width, algo), grid, start, end)
                    elif algo == "DFS":
                        dfs(lambda: draw(win, grid, ROWS, width, algo), grid, start, end)

    pygame.quit()
main(WIN, WIDTH)