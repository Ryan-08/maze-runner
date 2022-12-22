from line import Line
from point import Point


class Cell:
    def __init__(self, win=None):
        self.has_right=True
        self.has_top=True
        self.has_left=True
        self.has_bottom=True
        self.visited = False
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if(self.has_left):
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, 'black')
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, 'white')
        if(self.has_top):
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, 'black')
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, 'white')
        if(self.has_right):
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, 'black')
        else:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, 'white')
        if(self.has_bottom):
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, 'black')
        else:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, 'white')
        
    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        # find center of this cell and to_cell
        x_mid = (self._x1 + self._x2) /2
        y_mid = (self._y1 + self._y2) /2

        to_x_mid = (to_cell._x1 + to_cell._x2)/2
        to_y_mid = (to_cell._y1 + to_cell._y2)/2

        fill='red'
        if undo:
            fill='blue'                
        # draw line
        line = Line(Point(x_mid, y_mid), Point(to_x_mid, to_y_mid))
        self._win.draw_line(line, fill)         