from collections import deque
from tkinter import messagebox, Tk
import pygame
import sys

WIN_WIDTH = 650

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))

rows = 50
cell_width = WIN_WIDTH // rows

class Cell:
    def __init__(self, r, c):
        self.x = c * cell_width
        self.y = r * cell_width
        self.source = False
        self.target = False
        self.wall = False
        self.visited = False
        self.queued = False
        self.neibours = []
        self.par = None

    def draw(self, color):
        pygame.draw.rect(WIN, color, (self.x, self.y, cell_width-2, cell_width-2))

# create grid
grid = []
for r in range(rows):
    grid.append([])
    for c in range(rows):
        grid[r].append(Cell(r, c))



for r in range(rows):
    for c in range(rows):
        node = grid[r][c]
        for dr, dc in [[r+1, c],[r-1, c],[r, c+1],[r, c-1]]:
            if dr >= 0 and dc >= 0 and dr < rows and dc < rows:
                node.neibours.append(grid[dr][dc])


source = grid[0][0]
source.source = True

q = deque()
q.append(source)
path = set()
def main():
    begin_search = False
    set_target = False
    searching = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not begin_search:
                if event.type == pygame.MOUSEMOTION:
                    x, y = pygame.mouse.get_pos()
                    r = y // cell_width
                    c = x // cell_width
                    if r>=0 and c>=0 and r<rows and c<rows:
                        cell = grid[r][c]
                        # set target
                        if event.buttons[2] and not set_target and not cell.source:
                            set_target = True
                            cell.target = True
                        # set wall
                        if event.buttons[0] and not cell.target and not cell.source:
                            cell.wall = True
                # Start bfs
                if event.type == pygame.KEYDOWN and set_target:
                    begin_search = True

        if begin_search:
            if q and searching:
                node = q.popleft()
                node.visited = True
                if node.target:
                    searching = False
                    while node.par != source:
                        path.add(node.par)
                        node = node.par
                else:
                    for nei in node.neibours:
                        if not nei.queued and not nei.wall:
                            q.append(nei)
                            nei.queued = True
                            nei.par = node
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No path exists")
                    searching = False


        WIN.fill((100, 100, 100))
        for r in range(rows):
            for c in range(rows):
                cell = grid[r][c]
                cell.draw((15, 15, 15))
                if cell.source: cell.draw((0, 100, 100))
                if cell.wall: cell.draw((255, 0, 0))
                if cell.queued and not cell.source: cell.draw((255,255,0))
                if cell.visited and not cell.source: cell.draw((255, 165, 0))
                if cell.target: cell.draw((0, 0, 255))
                if cell in path: cell.draw((0, 255, 0))

        pygame.display.flip()

main()