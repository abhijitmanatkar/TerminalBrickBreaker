from globals import *


class Grid():
    '''Grid class to display everything'''

    def __init__(self, height=HEIGHT, width=WIDTH):
        # Generate and border grid
        self.height = height
        self.width = width
        self.canvas = [[' ' for _ in range(width)] for __ in range(height)]
        self.canvas[0] = ['#' for _ in range(width)]
        self.canvas[height - 1] = self.canvas[0]
        for i in range(len(self.canvas)):
            self.canvas[i][0] = '#'
            self.canvas[i][width - 1] = '#'

    def __str__(self):
        # Print grid
        ret = ''
        for row in self.canvas:
            for col in row:
                ret += col
            ret += '\n'
        return ret

    def __eq__(self, other):
        if self.canvas == other.canvas:
            return True
        else:
            return False

    def draw(self, obj):
        # Draw on object onto the grid
        xBase, yBase = obj.pos
        for y in range(len(obj.img)):
            for x in range(len(obj.img[y])):
                if (yBase + y < self.height) and (xBase + x < self.width):
                    self.canvas[yBase + y][xBase + x] = obj.img[y][x]
