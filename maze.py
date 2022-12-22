import random
import time
from cell import Cell

class Maze:
    def __init__(
        self, 
        start,
        end,
        x1, 
        y1, 
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None        
    ):        
        self._cells = []
        self._start = start
        self._end = end
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visted()

    # create list of cells
    def _create_cells(self):    
        for i in range(self._num_cols):                   
            col_cells = []
            for j in range(self._num_rows):                
                col_cells.append(Cell(self._win) )                                                
            self._cells.append(col_cells)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
        
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[self._start][0].has_top = False
        self._draw_cell(0,0)
        self._cells[self._end][self._num_rows-1].has_bottom = False
        self._draw_cell(self._num_cols-1,self._num_rows-1)
    
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            possible_direction_indexes = 0

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
                possible_direction_indexes += 1
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
                possible_direction_indexes += 1
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
                possible_direction_indexes += 1
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
                possible_direction_indexes += 1

            # if there is nowhere to go from here
            # just break out
            if possible_direction_indexes == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(possible_direction_indexes)
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right = False
                self._cells[i + 1][j].has_left = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left = False
                self._cells[i - 1][j].has_right = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom = False
                self._cells[i][j + 1].has_top = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top = False
                self._cells[i][j - 1].has_bottom = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visted(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False


    def solve(self):
        self._solve_r(self._start, 0)

    def _solve_r(self, i, j):
        self._animate()
        # current_cell = self._cells[i][j]
        # set current as visited
        self._cells[i][j].visited = True
        if i == self._end and j == self._num_rows - 1:
            return True

        # right
        if not self._cells[i][j].has_right and not self._cells[i + 1][j].visited:
            self._cells[i][j].draw_move(self._cells[i + 1][j])      
            if self._solve_r(i+1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i + 1][j], True)      
        # down
        if not self._cells[i][j].has_bottom and not self._cells[i][j + 1].visited:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j+1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j + 1], True)
        # left
        if i > 0 and not self._cells[i][j].has_left and not self._cells[i - 1][j].visited:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i-1][j], True)                
        # up
        if j > 0 and not self._cells[i][j].has_top and not self._cells[i][j - 1].visited:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j-1], True)    
        
        return False