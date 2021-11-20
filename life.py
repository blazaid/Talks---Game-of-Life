from collections import Counter
from itertools import product


class Universe:
    def __init__(self, cells=None, board_size=None):
        self.cells = set(cells) if cells else {}
        self.width, self.height = board_size or (None, None)
        self.generation = 0
        
        self.fit_cells_on_board()

    def step(self):
        self.cells = {
            c for c, n in self.active_neighbours().items()
            if n == 3 or (n == 2 and c in self.cells)
        }

        self.fit_cells_on_board()
        self.generation += 1
        
    def fit_cells_on_board(self):
        if self.width is not None:
            self.cells = {
                (cell[0] % self.width, cell[1])
                for cell in self.cells
            }
        if self.height is not None:
            self.cells = {
                (cell[0], cell[1] % self.height)
                for cell in self.cells
            }

    def active_neighbours(self):
        return Counter(
            neighbour
            for cell in self.cells
            for neighbour in self.neighbours(cell=cell)
        )

    def neighbours(self, cell):
        for x, y in product(range(-1, 2), repeat=2):
            if not (x == 0 and y == 0):
                neighbour_cell = [cell[0] + x, cell[1] + y]
                if self.width is not None:
                    neighbour_cell[0] = neighbour_cell[0] % self.width
                if self.height is not None:
                    neighbour_cell[1] = neighbour_cell[1] % self.height
                yield tuple(neighbour_cell)

    @property
    def size(self):
        return len(self.cells)
    
    def __str__(self):
        b = board(self)
        return next(b)

    
def board(universe, size=None, gens=None, ok='⬛', ko='⬜'):
    if size is None:
        if universe.width is None or universe.height is None:
            raise ValueError('Must specify either board\'s "size" param or Universe\'s "board_size" param')
        else:
            width, height = universe.width, universe.height
    else:
        width, height = size
    while gens is None or universe.generation < gens:
        yield '\n'.join(
        ''.join(
            ok if (x, y) in universe.cells else ko for x in range(width))
            for y in range(height)
        )
        universe.step()


def pattern(shape, live='#'):
    return {
        (x, y) 
        for (y, row) in enumerate(shape.strip().splitlines())
        for (x, c) in enumerate(row)
        if c == live
    }


def shift(cells, dx, dy):
    return {(x + dx, y + dy) for (x, y) in cells}


blinker = pattern("""###""")

toad    = pattern("""
.###
###.
""")

beehive = pattern("""
.##.
#..#
.##.
""")
